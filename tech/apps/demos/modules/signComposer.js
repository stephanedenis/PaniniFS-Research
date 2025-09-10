/* signComposer.js
 * Compose a sign specification from components.
 * composeSign({handshapeCode, movementPath, durationMs, nmfPresetIds, facialPresetIds})
 */
import { getHandshape } from './signDataLoader.js';
import { getFacialPreset } from './facialPresetLoader.js';

function now(){ return performance.now(); }

export function composeSign({handshapeCode, movementPath = [{x:0,y:0,z:0}], durationMs = 800, nmfPresetIds = [], facialPresetIds = []}={}){
  const t0 = now();
  const handshape = handshapeCode ? getHandshape(handshapeCode) : null;
  const facial = facialPresetIds.map(id=>getFacialPreset(id)).filter(Boolean);
  const phases = _derivePhases(movementPath, durationMs);
  const spec = { version:'0.1', handshapeCode, handshape, movementPath, durationMs, phases, nmfPresetIds, facialPresetIds, facial, meta:{createdAt:Date.now()} };
  const t1 = now();
  spec.meta.composeMs = +(t1 - t0).toFixed(2);
  return spec;
}

function _derivePhases(path, total){
  if(path.length < 2) return [{t:0,pos:path[0]},{t:total,pos:path[0]}];
  const segDur = total/(path.length-1);
  return path.map((p,i)=>({t:Math.round(i*segDur), pos:p}));
}

export function blendSequential(specA, specB, overlapRatio=0.2){
  const overlap = Math.min(specA.durationMs * overlapRatio, specA.durationMs);
  const adjustedStartB = specA.durationMs - overlap;
  return { sequence:[specA,specB], overlapMs:overlap, startB:adjustedStartB };
}

export default { composeSign, blendSequential };
