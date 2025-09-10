#!/bin/bash

# Script pour lancer le prototype PaniniGraph dans Firefox
# Usage: ./launch_firefox.sh

echo "🌍 Lancement du prototype PaniniGraph dans Firefox..."
echo "📁 Fichier: $(realpath language/prototype_paninigraph.html)"
echo ""

# Vérifier que Firefox est installé
if ! command -v firefox &> /dev/null; then
    echo "❌ Firefox n'est pas installé ou introuvable"
    echo "💡 Installation: sudo apt install firefox"
    exit 1
fi

# Lancer Firefox avec le prototype
firefox "file://$(realpath language/prototype_paninigraph.html)" &

echo "✅ Firefox lancé avec le prototype PaniniGraph"
echo "🎯 Interface prête pour les tests d'écriture non-linéaire !"
echo ""
echo "📋 Instructions rapides:"
echo "   1. Cliquez sur les émojis primitives (🤲 ➡️ 🤝 etc.)"
echo "   2. Utilisez '📏 Linéariser' pour voir l'animation"
echo "   3. Testez '🎭 Démo' pour un exemple complet"
echo "   4. '🔊 Prononcer' pour entendre les phonèmes"
echo ""
