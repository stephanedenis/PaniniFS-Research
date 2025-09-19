#!/bin/bash
# Script principal création projets GitHub dhātu
# Choisit automatiquement la meilleure méthode disponible

echo "🎯 Créateur de projets GitHub dhātu"
echo "===================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Fonction pour tester les permissions gh CLI
test_gh_permissions() {
    if command -v gh &> /dev/null; then
        echo "📱 GitHub CLI détecté, test des permissions..."
        if gh project list --owner stephanedenis &> /dev/null; then
            echo "✅ GitHub CLI configuré avec permissions projets"
            return 0
        else
            echo "⚠️  GitHub CLI sans permissions projets"
            return 1
        fi
    else
        echo "❌ GitHub CLI non installé"
        return 1
    fi
}

# Fonction pour tester token API
test_api_token() {
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "🔑 Token GitHub détecté, test de validité..."
        local response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                         https://api.github.com/user)
        if echo "$response" | jq -e '.login' &> /dev/null; then
            echo "✅ Token GitHub valide"
            return 0
        else
            echo "❌ Token GitHub invalide"
            return 1
        fi
    else
        echo "⚠️  Variable GITHUB_TOKEN non définie"
        return 1
    fi
}

echo "🔍 Détection méthode optimale..."
echo ""

# Test 1: GitHub CLI avec permissions
if test_gh_permissions; then
    echo ""
    echo "🚀 Utilisation GitHub CLI (méthode recommandée)"
    exec "$SCRIPT_DIR/create_projects_gh.sh"

# Test 2: API avec token
elif test_api_token; then
    echo ""
    echo "🚀 Utilisation API GitHub avec token"
    exec "$SCRIPT_DIR/create_projects_api.sh"

# Aucune méthode disponible - afficher instructions
else
    echo ""
    echo "🔧 Configuration requise"
    echo "========================"
    echo ""
    echo "Aucune méthode d'authentification disponible."
    echo "Choisissez une option:"
    echo ""
    echo "📱 Option 1: GitHub CLI (Recommandée)"
    echo "   1. Installer gh si nécessaire: sudo apt install gh"
    echo "   2. Authentifier: gh auth refresh -s project,read:project"
    echo "   3. Relancer ce script"
    echo ""
    echo "🔑 Option 2: Token API GitHub"
    echo "   1. Créer token: https://github.com/settings/tokens"
    echo "   2. Permissions: repo, project, read:project"
    echo "   3. Export: export GITHUB_TOKEN='votre_token'"
    echo "   4. Relancer ce script"
    echo ""
    echo "📚 Option 3: Création manuelle"
    echo "   Suivre le guide: scripts/GITHUB_PROJECTS_GUIDE.md"
    echo ""
    echo "🛠️  Scripts disponibles:"
    echo "   - scripts/setup_gh_auth.sh     # Guide auth GitHub CLI"
    echo "   - scripts/create_projects_gh.sh    # Via GitHub CLI"
    echo "   - scripts/create_projects_api.sh   # Via API REST"
    echo ""
    exit 1
fi