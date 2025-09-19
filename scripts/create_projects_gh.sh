#!/bin/bash
# Script création projets GitHub dhātu avec GitHub CLI (gh)
# Plus simple et direct que l'API REST

set -e  # Arrêter en cas d'erreur

echo "🎯 Création projets GitHub dhātu avec gh CLI"
echo "=============================================="

# Repository info
REPO="stephanedenis/PaniniFS-Research"

# Function pour créer un projet
create_project() {
    local category="$1"
    local name="$2"
    local description="$3"
    
    echo ""
    echo "🚀 Création: [$category] $name"
    echo "📝 Description: $description"
    
    # Créer le projet avec gh
    if gh project create --repo "$REPO" --title "[$category] $name" --body "$description"; then
        echo "✅ Projet créé avec succès!"
    else
        echo "❌ Erreur lors de la création"
        return 1
    fi
}

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
echo "   https://github.com/$REPO/projects"
echo ""
echo "📋 Prochaines étapes:"
echo "   1. Configurer les colonnes de chaque projet"
echo "   2. Ajouter les issues initiales"
echo "   3. Lier avec la documentation /projects/"
echo ""