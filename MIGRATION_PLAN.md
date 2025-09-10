# Repository Migration Plan (Dual Axis: Domain vs Tech)

Status: Phase P2 IN PROGRESS (demos, vendor libs, dataset split) – Updated 2025-09-10 UTC
Scope: Define mapping from current layout to target structure separating domain knowledge (panini/) and technical implementation (tech/).

## 1. Principles
- Separation of concerns: WHAT (linguistic, anatomical, conceptual research) vs HOW (software, tooling, runtime assets)
- No symbolic links; history preserved via `git mv` when executed.
- English normalized naming (snake_case for directories & multiword files, lowercase).
- Versioned data: raw domain datasets in panini/data, derived/runtime in tech/data or tech/assets.
- Incremental phases with stability gates; tests updated before removing originals.

## 2. Target Top-Level
```
panini/
  specs/ discoveries/ data/ references/ roadmap/ methodology/ publications/
tech/
  specs/ discoveries/ data/ references/ roadmap/ apps/ scripts/ tests/ assets/ docs/
shared/ (future: governance, licenses)
```

## 3. Mapping Table (Phase Priority)
| Old Path | New Path | Category | Axis | Priority |
|----------|----------|----------|------|----------|
| docs/research/REQUIREMENTS_3D_AVATAR_SIGN_LANG_LINGUISTICS.md | panini/specs/avatar/sign_avatar_requirements.md | Spec (domain) | panini | P1 |
| discoveries/baby-sign-validation/ | panini/discoveries/baby_sign_validation/ | Discovery | panini | P1 |
| discoveries/dhatu-universals/ | panini/discoveries/dhatu_universals/ | Discovery | panini | P1 |
| methodology/protocols/ | panini/methodology/protocols/ | Methodology | panini | P1 |
| publications/articles/ | panini/publications/articles/ | Publications | panini | P1 |
| publications/books/ | panini/publications/books/ | Publications | panini | P1 |
| research/dhatu/ | panini/data/dhatu/ | Raw dataset | panini | P2 |
| handshapes_preset.v0.1.json | panini/data/sign/handshapes_preset_v0_1.json (source) & tech/data/presets/handshapes_preset.v0.1.json (runtime) | Data split | both | P2 |
| nmf_rules.v0.1.json | panini/data/sign/nmf_rules_v0_1.json & tech/data/presets/nmf_rules.v0.1.json | Data split | both | P2 |
| interactive-validator/ | tech/apps/validator/ | App | tech | P1 |
| universal-sign-dhatu-interface.html | tech/apps/demos/universal_sign_interface.html | Demo | tech | P2 |
| lsq-advanced-hands.html | tech/apps/demos/lsq_advanced_hands.html | Demo | tech | P2 |
| lsq-hands-pro-system.html | tech/apps/demos/lsq_hands_pro_system.html | Demo | tech | P2 |
| navigation-test.html | tech/apps/demos/navigation_test.html | Demo | tech | P2 |
| hub.html | tech/apps/demos/hub.html | Demo | tech | P2 |
| test-*.js | tech/tests/js/ | Tests | tech | P1 |
| test_functional*.py | tech/tests/py/ | Tests | tech | P1 |
| validate.py | tech/tests/py/validate.py | Tests | tech | P1 |
| validate_navigation*.py | tech/tests/py/ | Tests | tech | P1 |
| scripts/generate_cache_hashes.py | tech/scripts/maintenance/generate_cache_hashes.py | Script | tech | P1 |
| three.min.js | tech/assets/vendor/three.min.js | Vendor | tech | P2 |
| GLTFLoader.js | tech/assets/vendor/GLTFLoader.js | Vendor | tech | P2 |
| dat.gui.min.js | tech/assets/vendor/dat.gui.min.js | Vendor | tech | P2 |
| CesiumMan.glb | tech/assets/models/CesiumMan.glb | Model | tech | P1 |
| RiggedFigure.glb | tech/assets/models/RiggedFigure.glb | Model | tech | P1 |
| RiggedSimple.glb | tech/assets/models/RiggedSimple.glb | Model | tech | P1 |
| debug-*.png | tech/assets/images/debug/ | Images | tech | P2 |
| error-*.png | tech/assets/images/errors/ | Images | tech | P2 |
| test-error.png | tech/assets/images/errors/test_error.png | Images | tech | P2 |
| validate-universal-interface.sh | tech/scripts/validation/validate_universal_interface.sh | Script | tech | P1 |
| REGLES_COPILOTAGE.md | tech/docs/governance/copilot_rules.md | Governance | tech | P3 |
| RAPPORT_TESTS_COMPLET.md | tech/docs/reports/tests_full_report.md | Report | tech | P3 |
| VALIDATION_STATUS.md | tech/docs/reports/validation_status.md | Report | tech | P3 |
| FREE_COMPUTE_STRATEGY.md | panini/roadmap/compute_strategy.md | Strategy | panini | P3 |
| GUIDE_DEPLOIEMENT_LSQ_FINAL.md | tech/docs/operations/lsq_deployment_guide.md | Operations | tech | P2 |
| GUIDE_MAINS_ARTICULEES_AVANCEES.md | panini/specs/hands/advanced_articulated_hands_guide.md | Spec detail | panini | P2 |
| README_NAVIGATION.md | tech/docs/navigation.md | Navigation | tech | P1 |

