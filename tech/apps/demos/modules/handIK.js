/* handIK.js
 * Minimal mapping of handshape angle spec -> GLTF skeleton bone rotations.
 * This is a heuristic placeholder (NOT anatomically perfect).
 */
import { getHandshape } from './signDataLoader.js';

// Bone name candidates per finger (heuristic; adapt to actual rig names)
const FINGER_BONES = {
  thumb: ['thumb_metacarpal', 'thumb_proximal', 'thumb_distal'],
  index: ['index_metacarpal', 'index_proximal', 'index_middle', 'index_distal'],
  middle: ['middle_metacarpal', 'middle_proximal', 'middle_middle', 'middle_distal'],
  ring: ['ring_metacarpal', 'ring_proximal', 'ring_middle', 'ring_distal'],
  pinky: ['pinky_metacarpal', 'pinky_proximal', 'pinky_middle', 'pinky_distal']
};

// Angle keys mapping: MCP->proximal flexion, PIP->middle, DIP->distal, splay.* -> metacarpal Y spread
const ANGLE_KEY_MAP = {
  MCP: { axis: 'x', scale: deg=>deg * (Math.PI/180) },
  PIP: { axis: 'x', scale: deg=>deg * (Math.PI/180) },
  DIP: { axis: 'x', scale: deg=>deg * (Math.PI/180) }
};

export class HandIK {
  constructor(root){
    this.root = root; // three.js model root
    this.boneIndex = {};
    this._indexBones(root);
  }
  _indexBones(obj){
    obj.traverse(node => {
      if(node.isBone){
        this.boneIndex[node.name.toLowerCase()] = node;
      }
    });
  }
  applyHandshape(code){
    const hs = getHandshape(code);
    if(!hs){ console.warn('[HandIK] handshape not found', code); return; }
    const angles = hs.angles || {};
    Object.entries(angles).forEach(([k,v])=>{
      // e.g. index.MCP
      const [finger, joint] = k.split('.');
      if(!joint){ return; }
      if(finger.startsWith('splay')){ return; } // skip splay heuristic for now
      const boneList = FINGER_BONES[finger];
      if(!boneList) return;
      const map = ANGLE_KEY_MAP[joint];
      if(!map) return;
      // Choose bone by joint order: MCP -> proximal (index 1), PIP -> middle (index 2), DIP -> distal (index 3)
      const boneName = (joint === 'MCP') ? boneList[1] : (joint === 'PIP') ? boneList[2] : (joint === 'DIP') ? boneList[3] : null;
      if(!boneName) return;
      const bone = this._findBone(boneName);
      if(!bone) return;
      const rad = map.scale(v);
      // Simple set on X; could blend instead of overwrite
      bone.rotation.x = rad;
    });
  }
  _findBone(name){
    return this.boneIndex[name.toLowerCase()] || null;
  }
}

export function initHandIK(model){
  // Find a skinned mesh and use its skeleton root
  let skinned = null;
  model.traverse(o=>{ if(o.isSkinnedMesh && !skinned) skinned = o; });
  if(!skinned || !skinned.skeleton){ console.warn('[HandIK] No skinned mesh found'); return null; }
  return new HandIK(skinned.skeleton.bones[0].parent || model);
}

export default { HandIK, initHandIK };
