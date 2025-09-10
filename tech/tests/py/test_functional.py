#!/usr/bin/env python3
"""
Tests Fonctionnels Approfondis PaniniFS Research
Validation complète de toutes les fonctionnalités du site
"""

import urllib.request
import urllib.error
import json
import time
from datetime import datetime
import re

class PaniniFSFunctionalTester:
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
        
    def test_javascript_functionality(self, url, js_indicators):
        """Test la présence d'éléments qui indiquent que JavaScript fonctionne"""
        try:
            response = urllib.request.urlopen(url, timeout=10)
            content = response.read().decode('utf-8')
            
            found_indicators = []
            missing_indicators = []
            
            for indicator in js_indicators:
                if indicator in content:
                    found_indicators.append(indicator)
                else:
                    missing_indicators.append(indicator)
            
            success = len(missing_indicators) == 0
            
            return {
                "success": success,
                "found": found_indicators,
                "missing": missing_indicators,
                "content_length": len(content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_dhatu_data_integrity(self):
        """Test l'intégrité des données dhātu"""
        self.log("🔍 Test d'intégrité des données dhātu")
        
        try:
            response = urllib.request.urlopen(f"{self.base_url}/interactive-validator/dhatu-data.js", timeout=10)
            content = response.read().decode('utf-8')
            
            # Vérifications essentielles
            checks = {
                "dhatu_array_present": "const dhatu" in content,
                "minimal_dhatu_count": content.count('"root":') >= 15,
                "language_support": "french" in content and "english" in content,
                "validation_metadata": "validationStatus" in content,
                "cross_linguistic": "arabic" in content or "lsq" in content
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
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur test données dhātu: {e}")
            return False
    
    def test_gesture_animations(self):
        """Test la présence des animations de gestes"""
        self.log("🎭 Test des animations de gestes baby sign")
        
        try:
            response = urllib.request.urlopen(f"{self.base_url}/interactive-validator/enhanced-baby-sign-gestures.js", timeout=10)
            content = response.read().decode('utf-8')
            
            # Vérifications des animations
            animation_checks = {
                "svg_animations": content.count("<animate") >= 10,
                "gesture_definitions": content.count("function") >= 15,
                "anatomical_features": "hands" in content and "body" in content,
                "movement_patterns": "dur=" in content,
                "baby_sign_vocabulary": content.count('id="') >= 50
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
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur test animations: {e}")
            return False
    
    def test_interactive_features(self):
        """Test des fonctionnalités interactives de l'application"""
        self.log("🎮 Test des fonctionnalités interactives")
        
        url = f"{self.base_url}/interactive-validator/"
        js_indicators = [
            "nav-tabs",
            "dhatu-grid", 
            "app-container",
            "addEventListener",
            "querySelector",
            "class=",
            "function",
            "onclick"
        ]
        
        result = self.test_javascript_functionality(url, js_indicators)
        
        if result["success"]:
            self.log(f"✅ Fonctionnalités interactives présentes ({len(result['found'])}/{len(js_indicators)})")
            
            self.results["tests"].append({
                "name": "Fonctionnalités interactives",
                "success": True,
                "found_elements": len(result["found"]),
                "total_elements": len(js_indicators)
            })
            return True
        else:
            self.log(f"❌ Fonctionnalités interactives manquantes: {result.get('missing', [])}")
            
            self.results["tests"].append({
                "name": "Fonctionnalités interactives", 
                "success": False,
                "missing_elements": result.get("missing", []),
                "error": result.get("error")
            })
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
            full_url = self.base_url + page_url
            result = self.test_javascript_functionality(full_url, indicators)
            
            if result["success"]:
                self.log(f"✅ {page_url} - Navigation OK")
                success_count += 1
            else:
                self.log(f"❌ {page_url} - Problème navigation")
        
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
    
    def run_complete_tests(self):
        """Exécute tous les tests fonctionnels"""
        self.log("🚀 Début des tests fonctionnels complets PaniniFS")
        self.log("=" * 60)
        
        tests_to_run = [
            ("Intégrité données", self.test_dhatu_data_integrity),
            ("Animations gestes", self.test_gesture_animations),
            ("Fonctionnalités interactives", self.test_interactive_features),
            ("Navigation inter-pages", self.test_cross_page_navigation),
            ("Métriques performance", self.test_performance_metrics)
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
        self.log("\n" + "=" * 60)
        self.log("📊 RAPPORT DES TESTS FONCTIONNELS")
        self.log("=" * 60)
        self.log(f"Catégories testées: {total_tests}")
        self.log(f"Catégories réussies: {successful_tests}")
        self.log(f"Catégories échouées: {total_tests - successful_tests}")
        self.log(f"Taux de réussite: {success_rate:.1f}%")
        
        # Sauvegarde du rapport
        report_file = f"/tmp/paniniFS_functional_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        self.log(f"Rapport détaillé: {report_file}")
        
        if success_rate >= 90:
            self.log("🎉 TESTS FONCTIONNELS RÉUSSIS - Site entièrement opérationnel!", "SUCCESS")
            return 0
        else:
            self.log("🚨 TESTS FONCTIONNELS PARTIELLEMENT ÉCHOUÉS - Améliorations requises!", "WARNING")
            return 1

def main():
    tester = PaniniFSFunctionalTester()
    return tester.run_complete_tests()

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)
