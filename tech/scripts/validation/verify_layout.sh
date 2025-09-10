#!/usr/bin/env bash
set -euo pipefail

pass=true

check() {
  if [ "$1" = exists ]; then
    shift; for p in "$@"; do
      if [ ! -e "$p" ]; then echo "[MISSING] $p"; pass=false; fi
    done
  elif [ "$1" = absent ]; then
    shift; for p in "$@"; do
      if [ -e "$p" ]; then echo "[SHOULD_BE_REMOVED] $p"; pass=false; fi
    done
  fi
}

echo "Verifying required directories/files..."
check exists panini panini/data/sign tech/assets/vendor tech/apps/demos tech/assets/models
check exists tech/assets/vendor/three.min.js tech/assets/vendor/dat.gui.min.js || true
check exists panini/data/sign/handshapes_preset_v0_1.json panini/data/sign/nmf_rules_v0_1.json || true
check exists tech/data/presets/handshapes_preset.v0.1.json tech/data/presets/nmf_rules.v0.1.json || true
check exists tech/docs/operations/lsq_deployment_guide.md panini/specs/hands/advanced_articulated_hands_guide.md || true
check exists tech/assets/images/debug tech/assets/images/errors || true
check exists tech/tests/js tech/tests/py || true
check exists tech/docs/governance/copilot_rules.md tech/docs/reports/tests_full_report.md tech/docs/reports/validation_status.md panini/roadmap/compute_strategy.md || true

# Legacy locations that must be absent
check absent three.min.js dat.gui.min.js GLTFLoader.js handshapes_preset.v0.1.json nmf_rules.v0.1.json
check absent GUIDE_DEPLOIEMENT_LSQ_FINAL.md GUIDE_MAINS_ARTICULEES_AVANCEES.md test-real-3d-models.js test_functional.py test_functional_fixed.py || true
check absent REGLES_COPILOTAGE.md RAPPORT_TESTS_COMPLET.md VALIDATION_STATUS.md cloud-processing/FREE_COMPUTE_STRATEGY.md || true

if $pass; then
  echo "[OK] Layout verification passed"
  exit 0
else
  echo "[FAIL] Layout verification failed" >&2
  exit 1
fi
