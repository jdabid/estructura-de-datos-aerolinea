#!/usr/bin/env bash
# Validates kustomize build for all environments
set -euo pipefail

ENVIRONMENTS=("dev" "staging" "prod")
BASE_DIR="infra/kustomize"
ERRORS=0

echo "=== Validando Kustomize builds ==="

# Validate base
echo -n "  base... "
if kubectl kustomize "$BASE_DIR/base/" > /dev/null 2>&1; then
    echo "OK"
else
    echo "FAIL"
    ERRORS=$((ERRORS + 1))
fi

# Validate each overlay
for env in "${ENVIRONMENTS[@]}"; do
    echo -n "  $env... "
    if kubectl kustomize "$BASE_DIR/overlays/$env/" > /dev/null 2>&1; then
        echo "OK"
    else
        echo "FAIL"
        ERRORS=$((ERRORS + 1))
    fi
done

# Summary
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "All kustomize builds passed!"
    exit 0
else
    echo "$ERRORS build(s) failed."
    exit 1
fi
