#!/bin/bash
# Script de diagnostic RX 480 pour openSUSE
# Créé le 19 Septembre 2025

echo "🔺 DIAGNOSTIC RX 480 - DRIVERS OPENSUSE"
echo "========================================"

echo -e "\n📊 1. DETECTION HARDWARE:"
echo "------------------------"
echo "GPUs détectés:"
lspci | grep VGA

echo -e "\nRecherche RX 480 (PCI ID 1002:67df):"
lspci -nn | grep 1002:67df
if [ $? -eq 0 ]; then
    echo "✅ RX 480 DÉTECTÉE !"
else
    echo "❌ RX 480 non détectée - vérifier installation physique"
fi

echo -e "\n📊 2. DRIVERS CHARGÉS:"
echo "---------------------"
echo "Modules GPU actifs:"
lsmod | grep -E "(radeon|amdgpu)"

echo -e "\n📊 3. FIRMWARE AMDGPU:"
echo "---------------------"
zypper info kernel-firmware-amdgpu | grep -E "(Version|Status)"

echo -e "\n📊 4. MESA OPENGL:"
echo "-----------------"
zypper info Mesa | grep -E "(Version|Status)"

echo -e "\n📊 5. DRIVER X11:"
echo "----------------"
zypper info xf86-video-amdgpu | grep -E "(Version|Status)" 2>/dev/null || echo "xf86-video-amdgpu non installé"

echo -e "\n📊 6. CONFIGURATION SYSTÈME:"
echo "----------------------------"
echo "Configuration amdgpu:"
cat /etc/modprobe.d/amdgpu-rx480.conf 2>/dev/null || echo "Configuration amdgpu non trouvée"

echo -e "\nBlacklist radeon:"
cat /etc/modprobe.d/blacklist-radeon-rx480.conf 2>/dev/null || echo "Blacklist radeon non configuré"

echo -e "\n📊 7. OPENGL STATUS:"
echo "------------------"
if command -v glxinfo >/dev/null 2>&1; then
    echo "OpenGL Vendor: $(glxinfo | grep "OpenGL vendor" | cut -d: -f2-)"
    echo "OpenGL Renderer: $(glxinfo | grep "OpenGL renderer" | cut -d: -f2-)"
    echo "OpenGL Version: $(glxinfo | grep "OpenGL version" | cut -d: -f2-)"
else
    echo "glxinfo non disponible - installer mesa-demos"
fi

echo -e "\n🎯 RECOMMANDATIONS:"
echo "------------------"
if ! lspci -nn | grep -q 1002:67df; then
    echo "❌ RX 480 non détectée:"
    echo "   1. Vérifier installation physique"
    echo "   2. Redémarrer le système"
    echo "   3. Vérifier alimentation 8-pin"
fi

if lsmod | grep -q radeon; then
    echo "⚠️  Driver radeon encore actif:"
    echo "   Redémarrage requis pour activer configuration"
fi

if lspci -nn | grep -q 1002:67df && lsmod | grep -q amdgpu; then
    echo "✅ RX 480 détectée avec driver amdgpu - Configuration OK !"
fi

echo -e "\n🔺 Diagnostic terminé"