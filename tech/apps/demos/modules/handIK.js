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

// Alternate name patterns to improve detection (lowercased)
const ALT_NAME_MAP = [
  { pattern: /thumb.*metacarp/, alias: 'thumb_metacarpal' },
  { pattern: /thumb.*prox/, alias: 'thumb_proximal' },
  { pattern: /index.*metacarp/, alias: 'index_metacarpal' },
  { pattern: /index.*prox/, alias: 'index_proximal' },
  { pattern: /middle.*metacarp/, alias: 'middle_metacarpal' },
  { pattern: /ring.*metacarp/, alias: 'ring_metacarpal' },
  { pattern: /pinky.*metacarp|little.*metacarp/, alias: 'pinky_metacarpal' }
];

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
    this.targets = {}; // boneName -> { xTarget }
    this.speed = 8; // blending speed factor
  this._activeTransition = null; // { endTime, code }
    this._indexBones(root);
  }
  _indexBones(obj){
    obj.traverse(node => {
      if(node.isBone){
        const key = node.name.toLowerCase();
        this.boneIndex[key] = node;
        this.targets[key] = { xTarget: node.rotation.x };
  // Alternate mapping
  ALT_NAME_MAP.forEach(m => { if(m.pattern.test(key)) { this.boneIndex[m.alias] = node; this.targets[m.alias] = this.targets[key]; } });
      }
    });
  }
  applyHandshapeImmediate(code){
    const hs = getHandshape(code);
    if(!hs){ console.warn('[HandIK] handshape not found', code); return; }
    this._iterateAngles(hs.angles, (bone, rad)=>{ bone.rotation.x = rad; this.targets[bone.name.toLowerCase()].xTarget = rad; });
  }
  applyHandshape(code){
    const hs = getHandshape(code);
    if(!hs){ console.warn('[HandIK] handshape not found', code); return; }
    this._iterateAngles(hs.angles, (bone, rad)=>{ const tgt = this.targets[bone.name.toLowerCase()]; if(tgt) tgt.xTarget = rad; });
  }
  transitionToHandshape(code, durationMs=300){
    this.applyHandshape(code);
    this._activeTransition = { endTime: performance.now() + durationMs, code };
  }
  _iterateAngles(angles={}, fn){
    Object.entries(angles).forEach(([k,v])=>{
      const [finger,joint] = k.split('.');
      if(!joint) return;
      if(finger === 'splay'){ // splay.index / splay.pinky
        // crude splay: rotate metacarpal Y slightly
        const [_, which] = k.split('.');
        const metaName = which === 'index' ? 'index_metacarpal' : which === 'pinky' ? 'pinky_metacarpal' : null;
        if(!metaName) return;
        const bone = this._findBone(metaName);
        if(!bone) return;
        const rad = (v * 0.5) * (Math.PI/180); // reduce magnitude
        const target = this.targets[metaName.toLowerCase()];
        if(target) target.yTarget = (target.yTarget ?? bone.rotation.y) + rad;
        return;
      }
      const boneList = FINGER_BONES[finger];
      if(!boneList) return;
      const map = ANGLE_KEY_MAP[joint];
      if(!map) return;
      const boneName = (joint==='MCP')?boneList[1]:(joint==='PIP')?boneList[2]:(joint==='DIP')?boneList[3]:null;
      if(!boneName) return;
      const bone = this._findBone(boneName);
      if(!bone) return;
      const rad = map.scale(v);
      fn(bone, rad);
    });
  }
  update(dt){
    // Simple exponential approach
    const blend = 1 - Math.exp(-this.speed * dt);
    Object.entries(this.targets).forEach(([key, tgt])=>{
      const bone = this.boneIndex[key];
      if(!bone) return;
      const current = bone.rotation.x;
      bone.rotation.x = current + (tgt.xTarget - current) * blend;
      if(typeof tgt.yTarget === 'number') {
        const cy = bone.rotation.y;
        bone.rotation.y = cy + (tgt.yTarget - cy) * blend;
      }
    });
    if(this._activeTransition && performance.now() > this._activeTransition.endTime){
      this._activeTransition = null;
    }
  }
  _findBone(name){ return this.boneIndex[name.toLowerCase()] || null; }
}

export function initHandIK(model){
  // Find a skinned mesh and use its skeleton root
  let skinned = null;
  model.traverse(o=>{ if(o.isSkinnedMesh && !skinned) skinned = o; });
  if(!skinned || !skinned.skeleton){ console.warn('[HandIK] No skinned mesh found'); return null; }
  return new HandIK(skinned.skeleton.bones[0].parent || model);
}

export default { HandIK, initHandIK };
