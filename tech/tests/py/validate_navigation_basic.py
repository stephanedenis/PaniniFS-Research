#!/usr/bin/env python3
"""
Validateur de Navigation PaniniFS Research - Version Basique
Mode fallback sans Playwright pour environnements avec contraintes
"""

import http.server
import socketserver
import subprocess
import time
import json
import sys
import os
import signal
import threading
from datetime import datetime
import urllib.request
import urllib.error
from pathlib import Path

class PaniniFSNavigationValidatorBasic:
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.server_process = None
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "validator_version": "1.0-basic",
            "test_results": [],
            "summary": {},
            "errors": []
        }
        self.success_count = 0
        self.total_tests = 0
        
    def log(self, message, level="INFO"):
        """Journalisation avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def start_server(self):
        """Démarre le serveur HTTP si nécessaire"""
        try:
            # Test si le serveur est déjà actif
            urllib.request.urlopen(f"{self.base_url}/hub.html", timeout=2)
            self.log("Serveur HTTP déjà actif sur le port 8081")
            return True
        except:
            self.log("Démarrage du serveur HTTP sur le port 8081...")
            
        # Démarrage du serveur en arrière-plan
        try:
            self.server_process = subprocess.Popen([
                "python3", "-m", "http.server", "8081"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Attendre que le serveur soit prêt
            for _ in range(10):
                time.sleep(1)
                try:
                    urllib.request.urlopen(f"{self.base_url}/hub.html", timeout=2)
                    self.log("✅ Serveur HTTP démarré avec succès")
                    return True
                except:
                    continue
                    
            self.log("❌ Échec du démarrage du serveur")
            return False
            
        except Exception as e:
            self.log(f"❌ Erreur lors du démarrage du serveur: {e}", "ERROR")
            return False
    
    def stop_server(self):
        """Arrête le serveur HTTP"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            self.log("Serveur HTTP arrêté")
    
    def test_url_accessibility(self, url, expected_content=None):
        """Test basique d'accessibilité d'une URL"""
        test_name = f"Accessibilité: {url}"
        self.total_tests += 1
        
        try:
            start_time = time.time()
            response = urllib.request.urlopen(url, timeout=10)
            load_time = time.time() - start_time
            
            if response.status == 200:
                content = response.read().decode('utf-8')
                
                # Vérification du contenu si spécifié
                content_ok = True
                if expected_content:
                    for expected in expected_content:
                        if expected not in content:
                            content_ok = False
                            break
                
                if content_ok:
                    self.log(f"✅ {test_name} - OK ({load_time:.2f}s)")
                    self.success_count += 1
                    self.report["test_results"].append({
                        "test": test_name,
                        "status": "PASS",
                        "load_time": load_time,
                        "details": f"Chargé en {load_time:.2f}s"
                    })
                    return True
                else:
                    self.log(f"❌ {test_name} - Contenu manquant")
                    self.report["test_results"].append({
                        "test": test_name,
                        "status": "FAIL",
                        "error": "Contenu attendu manquant"
                    })
                    return False
            else:
                self.log(f"❌ {test_name} - Status {response.status}")
                self.report["test_results"].append({
                    "test": test_name,
                    "status": "FAIL",
                    "error": f"HTTP {response.status}"
                })
                return False
                
        except Exception as e:
            self.log(f"❌ {test_name} - Erreur: {e}")
            self.report["test_results"].append({
                "test": test_name,
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_validation_tests(self):
        """Exécute tous les tests de validation"""
        self.log("🚀 Début de la validation automatique PaniniFS")
        
        # Test 1: Hub Principal
        self.log("\n📋 Test 1: Hub Principal")
        self.test_url_accessibility(
            f"{self.base_url}/hub.html",
            ["PaniniFS Research Hub", "Validateur Interactif", "access-card"]
        )
        
        # Test 2: Validateur Interactif
        self.log("\n📋 Test 2: Validateur Interactif")
        self.test_url_accessibility(
            f"{self.base_url}/interactive-validator/",
            ["PaniniFS Research", "dhatu-grid", "nav-tabs"]
        )
        
        # Test 3: Galerie Gestes
        self.log("\n📋 Test 3: Galerie des Gestes")
        self.test_url_accessibility(
            f"{self.base_url}/interactive-validator/gesture-gallery.html",
            ["Galerie des Gestes", "gesture-showcase"]
        )
        
        # Test 4: Tests Techniques
        self.log("\n📋 Test 4: Tests Techniques")
        self.test_url_accessibility(
            f"{self.base_url}/interactive-validator/test-gestures.html",
            ["Test des Gestes", "gesture-grid"]
        )
        
        # Test 5: Navigation Test
        self.log("\n📋 Test 5: Outil de Navigation")
        self.test_url_accessibility(
            f"{self.base_url}/navigation-test.html",
            ["Test de Navigation", "test-results"]
        )
        
        # Test 6: Accès Racine
        self.log("\n📋 Test 6: Accès Racine")
        self.test_url_accessibility(f"{self.base_url}/")
        
    def check_file_structure(self):
        """Vérifie la structure des fichiers"""
        self.log("\n📂 Vérification de la structure des fichiers")
        
        required_files = [
            "hub.html",
            "navigation-test.html",
            "interactive-validator/index.html",
            "interactive-validator/app.js",
            "interactive-validator/dhatu-data.js",
            "interactive-validator/enhanced-baby-sign-gestures.js",
            "interactive-validator/gesture-gallery.html",
            "interactive-validator/test-gestures.html"
        ]
        
        for file_path in required_files:
            full_path = Path(file_path)
            if full_path.exists():
                self.log(f"✅ {file_path}")
                self.success_count += 1
            else:
                self.log(f"❌ {file_path} - MANQUANT")
                self.report["errors"].append(f"Fichier manquant: {file_path}")
            
            self.total_tests += 1
    
    def generate_report(self):
        """Génère le rapport final"""
        success_rate = (self.success_count / self.total_tests * 100) if self.total_tests > 0 else 0
        
        self.report["summary"] = {
            "total_tests": self.total_tests,
            "successful_tests": self.success_count,
            "failed_tests": self.total_tests - self.success_count,
            "success_rate": round(success_rate, 2),
            "validation_passed": success_rate >= 90
        }
        
        # Sauvegarde du rapport
        report_file = f"/tmp/paniniFS_validation_report_basic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        # Affichage du résumé
        self.log("\n" + "="*60)
        self.log("📊 RAPPORT DE VALIDATION PANINIFW")
        self.log("="*60)
        self.log(f"Tests exécutés: {self.total_tests}")
        self.log(f"Tests réussis: {self.success_count}")
        self.log(f"Tests échoués: {self.total_tests - self.success_count}")
        self.log(f"Taux de réussite: {success_rate:.1f}%")
        self.log(f"Rapport sauvegardé: {report_file}")
        
        if success_rate >= 90:
            self.log("🎉 VALIDATION RÉUSSIE - Livrable approuvé!", "SUCCESS")
            return 0
        else:
            self.log("🚨 VALIDATION ÉCHOUÉE - Corrections requises!", "ERROR")
            return 1
    
    def handle_interrupt(self, signum, frame):
        """Gestion de l'interruption clavier"""
        self.log("\n⚠️ Interruption détectée - Arrêt propre...")
        self.stop_server()
        sys.exit(3)

def main():
    validator = PaniniFSNavigationValidatorBasic()
    
    # Gestion de l'interruption clavier
    signal.signal(signal.SIGINT, validator.handle_interrupt)
    
    try:
        # Démarrage du serveur
        if not validator.start_server():
            return 2
        
        # Vérification de la structure des fichiers
        validator.check_file_structure()
        
        # Exécution des tests de validation
        validator.run_validation_tests()
        
        # Génération du rapport
        exit_code = validator.generate_report()
        
        return exit_code
        
    except Exception as e:
        validator.log(f"❌ Erreur inattendue: {e}", "ERROR")
        return 4
    finally:
        validator.stop_server()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