## 4. Phases
- P1: Core specs & models & validator app & tests & critical scripts.
- P2: Demos, vendor libs, detailed guides, dataset split (source vs runtime), deployment guide.
- P3: Reports, governance docs, strategy, image organization, cleanup.
- P4: Remove old empty dirs, update references, enforce path checks.

## 5. Conventions
| Aspect | Rule |
|--------|------|
| Directories | snake_case lowercase |
| Specs filenames | <topic>_requirements.md or <topic>_spec.md |
| Versioned JSON (domain source) | name_v<major>_<minor>.json |
| Runtime JSON (tech derived) | name.v<major>.<minor>.json |
| Models | <module>_rig_v<major>.<minor>.glb |
| Reports | <date>_<topic>_report.md (ISO date optional) |
| Scripts | verb_object.py / validate_<area>.py |

## 6. Validation Checklist Before Each Phase
- All moved files referenced in README / scripts updated.
- Tests pass (tech/tests) after path changes.
- No orphan large binaries >10MB left outside target axes.
- Git diff free of accidental deletions (only renames/moves).

## 7. Rollback Strategy
- If failure mid-phase: revert branch to previous commit (no partial manual undo).
- Keep branch `migration/dual-axis` until full completion and review.

## 8. Outstanding Decisions
- Whether to separate panini/publications vs root publications (decided: consolidate under panini/).
- Introduce `shared/` later; currently not created.
- Potential schema generation pipeline location (likely tech/scripts/build/).

## 9. Execution Log
### Phase P1 (Completed 2025-09-10 UTC)
Scope executed:
- Discoveries: baby_sign_validation, dhatu_universals relocated to `panini/discoveries/`
- Methodology protocols relocated to `panini/methodology/protocols/`
- Publications (articles, books) flattened & relocated to `panini/publications/`
- Validator app relocated to `tech/apps/validator/`
- JS tests relocated to `tech/tests/js/`
- Python tests relocated to `tech/tests/py/`
- 3D model assets relocated to `tech/assets/models/`
- Critical scripts (hash generator, validation script) relocated to `tech/scripts/`
- Navigation doc relocated to `tech/docs/navigation.md`
Validation summary:
- Structural moves staged & committed under single commit `chore(migration): Phase P1 ...`
- No vendor libs / demos moved yet (reserved for P2)
- Next: Phase P2 (demos, vendor libs, dataset source/runtime split, guides)

Pending items for P2 start conditions:
1. Update internal relative paths in any scripts referencing old test or model locations (TBD after initial test run)
2. Introduce `tech/assets/vendor/` and move three.min.js, GLTFLoader.js, dat.gui.min.js
3. Split handshape & nmf rules JSON (source vs runtime)
4. Relocate demo HTML pages into `tech/apps/demos/`
5. Prepare data provenance notes for moved JSON assets

Phase P3 & P4 remain unchanged.

### Phase P2 (In Progress 2025-09-10 UTC)
Scope executed so far:
- Demos & prototypes relocated to `tech/apps/demos/` with archive subset in `tech/apps/demos/archive/` and snake_case normalization.
- Vendor libraries moved to `tech/assets/vendor/` (`three.min.js`, `dat.gui.min.js`, `GLTFLoader.js`).
- Raw dhatu dataset directory moved to `panini/data/dhatu/` (if present).
- Data source/runtime split implemented for `handshapes_preset` and `nmf_rules` JSON (source in `panini/data/sign/`, runtime copies in `tech/data/presets/`).
- Path references in demo HTML updated to new vendor relative paths and legacy root references removed.
- Added structural validation script `tech/scripts/validation/verify_layout.sh`.

Pending P2 actions:
1. Migrate guides (`GUIDE_DEPLOIEMENT_LSQ_FINAL.md` -> `tech/docs/operations/lsq_deployment_guide.md`; `GUIDE_MAINS_ARTICULEES_AVANCEES.md` -> `panini/specs/hands/advanced_articulated_hands_guide.md`).
2. Relocate debug/error images into `tech/assets/images/{debug,errors}/` and update mapping table.
3. Run verification script and test suites post-image moves.
4. Finalize mapping table additions for P2 then mark Phase P2 completed.

Validation to date:
- Grep confirms no remaining direct `<script src="three.min.js">` in demos; all use relative vendor path.
- JSON files absent from legacy root/data path after move (runtime duplicates present).
- Layout script passes (manual invocation pending commit stage).

Risks / Watch:
- Duplicate untracked test JS/Py files at repository root not yet moved to `tech/tests/`; evaluate before closing P2.
- Ensure GLTFLoader usage still resolved via relative path (may need `<script src="../../assets/vendor/GLTFLoader.js"></script>` where applicable—double-check in non-edited demos).

Next Gate Criteria (to close P2):
- All guides & images relocated.
- Root-level test files either migrated or intentionally retained with rationale documented.
- `verify_layout.sh` exits 0 in CI context.
- Updated status changed to Phase P2 COMPLETED with timestamp.

---
(End of plan)
