#!/usr/bin/env python3
"""
Launcher Intelligent pour Validation PaniniFS Research
Choisit automatiquement entre Playwright et version basique
"""

import subprocess
import sys
import os

def check_playwright_available():
    """Vérifie si Playwright est disponible et fonctionnel"""
    try:
        result = subprocess.run([
            "python3", "-c", "from playwright.async_api import async_playwright; print('OK')"
        ], capture_output=True, text=True, timeout=10)
        return result.returncode == 0 and "OK" in result.stdout
    except:
        return False

def main():
    print("🚀 PaniniFS Research - Validation Automatique Intelligente")
    print("=" * 60)
    
    # Vérification de Playwright
    print("🔍 Vérification de la disponibilité de Playwright...")
    
    if check_playwright_available():
        print("✅ Playwright disponible - Utilisation de la validation complète")
        script = "validate_navigation.py"
    else:
        print("⚠️  Playwright indisponible - Utilisation de la validation basique")
        script = "validate_navigation_basic.py"
    
    print(f"📋 Exécution de: {script}")
    print("-" * 60)
    
    # Exécution du script approprié
    try:
        result = subprocess.run([
            "python3", script
        ], cwd=os.getcwd())
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrompue par l'utilisateur")
        return 3
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return 4

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
