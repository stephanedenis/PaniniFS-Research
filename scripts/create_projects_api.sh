#!/bin/bash
# Alternative: Création projets via API GitHub avec curl
# Utilise votre configuration SSH existante

echo "🔗 Création projets GitHub dhātu via API REST"
echo "=============================================="
echo ""

# Instructions pour obtenir un token GitHub
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  Variable GITHUB_TOKEN non définie"
    echo ""
    echo "📋 Instructions pour obtenir un token:"
    echo "1. Aller sur: https://github.com/settings/tokens"
    echo "2. Cliquer 'Generate new token (classic)'"
    echo "3. Sélectionner permissions:"
    echo "   - repo (Full control of private repositories)"
    echo "   - project (Full control of projects)"
    echo "4. Copier le token généré"
    echo "5. Exporter: export GITHUB_TOKEN='ghp_votre_token_ici'"
    echo "6. Relancer ce script"
    echo ""
    exit 1
fi

# Configuration
REPO_OWNER="stephanedenis"
REPO_NAME="PaniniFS-Research"
API_BASE="https://api.github.com"

# Headers pour l'API
AUTH_HEADER="Authorization: token $GITHUB_TOKEN"
ACCEPT_HEADER="Accept: application/vnd.github.v3+json"

# Function pour créer un projet
create_project() {
    local category="$1"
    local name="$2"
    local description="$3"
    
    echo ""
    echo "🚀 Création: [$category] $name"
    
    # JSON payload
    local json_data=$(cat <<EOF
{
  "name": "[$category] $name",
  "body": "$description",
  "state": "open"
}
EOF
)
    
    # Créer le projet
    local response=$(curl -s -X POST \
        -H "$AUTH_HEADER" \
        -H "$ACCEPT_HEADER" \
        -H "Content-Type: application/json" \
        -d "$json_data" \
        "$API_BASE/repos/$REPO_OWNER/$REPO_NAME/projects")
    
    # Vérifier le résultat
    local project_url=$(echo "$response" | jq -r '.html_url // empty')
    
    if [ -n "$project_url" ]; then
        echo "✅ Projet créé: $project_url"
        
        # Extraire l'ID du projet pour créer les colonnes
        local project_id=$(echo "$response" | jq -r '.id // empty')
        
        if [ -n "$project_id" ]; then
            create_columns "$project_id"
        fi
    else
        echo "❌ Erreur création projet:"
        echo "$response" | jq .
    fi
}

# Function pour créer les colonnes d'un projet
create_columns() {
    local project_id="$1"
    local columns=("📋 Backlog" "🏗️ In Progress" "🧪 Testing" "✅ Done")
    
    for column in "${columns[@]}"; do
        local column_json=$(cat <<EOF
{
  "name": "$column"
}
EOF
)
        
        local col_response=$(curl -s -X POST \
            -H "$AUTH_HEADER" \
            -H "$ACCEPT_HEADER" \
            -H "Content-Type: application/json" \
            -d "$column_json" \
            "$API_BASE/projects/$project_id/columns")
        
        local col_name=$(echo "$col_response" | jq -r '.name // empty')
        if [ -n "$col_name" ]; then
            echo "  📋 Colonne créée: $col_name"
        else
            echo "  ❌ Erreur colonne: $column"
        fi
    done
}

# Vérifier que jq est installé
if ! command -v jq &> /dev/null; then
    echo "❌ 'jq' non installé. Installation:"
    echo "   sudo apt install jq"
    exit 1
fi

echo "🔧 Token configuré, création des projets..."

# 🔧 CORE PROJECTS
echo ""
echo "🔧 === CORE PROJECTS ==="

create_project "CORE" "dhatu-universal-compressor" \
    "🧠 Système compression sémantique universelle dhātu - 100% reconstruction garantie"

create_project "CORE" "dhatu-corpus-manager" \
    "📚 Gestionnaire corpus multilingue - Collection autonome Gutenberg/ArXiv/HAL"

create_project "CORE" "dhatu-web-framework" \
    "🌐 Framework web dhātu-natif - Dashboard temps réel + APIs"

create_project "CORE" "dhatu-gpu-accelerator" \
    "⚡ Accélération GPU optimisée - Performance dhātu hardware"

# 🛠️ TOOLS PROJECTS
echo ""
echo "🛠️ === TOOLS PROJECTS ==="

create_project "TOOLS" "dhatu-pattern-analyzer" \
    "🔍 Analyse patterns sémantiques émergents - Corrélations dhātu"

create_project "TOOLS" "dhatu-creative-generator" \
    "🎨 Génération créative assistée - Innovation dhātu-guidée"

create_project "TOOLS" "dhatu-space-visualizer" \
    "🌌 Visualisation espaces multidimensionnels - Géométrie dhātu"

create_project "TOOLS" "dhatu-evolution-simulator" \
    "🧬 Simulation évolution linguistique - Dynamiques dhātu"

# 🚪 INTERFACES PROJECTS
echo ""
echo "🚪 === INTERFACES PROJECTS ==="

create_project "INTERFACES" "dhatu-dashboard" \
    "📊 Interface monitoring temps réel - UX dhātu responsive"

create_project "INTERFACES" "dhatu-api-gateway" \
    "🚪 Passerelle API unifiée - Microservices dhātu"

# 🔬 RESEARCH PROJECTS
echo ""
echo "🔬 === RESEARCH PROJECTS ==="

create_project "RESEARCH" "dhatu-linguistics-engine" \
    "🔬 Moteur analyse linguistique computationnelle - Théorie dhātu"

create_project "RESEARCH" "dhatu-multimodal-learning" \
    "🎭 Apprentissage multimodal dhātu - Gestuel + vocal + cognitif"

echo ""
echo "=============================================="
echo "🎉 Création des projets GitHub dhātu terminée!"
echo ""
echo "🔗 Voir les projets:"
echo "   https://github.com/$REPO_OWNER/$REPO_NAME/projects"
echo ""