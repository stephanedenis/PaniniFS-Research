#!/bin/bash

# Script pour configurer le copilotage avec sous-module partagé
# Auteur: GitHub Copilot
# Date: $(date)

set -e  # Arrêter le script en cas d'erreur

echo "🚀 Configuration du système de copilotage..."

# Étape 1: Copier le dossier copilotage depuis ../PaniniFS/
echo "📁 Copie du dossier copilotage depuis ../PaniniFS/..."

if [ -d "../PaniniFS/copilotage" ]; then
    # Créer le dossier copilotage s'il n'existe pas
    if [ ! -d "copilotage" ]; then
        mkdir -p copilotage
        echo "✅ Dossier copilotage créé"
    else
        echo "⚠️  Le dossier copilotage existe déjà"
    fi
    
    # Copier le contenu (exclure le dossier shared s'il existe)
    echo "📋 Copie des fichiers..."
    cp -r ../PaniniFS/copilotage/* copilotage/ 2>/dev/null || true
    
    # Supprimer le dossier shared local s'il a été copié (on va le remplacer par le sous-module)
    if [ -d "copilotage/shared" ]; then
        rm -rf copilotage/shared
        echo "🗑️  Dossier shared local supprimé (sera remplacé par le sous-module)"
    fi
    
    echo "✅ Copie terminée"
else
    echo "❌ Erreur: Le dossier ../PaniniFS/copilotage n'existe pas"
    exit 1
fi

# Étape 2: Configurer le sous-module Git
echo "🔗 Configuration du sous-module Git..."

# Vérifier si on est dans un repository Git
if [ ! -d ".git" ]; then
    echo "❌ Erreur: Ce répertoire n'est pas un repository Git"
    exit 1
fi

# Ajouter le sous-module PaniniFS-CopilotageShared
echo "📦 Ajout du sous-module PaniniFS-CopilotageShared..."

if [ -d "copilotage/shared" ]; then
    echo "⚠️  Le sous-module existe déjà, suppression..."
    git submodule deinit -f copilotage/shared 2>/dev/null || true
    rm -rf copilotage/shared
    git rm -f copilotage/shared 2>/dev/null || true
fi

# Ajouter le nouveau sous-module
git submodule add https://github.com/stephanedenis/PaniniFS-CopilotageShared.git copilotage/shared

echo "🔄 Initialisation et mise à jour du sous-module..."
git submodule update --init --recursive

# Étape 3: Vérification finale
echo "🔍 Vérification de la configuration..."

if [ -d "copilotage" ] && [ -d "copilotage/shared" ]; then
    echo "✅ Configuration réussie !"
    echo ""
    echo "📊 Structure créée:"
    echo "copilotage/"
    echo "├── config.yml"
    echo "├── README.md"
    echo "└── shared/ (sous-module Git)"
    echo ""
    echo "🎯 Prochaines étapes:"
    echo "1. Commitez les changements: git add . && git commit -m 'Add copilotage setup with shared submodule'"
    echo "2. Vérifiez le contenu: ls -la copilotage/"
    echo "3. Testez le sous-module: cd copilotage/shared && git status"
else
    echo "❌ Erreur lors de la configuration"
    exit 1
fi

echo ""
echo "🎉 Script terminé avec succès !"
