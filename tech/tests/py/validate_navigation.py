#!/usr/bin/env python3
"""
PaniniFS Navigation Validator - Playwright Automation
Validation automatique de tous les liens et interfaces web
Stratégie obligatoire pour assurer la qualité des livrables
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess
import time
import os

class PaniniFSNavigationValidator:
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.server_process = None
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "server_status": "unknown",
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_results": [],
            "screenshots": [],
            "performance_metrics": {}
        }
        
        # Définition des tests obligatoires
        self.mandatory_tests = [
            {
                "name": "Hub Principal",
                "url": "/hub.html",
                "required_elements": [".hub-container", ".access-grid", ".access-card"],
                "required_text": ["PaniniFS Research Hub", "Validateur Interactif"],
                "category": "navigation"
            },
            {
                "name": "Validateur Interactif",
                "url": "/interactive-validator/",
                "required_elements": [".app-container", ".nav-tabs", ".dhatu-grid"],
                "required_text": ["PaniniFS Research", "Dhātu"],
                "category": "application"
            },
            {
                "name": "Galerie Gestes Anatomiques",
                "url": "/interactive-validator/gesture-gallery.html",
                "required_elements": [".gesture-gallery", ".gesture-showcase"],
                "required_text": ["Galerie des Gestes", "Anatomiques"],
                "category": "visualization"
            },
            {
                "name": "Test Technique Gestes",
                "url": "/interactive-validator/test-gestures.html",
                "required_elements": [".gesture-grid", ".controls"],
                "required_text": ["Test des Gestes", "Baby Sign"],
                "category": "testing"
            },
            {
                "name": "Documents Production",
                "url": "/production/documents/",
                "required_elements": ["body"],
                "required_text": ["Index of", "documents"],
                "category": "documentation"
            },
            {
                "name": "Page Test Navigation",
                "url": "/navigation-test.html",
                "required_elements": [".test-grid", ".test-link"],
                "required_text": ["Test de Navigation", "PaniniFS"],
                "category": "testing"
            }
        ]

    async def start_server(self):
        """Démarrer le serveur HTTP local si nécessaire"""
        try:
            # Vérifier si le serveur tourne déjà
            import requests
            response = requests.get(f"{self.base_url}", timeout=2)
            if response.status_code == 200:
                self.results["server_status"] = "already_running"
                print("✅ Serveur HTTP déjà en cours d'exécution")
                return True
        except:
            pass
        
        # Démarrer le serveur
        print("🚀 Démarrage du serveur HTTP...")
        try:
            self.server_process = subprocess.Popen(
                ["python3", "-m", "http.server", "8081"],
                cwd="/home/stephane/GitHub/PaniniFS-Research",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Attendre que le serveur démarre
            time.sleep(3)
            
            # Vérifier que le serveur répond
            import requests
            response = requests.get(f"{self.base_url}", timeout=5)
            if response.status_code == 200:
                self.results["server_status"] = "started"
                print("✅ Serveur HTTP démarré avec succès")
                return True
            else:
                raise Exception(f"Serveur ne répond pas: {response.status_code}")
                
        except Exception as e:
            self.results["server_status"] = f"failed: {str(e)}"
            print(f"❌ Erreur démarrage serveur: {e}")
            return False

    async def stop_server(self):
        """Arrêter le serveur HTTP"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("🛑 Serveur HTTP arrêté")

    async def validate_page(self, browser, test_config):
        """Valider une page spécifique"""
        page = await browser.new_page()
        test_result = {
            "name": test_config["name"],
            "url": test_config["url"],
            "category": test_config["category"],
            "status": "unknown",
            "errors": [],
            "performance": {},
            "screenshot": None
        }
        
        try:
            print(f"🔍 Test: {test_config['name']} ({test_config['url']})")
            
            # Navigation avec timeout
            full_url = f"{self.base_url}{test_config['url']}"
            start_time = time.time()
            
            response = await page.goto(full_url, wait_until="domcontentloaded", timeout=10000)
            load_time = time.time() - start_time
            
            test_result["performance"]["load_time"] = load_time
            test_result["performance"]["status_code"] = response.status
            
            # Vérifier le statut HTTP
            if response.status != 200:
                test_result["errors"].append(f"HTTP {response.status}")
                test_result["status"] = "failed"
                return test_result
            
            # Attendre le contenu
            await page.wait_for_load_state("networkidle", timeout=5000)
            
            # Vérifier les éléments requis
            for element in test_config["required_elements"]:
                try:
                    await page.wait_for_selector(element, timeout=3000)
                    print(f"  ✅ Élément trouvé: {element}")
                except:
                    test_result["errors"].append(f"Élément manquant: {element}")
                    print(f"  ❌ Élément manquant: {element}")
            
            # Vérifier le texte requis
            page_content = await page.content()
            for text in test_config["required_text"]:
                if text in page_content:
                    print(f"  ✅ Texte trouvé: {text}")
                else:
                    test_result["errors"].append(f"Texte manquant: {text}")
                    print(f"  ❌ Texte manquant: {text}")
            
            # Capture d'écran
            screenshot_path = f"/tmp/paniniFS_screenshot_{test_config['name'].replace(' ', '_')}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            test_result["screenshot"] = screenshot_path
            self.results["screenshots"].append(screenshot_path)
            
            # Métriques de performance
            performance = await page.evaluate("""
                () => {
                    const navigation = performance.getEntriesByType('navigation')[0];
                    return {
                        dom_content_loaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                        load_complete: navigation.loadEventEnd - navigation.loadEventStart,
                        first_paint: performance.getEntriesByType('paint').find(p => p.name === 'first-paint')?.startTime || 0
                    }
                }
            """)
            test_result["performance"].update(performance)
            
            # Déterminer le statut final
            if len(test_result["errors"]) == 0:
                test_result["status"] = "passed"
                print(f"  ✅ Test réussi: {test_config['name']}")
            else:
                test_result["status"] = "failed"
                print(f"  ❌ Test échoué: {test_config['name']} ({len(test_result['errors'])} erreurs)")
                
        except Exception as e:
            test_result["status"] = "error"
            test_result["errors"].append(f"Exception: {str(e)}")
            print(f"  💥 Erreur durant le test: {e}")
        
        finally:
            await page.close()
            
        return test_result

    async def run_validation(self):
        """Exécuter la validation complète"""
        print("🎯 Début de la validation PaniniFS Navigation")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Démarrer le serveur
        if not await self.start_server():
            return False
        
        try:
            async with async_playwright() as p:
                # Lancer le navigateur
                browser = await p.chromium.launch(headless=True)
                
                print(f"\n🔬 Exécution de {len(self.mandatory_tests)} tests obligatoires...")
                
                # Exécuter tous les tests
                for test_config in self.mandatory_tests:
                    test_result = await self.validate_page(browser, test_config)
                    self.results["test_results"].append(test_result)
                    self.results["total_tests"] += 1
                    
                    if test_result["status"] == "passed":
                        self.results["passed_tests"] += 1
                    else:
                        self.results["failed_tests"] += 1
                
                await browser.close()
                
        except Exception as e:
            print(f"💥 Erreur critique durant la validation: {e}")
            return False
        
        finally:
            # Arrêter le serveur si on l'a démarré
            if self.results["server_status"] == "started":
                await self.stop_server()
        
        return True

    def generate_report(self):
        """Générer le rapport de validation"""
        success_rate = (self.results["passed_tests"] / self.results["total_tests"]) * 100 if self.results["total_tests"] > 0 else 0
        
        print(f"\n{'='*60}")
        print("📊 RAPPORT DE VALIDATION PANINIFSNAVIGATION")
        print(f"{'='*60}")
        print(f"⏰ Timestamp: {self.results['timestamp']}")
        print(f"🌐 Serveur: {self.results['server_status']}")
        print(f"📈 Tests total: {self.results['total_tests']}")
        print(f"✅ Tests réussis: {self.results['passed_tests']}")
        print(f"❌ Tests échoués: {self.results['failed_tests']}")
        print(f"🎯 Taux de réussite: {success_rate:.1f}%")
        
        print(f"\n📋 DÉTAIL DES TESTS:")
        for result in self.results["test_results"]:
            status_icon = "✅" if result["status"] == "passed" else "❌"
            print(f"{status_icon} {result['name']} ({result['category']})")
            if result["errors"]:
                for error in result["errors"]:
                    print(f"   💥 {error}")
            if result["performance"].get("load_time"):
                print(f"   ⏱️ Temps de chargement: {result['performance']['load_time']:.2f}s")
        
        # Sauvegarder le rapport JSON
        report_path = f"/tmp/paniniFS_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport JSON sauvegardé: {report_path}")
        
        if self.results["screenshots"]:
            print(f"📸 Screenshots disponibles:")
            for screenshot in self.results["screenshots"]:
                print(f"   📷 {screenshot}")
        
        # Déterminer le résultat global
        if success_rate >= 90:
            print(f"\n🎉 VALIDATION RÉUSSIE (≥90%)")
            return True
        else:
            print(f"\n⚠️ VALIDATION PARTIELLEMENT ÉCHOUÉE (<90%)")
            return False

async def main():
    """Point d'entrée principal"""
    validator = PaniniFSNavigationValidator()
    
    try:
        success = await validator.run_validation()
        if success:
            validation_passed = validator.generate_report()
            sys.exit(0 if validation_passed else 1)
        else:
            print("💥 Validation interrompue par une erreur critique")
            sys.exit(2)
    except KeyboardInterrupt:
        print("\n🛑 Validation interrompue par l'utilisateur")
        sys.exit(3)
    except Exception as e:
        print(f"💥 Erreur inattendue: {e}")
        sys.exit(4)

if __name__ == "__main__":
    asyncio.run(main())
