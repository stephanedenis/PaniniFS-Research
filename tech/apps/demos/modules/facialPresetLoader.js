/* facialPresetLoader.js
 * Loader & cache for facial expression presets (non-manual markers).
 */
const FACIAL_PATH = '../../data/presets/facial_presets.v0.1.json';
let _facialCache = null;

function _fetchJSON(path){
  return fetch(path,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('Fetch '+path+' '+r.status);return r.json();});
}
function _validate(json){
  const errors=[];
  if(!json||typeof json!=='object') errors.push('root:notObject');
  if(!Array.isArray(json.facialPresets)) errors.push('facialPresets:notArray');
  else json.facialPresets.forEach((p,i)=>{if(!p.id) errors.push('facialPresets['+i+'].id:missing');});
  return errors;
}
export async function loadFacialPresets({force=false}={}){
  if(!force && _facialCache) return _facialCache;
  const json=await _fetchJSON(FACIAL_PATH);
  const errors=_validate(json);
  if(errors.length) console.warn('[facialPresetLoader] validation',errors);
  _facialCache=json;return json;
}
export function getFacialPresets(){ if(!_facialCache) throw new Error('Facial presets not loaded'); return _facialCache.facialPresets; }
export function getFacialPreset(id){ return getFacialPresets().find(p=>p.id===id)||null; }
export function getFacialVersion(){ return _facialCache?.version||null; }
export default {loadFacialPresets,getFacialPresets,getFacialPreset,getFacialVersion};
