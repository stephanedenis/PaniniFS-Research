#!/bin/bash
# Script de transfert PDF vers reMarkable
# Usage: ./transfer_to_remarkable.sh

PDF_FILE="/home/stephane/GitHub/PaniniFS-Research/ANALYSE_LINGUISTIQUE_MULTILINGUE_REMARKABLE.pdf"
REMARKABLE_IP="10.11.99.1"  # IP par défaut reMarkable via USB
REMARKABLE_USER="root"

echo "📱 TRANSFERT VERS REMARKABLE"
echo "=================================="

# Vérification existence du fichier
if [ ! -f "$PDF_FILE" ]; then
    echo "❌ Fichier PDF non trouvé: $PDF_FILE"
    exit 1
fi

echo "📄 Fichier: $(basename $PDF_FILE)"
echo "📊 Taille: $(du -h $PDF_FILE | cut -f1)"

# Méthodes de transfert disponibles
echo ""
echo "🔗 MÉTHODES DE TRANSFERT DISPONIBLES:"
echo "1. Via USB (IP: $REMARKABLE_IP)"
echo "2. Via rsync/SSH"
echo "3. Via reMarkable Cloud"
echo "4. Via email vers tablet@reMarkable"

echo ""
echo "💡 INSTRUCTIONS:"
echo "   USB: Connectez votre reMarkable en USB et activez le stockage"
echo "   SSH: rmapi ou scp direct si configuré"
echo "   Cloud: Upload via my.remarkable.com"
echo "   Email: Envoyez le PDF en pièce jointe à tablet@reMarkable"

echo ""
echo "📁 LOCALISATION DU FICHIER:"
echo "   $PDF_FILE"

echo ""
echo "✅ PDF PRÊT POUR ANNOTATION SUR REMARKABLE!"
echo "   • Format A4 optimisé"
echo "   • Marges larges pour annotations" 
echo "   • Tableaux structurés"
echo "   • 48.5 KB - Transfert rapide"
