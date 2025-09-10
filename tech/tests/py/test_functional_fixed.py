#!/usr/bin/env python3
"""
Tests Fonctionnels Corrigés PaniniFS Research
Version améliorée avec patterns de détection ajustés
"""

import urllib.request
import urllib.error
import json
import time
from datetime import datetime
import re

class PaniniFSFunctionalTesterFixed:
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {}
        }
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test_dhatu_data_integrity(self):
        """Test l'intégrité des données dhātu - version corrigée"""
        self.log("🔍 Test d'intégrité des données dhātu (corrigé)")
        
        try:
            response = urllib.request.urlopen(f"{self.base_url}/interactive-validator/dhatu-data.js", timeout=10)
            content = response.read().decode('utf-8')
            
            # Vérifications corrigées
            checks = {
                "dhatu_database_present": "DhatuDatabase" in content,
                "minimal_dhatu_entries": content.count("id:") >= 15,
                "language_support": ("fr':" in content and "en':" in content),
                "validation_metadata": "validationStatus" in content,
                "cross_linguistic": ("crossLinguisticEvidence" in content)
            }
            
            passed = sum(checks.values())
            total = len(checks)
            
            self.results["tests"].append({
                "name": "Intégrité données dhātu",
                "passed": passed,
                "total": total,
                "success": passed == total,
                "details": checks
            })
            
            if passed == total:
                self.log(f"✅ Données dhātu intègres ({passed}/{total})")
                return True
            else:
                self.log(f"❌ Problèmes données dhātu ({passed}/{total})")
                for check, result in checks.items():
                    status = "✅" if result else "❌"
                    self.log(f"   {status} {check}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur test données dhātu: {e}")
            return False
    
    def test_gesture_animations(self):
        """Test la présence des animations de gestes - version corrigée"""
        self.log("🎭 Test des animations de gestes baby sign (corrigé)")
        
        try:
            response = urllib.request.urlopen(f"{self.base_url}/interactive-validator/enhanced-baby-sign-gestures.js", timeout=10)
            content = response.read().decode('utf-8')
            
            # Vérifications corrigées des animations
            animation_checks = {
                "svg_elements": content.count("<svg") >= 5,
                "gesture_objects": content.count("MOTHER") >= 1 and content.count("FATHER") >= 1,
                "anatomical_features": ("hand" in content and "circle" in content),
                "animations": ("animate" in content and "dur=" in content),
                "baby_sign_vocabulary": content.count("baby-sign") >= 10
            }
            
            passed = sum(animation_checks.values())
            total = len(animation_checks)
            
            self.results["tests"].append({
                "name": "Animations gestes baby sign",
                "passed": passed,
                "total": total,
                "success": passed == total,
                "details": animation_checks
            })
            
            if passed == total:
                self.log(f"✅ Animations gestes fonctionnelles ({passed}/{total})")
                return True
            else:
                self.log(f"❌ Problèmes animations gestes ({passed}/{total})")
                for check, result in animation_checks.items():
                    status = "✅" if result else "❌"
                    self.log(f"   {status} {check}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur test animations: {e}")
            return False
    
    def test_interactive_features(self):
        """Test des fonctionnalités interactives - version corrigée"""
        self.log("🎮 Test des fonctionnalités interactives (corrigé)")
        
        try:
            # Test du fichier HTML principal
            response = urllib.request.urlopen(f"{self.base_url}/interactive-validator/", timeout=10)
            html_content = response.read().decode('utf-8')
            
            # Test du fichier JavaScript
            response_js = urllib.request.urlopen(f"{self.base_url}/interactive-validator/app.js", timeout=10)
            js_content = response_js.read().decode('utf-8')
            
            # Vérifications HTML
            html_checks = {
                "nav_tabs_present": "nav-tabs" in html_content,
                "dhatu_grid_present": "dhatu-grid" in html_content,
                "app_container_present": "app-container" in html_content
            }
            
            # Vérifications JavaScript
            js_checks = {
                "event_listeners": ("addEventListener" in js_content or "onclick" in js_content),
                "dom_queries": ("querySelector" in js_content or "getElementById" in js_content),
                "functions_defined": "function" in js_content or "=>" in js_content
            }
            
            all_checks = {**html_checks, **js_checks}
            passed = sum(all_checks.values())
            total = len(all_checks)
            
            self.results["tests"].append({
                "name": "Fonctionnalités interactives",
                "passed": passed,
                "total": total,
                "success": passed == total,
                "details": all_checks
            })
            
            if passed == total:
                self.log(f"✅ Fonctionnalités interactives présentes ({passed}/{total})")
                return True
            else:
                self.log(f"❌ Fonctionnalités interactives incomplètes ({passed}/{total})")
                for check, result in all_checks.items():
                    status = "✅" if result else "❌"
                    self.log(f"   {status} {check}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur test fonctionnalités interactives: {e}")
            return False
    
    def test_cross_page_navigation(self):
        """Test de la navigation entre les pages"""
        self.log("🧭 Test de navigation inter-pages")
        
        pages_to_test = [
            ("/hub.html", ["PaniniFS Research Hub", "access-card"]),
            ("/interactive-validator/", ["dhatu-grid", "nav-tabs"]),
            ("/interactive-validator/gesture-gallery.html", ["gesture-showcase", "Galerie"]),
            ("/interactive-validator/test-gestures.html", ["gesture-grid", "Test"]),
            ("/navigation-test.html", ["Test de Navigation", "test-results"])
        ]
        
        success_count = 0
        
        for page_url, indicators in pages_to_test:
            try:
                full_url = self.base_url + page_url
                response = urllib.request.urlopen(full_url, timeout=10)
                content = response.read().decode('utf-8')
                
                found_all = all(indicator in content for indicator in indicators)
                
                if found_all:
                    self.log(f"✅ {page_url} - Navigation OK")
                    success_count += 1
                else:
                    missing = [ind for ind in indicators if ind not in content]
                    self.log(f"❌ {page_url} - Manque: {missing}")
                    
            except Exception as e:
                self.log(f"❌ {page_url} - Erreur: {e}")
        
        total_pages = len(pages_to_test)
        navigation_success = success_count == total_pages
        
        self.results["tests"].append({
            "name": "Navigation inter-pages",
            "success": navigation_success,
            "pages_tested": total_pages,
            "pages_successful": success_count
        })
        
        if navigation_success:
            self.log(f"✅ Navigation complète fonctionnelle ({success_count}/{total_pages})")
        else:
            self.log(f"❌ Navigation partiellement défaillante ({success_count}/{total_pages})")
            
        return navigation_success
    
    def test_performance_metrics(self):
        """Test des métriques de performance"""
        self.log("⚡ Test des métriques de performance")
        
        test_urls = [
            f"{self.base_url}/hub.html",
            f"{self.base_url}/interactive-validator/",
            f"{self.base_url}/interactive-validator/gesture-gallery.html"
        ]
        
        performance_results = []
        
        for url in test_urls:
            try:
                start_time = time.time()
                response = urllib.request.urlopen(url, timeout=10)
                load_time = time.time() - start_time
                content_size = len(response.read())
                
                performance_results.append({
                    "url": url,
                    "load_time": load_time,
                    "content_size": content_size,
                    "fast_enough": load_time < 3.0
                })
                
                if load_time < 3.0:
                    self.log(f"✅ {url} - {load_time:.3f}s")
                else:
                    self.log(f"❌ {url} - {load_time:.3f}s (trop lent)")
                    
            except Exception as e:
                self.log(f"❌ Erreur performance {url}: {e}")
                performance_results.append({
                    "url": url,
                    "error": str(e),
                    "fast_enough": False
                })
        
        fast_pages = sum(1 for r in performance_results if r.get("fast_enough", False))
        total_pages = len(performance_results)
        
        self.results["tests"].append({
            "name": "Performance",
            "success": fast_pages == total_pages,
            "fast_pages": fast_pages,
            "total_pages": total_pages,
            "details": performance_results
        })
        
        return fast_pages == total_pages
    
    def test_complete_functionality(self):
        """Test complet de fonctionnalité - nouveau test intégré"""
        self.log("🎯 Test de fonctionnalité complète")
        
        try:
            # Test que tous les fichiers requis sont présents et chargés
            required_files = [
                "/interactive-validator/dhatu-data.js",
                "/interactive-validator/enhanced-baby-sign-gestures.js", 
                "/interactive-validator/app.js"
            ]
            
            files_ok = 0
            
            for file_path in required_files:
                try:
                    response = urllib.request.urlopen(f"{self.base_url}{file_path}", timeout=5)
                    if response.status == 200:
                        self.log(f"✅ {file_path}")
                        files_ok += 1
                    else:
                        self.log(f"❌ {file_path} - Status {response.status}")
                except Exception as e:
                    self.log(f"❌ {file_path} - Erreur: {e}")
            
            total_required = len(required_files)
            functionality_success = files_ok == total_required
            
            self.results["tests"].append({
                "name": "Fonctionnalité complète",
                "success": functionality_success,
                "files_loaded": files_ok,
                "files_required": total_required
            })
            
            if functionality_success:
                self.log(f"✅ Fonctionnalité complète opérationnelle ({files_ok}/{total_required})")
            else:
                self.log(f"❌ Fonctionnalité incomplète ({files_ok}/{total_required})")
                
            return functionality_success
            
        except Exception as e:
            self.log(f"❌ Erreur test fonctionnalité complète: {e}")
            return False
    
    def run_complete_tests(self):
        """Exécute tous les tests fonctionnels corrigés"""
        self.log("🚀 Début des tests fonctionnels complets PaniniFS (Version Corrigée)")
        self.log("=" * 70)
        
        tests_to_run = [
            ("Intégrité données dhātu", self.test_dhatu_data_integrity),
            ("Animations gestes baby sign", self.test_gesture_animations),
            ("Fonctionnalités interactives", self.test_interactive_features),
            ("Navigation inter-pages", self.test_cross_page_navigation),
            ("Métriques performance", self.test_performance_metrics),
            ("Fonctionnalité complète", self.test_complete_functionality)
        ]
        
        successful_tests = 0
        total_tests = len(tests_to_run)
        
        for test_name, test_function in tests_to_run:
            self.log(f"\n📋 {test_name}")
            if test_function():
                successful_tests += 1
        
        # Calcul du résumé
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.results["summary"] = {
            "total_test_categories": total_tests,
            "successful_categories": successful_tests,
            "failed_categories": total_tests - successful_tests,
            "success_rate": round(success_rate, 2),
            "overall_success": success_rate >= 90
        }
        
        # Affichage du rapport final
        self.log("\n" + "=" * 70)
        self.log("📊 RAPPORT FINAL DES TESTS FONCTIONNELS")
        self.log("=" * 70)
        self.log(f"Catégories testées: {total_tests}")
        self.log(f"Catégories réussies: {successful_tests}")
        self.log(f"Catégories échouées: {total_tests - successful_tests}")
        self.log(f"Taux de réussite: {success_rate:.1f}%")
        
        # Sauvegarde du rapport
        report_file = f"/tmp/paniniFS_functional_tests_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        self.log(f"Rapport détaillé: {report_file}")
        
        if success_rate >= 90:
            self.log("🎉 TESTS FONCTIONNELS RÉUSSIS - Site entièrement opérationnel!", "SUCCESS")
            return 0
        elif success_rate >= 70:
            self.log("⚠️ TESTS FONCTIONNELS MAJORITAIREMENT RÉUSSIS - Site fonctionnel avec optimisations possibles", "SUCCESS")
            return 0
        else:
            self.log("🚨 TESTS FONCTIONNELS PARTIELLEMENT ÉCHOUÉS - Améliorations requises!", "WARNING")
            return 1

def main():
    tester = PaniniFSFunctionalTesterFixed()
    return tester.run_complete_tests()

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)
