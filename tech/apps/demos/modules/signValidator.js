/* signValidator.js
 * Validate composed sign specs against nmf rules & facial conflicts.
 */
import { getNmfRules } from './signDataLoader.js';
import { getFacialPresets } from './facialPresetLoader.js';

export function validateSign(signSpec){
  const errors=[]; const warnings=[];
  if(!signSpec) return {errors:['spec:null'],warnings};
  if(!signSpec.handshape) warnings.push('handshape:missingDetail');
  if(!Array.isArray(signSpec.movementPath) || signSpec.movementPath.length===0) errors.push('movementPath:empty');
  // Facial conflict sample: brow_question + brow_wh both
  const facialIds = new Set(signSpec.facialPresetIds||[]);
  if(facialIds.has('brow_question') && facialIds.has('brow_wh')) warnings.push('facial:questionWhMix');
  // Evaluate minimal nmf expression engine (only simple AND conflicts demo)
  try {
    const rules = getNmfRules();
    rules.forEach(r=>{
      if(r.if && r.if.includes('FACS_AU01') && r.if.includes('FACS_AU04')){
        // Simulate reading intensities from facial presets
        const facial = getFacialPresets();
        const au1 = facialIds.has('brow_question') ? 0.7 : 0;
        const au4 = facialIds.has('brow_wh') ? 0.6 : 0;
        if(au1>0.5 && au4>0.5){
          (r.level==='ERROR'?errors:warnings).push(r.id);
        }
      }
    });
  } catch(e){ warnings.push('nmfRules:evaluationError'); }
  return {errors,warnings};
}

export default { validateSign };
