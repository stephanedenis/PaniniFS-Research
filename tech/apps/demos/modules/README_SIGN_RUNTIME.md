# Sign Runtime Layer (Hands + Facial Non-Manuals)

## Modules
- signDataLoader.js: Loads handshapes & NMF rules (cached) from `tech/data/presets/*`.
- facialPresetLoader.js: Loads facial expression presets (blendshape targets & intensity metadata).
- signComposer.js: Composes a sign spec from primitives (handshape, movementPath, facial presets, nmf tags) and records timing.
- signValidator.js: Lightweight validation using NMF rules + facial conflict heuristics.

## Data Flow
Authoritative source JSON (domain) lives in `panini/data/sign/*_v0_1.json`.
Runtime normalized copies in `tech/data/presets/*.v0.1.json` are what the demo fetches.

```
 panini/data/sign/handshapes_preset_v0_1.json  -->  tech/data/presets/handshapes_preset.v0.1.json
 panini/data/sign/nmf_rules_v0_1.json          -->  tech/data/presets/nmf_rules.v0.1.json
 panini/data/sign/facial_presets_v0_1.json     -->  tech/data/presets/facial_presets.v0.1.json
```

## Global Runtime Interface
`window.signRuntime` (created during demo `init()`):
```
{
  data: {
    getHandshapes(), getHandshape(code), getNmfRules(), getFacialPresets()
  },
  compose(options) -> signSpec,
  validate(signSpec) -> { errors:[], warnings:[] }
}
```
Overlay (bottom-right) updates compose time and validation counts.

## composeSign Options
```
{
  handshapeCode: 'A',
  movementPath: [{x:0,y:0,z:0}, {x:0.1,y:0.2,z:0}],
  durationMs: 900,
  nmfPresetIds: ['brow_question'],
  facialPresetIds: ['brow_question']
}
```

## Example (in browser console)
```
const spec = signRuntime.compose({ handshapeCode:'A', movementPath:[{x:0,y:0,z:0},{x:0,y:0.15,z:0}], facialPresetIds:['brow_question'] });
const res = signRuntime.validate(spec);
console.log(spec.meta.composeMs, res);
```

## Future Extensions
- Coarticulation smoothing with parametric easing between overlapping phases.
- Rich rule engine (AST parse of logical expressions for NMF rules).
- Inverse kinematics application to skeletal rig directly from handshape angles.
- Facial blendshape animation timeline derived from intensity envelope.
- Serialization format EXT_avatar_sign@0.2 capturing multi-channel timing.

## HandIK (Prototype)
Module: `handIK.js`
Purpose: Map `handshape.angles` (MCP/PIP/DIP) to approximate bone rotations on loaded GLTF rig.
Heuristics:
- Looks for bone names like `index_proximal`, `middle_middle`, etc. (lowercased).
- Applies flexion as rotation.x in radians (direct set, no blending yet).
Usage (console):
```
window.handIK && window.handIK.applyHandshape('A');
```
Limitations:
- No abduction/adduction or splay implemented yet.
- No interpolation (future: blend rather than overwrite).
- Bone name patterns may need adaptation per rig.


## Testing Notes
`sign-runtime.spec.js` is a minimal presence test; it skips when running directly via `file://`. For full automation serve the `tech/apps/demos` directory over HTTP.

