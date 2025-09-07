#!/usr/bin/env python3
"""
Optimiseur de Set Minimal de Dhātu pour PaniniFS
Recherche le nombre optimal de dhātu pour couverture sémantique maximale
"""

import json
import itertools
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
from semantic_coverage_analyzer import SemanticCoverageAnalyzer
from dhatu_candidate_generator import DhatuCandidateGenerator, DhatuCandidate

@dataclass
class OptimizationResult:
    """Résultat d'une optimisation de set dhātu"""
    dhatu_set: List[str]
    coverage_score: float
    efficiency_ratio: float  # coverage / dhatu_count
    semantic_completeness: float  # % concepts sémantiques couverts
    redundancy_score: float  # Niveau de redondance entre dhātu

class DhatuSetOptimizer:
    """Optimiseur pour trouver le set minimal de dhātu optimal"""
    
    def __init__(self):
        self.analyzer = SemanticCoverageAnalyzer()
        self.generator = DhatuCandidateGenerator()
        
        # Définition des nouveaux dhātu proposés avec leurs patterns
        self.extended_dhatu_patterns = {
            # Dhātu originaux
            **self.analyzer.dhatu_patterns,
            
            # Nouveaux dhātu candidats
            'EXIST': {
                'patterns': [
                    r'\b(exists?|there is|there are|being|reality|presence)\b',
                    r'\b(existe|il y a|être|réalité|présence)\b',
                    r'\b(available|present|absent|missing)\b'
                ],
                'concepts': ['existence', 'presence', 'being', 'availability']
            },
            'EVAL': {
                'patterns': [
                    r'\b(elegant|beautiful|ugly|good|bad|better|worse|quality)\b',
                    r'\b(élégant|beau|laid|bon|mauvais|meilleur|pire|qualité)\b',
                    r'\b(clean|robust|efficient|optimal|superior)\b'
                ],
                'concepts': ['evaluation', 'quality', 'assessment', 'aesthetics']
            },
            'CAUSE': {
                'patterns': [
                    r'\b(because|since|due to|causes?|results in|leads to)\b',
                    r'\b(parce que|car|à cause de|provoque|entraîne|mène à)\b',
                    r'\b(therefore|thus|consequently|hence)\b'
                ],
                'concepts': ['causation', 'consequence', 'reason', 'implication']
            },
            'MODAL': {
                'patterns': [
                    r'\b(might|could|may|possible|potential|maybe|perhaps)\b',
                    r'\b(pourrait|peut-être|possible|potentiel|éventuellement)\b',
                    r'\b(probably|likely|unlikely|chance)\b'
                ],
                'concepts': ['possibility', 'probability', 'modality', 'uncertainty']
            },
            'RELATE': {
                'patterns': [
                    r'\b(relates to|in relation to|connected to|linked to|associated)\b',
                    r'\b(en relation avec|lié à|associé à|connecté à)\b',
                    r'\b(compared to|versus|relative to|with respect to)\b'
                ],
                'concepts': ['relation', 'connection', 'association', 'comparison']
            },
            'FEEL': {
                'patterns': [
                    r'\b(love|hate|like|prefer|enjoy|appreciate|dislike)\b',
                    r'\b(aime|déteste|préfère|apprécie|n\'aime pas)\b',
                    r'\b(satisfying|frustrating|exciting|boring|pleasant)\b'
                ],
                'concepts': ['emotion', 'preference', 'feeling', 'sentiment']
            },
            'FLOW': {
                'patterns': [
                    r'\b(then|after|before|next|previous|timeline|sequence)\b',
                    r'\b(puis|après|avant|suivant|précédent|chronologie)\b',
                    r'\b(meanwhile|simultaneously|eventually|finally)\b'
                ],
                'concepts': ['temporal_flow', 'progression', 'chronology', 'timing']
            }
        }
    
    def find_minimal_optimal_set(self, target_coverage: float = 90.0, 
                                max_dhatu: int = 12, 
                                test_corpus: List[str] = None) -> Dict:
        """Trouve le set minimal de dhātu pour atteindre la couverture cible"""
        
        if test_corpus is None:
            test_corpus = self._get_default_test_corpus()
        
        all_dhatu = list(self.extended_dhatu_patterns.keys())
        best_result = None
        results_by_size = defaultdict(list)
        
        print(f"🔍 Recherche du set optimal (cible: {target_coverage}%, max: {max_dhatu} dhātu)")
        print(f"📊 Corpus de test: {len(test_corpus)} textes")
        print(f"🧬 Dhātu disponibles: {len(all_dhatu)} ({', '.join(all_dhatu)})")
        
        # Tester des sets de taille croissante
        for size in range(7, min(max_dhatu + 1, len(all_dhatu) + 1)):
            print(f"\n⚙️  Test des combinaisons de {size} dhātu...")
            
            # Limiter le nombre de combinaisons testées pour éviter l'explosion combinatoire
            max_combinations = 1000 if size <= 10 else 500
            combinations_tested = 0
            
            for dhatu_combination in itertools.combinations(all_dhatu, size):
                if combinations_tested >= max_combinations:
                    print(f"   (Limite de {max_combinations} combinaisons atteinte)")
                    break
                
                # Tester cette combinaison
                result = self._evaluate_dhatu_set(list(dhatu_combination), test_corpus)
                results_by_size[size].append(result)
                
                # Vérifier si c'est le meilleur résultat jusqu'à présent
                if (best_result is None or 
                    (result.coverage_score >= target_coverage and 
                     result.efficiency_ratio > best_result.efficiency_ratio) or
                    (best_result.coverage_score < target_coverage and 
                     result.coverage_score > best_result.coverage_score)):
                    best_result = result
                
                combinations_tested += 1
                
                # Affichage de progression
                if combinations_tested % 100 == 0:
                    print(f"   {combinations_tested} combinaisons testées...")
            
            # Si on a atteint la cible avec cette taille, on peut s'arrêter
            best_for_size = max(results_by_size[size], key=lambda x: x.coverage_score)
            print(f"   Meilleur pour {size} dhātu: {best_for_size.coverage_score:.1f}% "
                  f"(efficacité: {best_for_size.efficiency_ratio:.1f}%)")
            
            if best_for_size.coverage_score >= target_coverage:
                print(f"   ✅ Cible atteinte avec {size} dhātu !")
                break
        
        return {
            'optimal_result': best_result,
            'results_by_size': dict(results_by_size),
            'analysis': self._analyze_optimization_results(results_by_size, target_coverage),
            'recommendations': self._generate_optimization_recommendations(best_result, target_coverage)
        }
    
    def _evaluate_dhatu_set(self, dhatu_set: List[str], test_corpus: List[str]) -> OptimizationResult:
        """Évalue un set specific de dhātu sur le corpus de test"""
        
        # Créer un analyseur temporaire avec ce set de dhātu
        temp_patterns = {k: v for k, v in self.extended_dhatu_patterns.items() if k in dhatu_set}
        temp_analyzer = SemanticCoverageAnalyzer()
        temp_analyzer.dhatu_patterns = temp_patterns
        
        total_coverage = []
        semantic_concepts_covered = set()
        semantic_concepts_total = set()
        
        for text in test_corpus:
            result = temp_analyzer.analyze_text(text)
            total_coverage.append(result['coverage_score']['percentage'])
            
            # Compter les concepts sémantiques
            for match in result['dhatu_matches']:
                semantic_concepts_covered.add(match.concept)
            
            # Estimer les concepts totaux (y compris gaps)
            for gap in result['semantic_gaps']:
                semantic_concepts_total.add(gap.semantic_category)
        
        avg_coverage = sum(total_coverage) / len(total_coverage) if total_coverage else 0
        semantic_completeness = len(semantic_concepts_covered) / max(len(semantic_concepts_covered) + len(semantic_concepts_total), 1) * 100
        efficiency_ratio = avg_coverage / len(dhatu_set) if dhatu_set else 0
        
        # Calculer la redondance (concepts qui se chevauchent)
        redundancy_score = self._calculate_redundancy(dhatu_set, temp_patterns)
        
        return OptimizationResult(
            dhatu_set=dhatu_set,
            coverage_score=avg_coverage,
            efficiency_ratio=efficiency_ratio,
            semantic_completeness=semantic_completeness,
            redundancy_score=redundancy_score
        )
    
    def _calculate_redundancy(self, dhatu_set: List[str], patterns: Dict) -> float:
        """Calcule le score de redondance entre dhātu (patterns qui se chevauchent)"""
        
        # Analyse simple : compter les mots-clés partagés entre patterns
        all_words = defaultdict(list)
        
        for dhatu_name in dhatu_set:
            if dhatu_name in patterns:
                for pattern in patterns[dhatu_name]['patterns']:
                    # Extraire les mots des patterns regex
                    words = pattern.replace(r'\b', '').replace('(', '').replace(')', '').split('|')
                    for word in words:
                        if word.strip():
                            all_words[word.strip().lower()].append(dhatu_name)
        
        # Calculer le pourcentage de mots partagés
        shared_words = sum(1 for dhatu_list in all_words.values() if len(dhatu_list) > 1)
        total_words = len(all_words)
        
        return (shared_words / total_words * 100) if total_words > 0 else 0
    
    def _get_default_test_corpus(self) -> List[str]:
        """Corpus de test par défaut pour l'optimisation"""
        return [
            "I love this elegant solution because it efficiently transforms data",
            "Cette approche est robuste car elle gère bien les cas d'erreur", 
            "for i in range(10): print(i) if i > 5",
            "The algorithm exists to solve the problem, but it might sometimes fail",
            "En relation avec notre discussion, ce code est plus lisible",
            "Cette fonction est belle et efficace comparée à l'ancienne version",
            "Le système pourrait être amélioré si nous ajoutons cette fonctionnalité",
            "Par opposition aux autres solutions, celle-ci est plus maintenable",
            "Il y a plusieurs façons d'implémenter cela, mais cette approche est préférable",
            "Pendant que le processus s'exécute, nous pouvons faire autre chose",
            "Cette méthode fonctionne bien parce qu'elle suit les bonnes pratiques",
            "def process_data(input_list): return [x*2 for x in input_list if x > 0]",
            "The user interface feels intuitive and responds quickly to input",
            "We need to locate the bug and decide how to fix it systematically",
            "This pattern groups similar items and sequences them logically"
        ]
    
    def _analyze_optimization_results(self, results_by_size: Dict, target_coverage: float) -> Dict:
        """Analyse les résultats d'optimisation pour identifier les patterns"""
        
        analysis = {
            'coverage_progression': {},
            'efficiency_sweet_spot': None,
            'minimal_viable_size': None,
            'optimal_size': None
        }
        
        for size, results in results_by_size.items():
            best_for_size = max(results, key=lambda x: x.coverage_score)
            analysis['coverage_progression'][size] = {
                'best_coverage': best_for_size.coverage_score,
                'best_efficiency': best_for_size.efficiency_ratio,
                'avg_coverage': sum(r.coverage_score for r in results) / len(results)
            }
            
            # Identifier la taille minimale viable (atteint la cible)
            if (analysis['minimal_viable_size'] is None and 
                best_for_size.coverage_score >= target_coverage):
                analysis['minimal_viable_size'] = size
            
            # Identifier le sweet spot d'efficacité
            if (analysis['efficiency_sweet_spot'] is None or 
                best_for_size.efficiency_ratio > analysis['efficiency_sweet_spot'][1]):
                analysis['efficiency_sweet_spot'] = (size, best_for_size.efficiency_ratio)
        
        # Identifier la taille optimale (équilibre couverture/efficacité)
        if analysis['minimal_viable_size']:
            analysis['optimal_size'] = analysis['minimal_viable_size']
        else:
            # Prendre la taille avec la meilleure efficacité
            if analysis['efficiency_sweet_spot']:
                analysis['optimal_size'] = analysis['efficiency_sweet_spot'][0]
        
        return analysis
    
    def _generate_optimization_recommendations(self, best_result: OptimizationResult, 
                                             target_coverage: float) -> List[str]:
        """Génère des recommandations basées sur les résultats d'optimisation"""
        
        recommendations = []
        
        if best_result is None:
            return ["Aucun résultat d'optimisation disponible"]
        
        if best_result.coverage_score >= target_coverage:
            recommendations.append(f"✅ Cible atteinte avec {len(best_result.dhatu_set)} dhātu "
                                 f"({best_result.coverage_score:.1f}%)")
        else:
            recommendations.append(f"⚠️  Cible non atteinte : {best_result.coverage_score:.1f}% "
                                 f"vs {target_coverage}% visé")
        
        if best_result.efficiency_ratio > 8.0:
            recommendations.append("🎯 Excellente efficacité par dhātu")
        elif best_result.efficiency_ratio > 6.0:
            recommendations.append("👍 Bonne efficacité par dhātu")
        else:
            recommendations.append("⚠️  Efficacité faible - considérer réduction du set")
        
        if best_result.redundancy_score > 20:
            recommendations.append("🔄 Redondance élevée détectée - optimisation possible")
        
        if best_result.semantic_completeness > 80:
            recommendations.append("🌐 Excellente couverture des concepts sémantiques")
        
        return recommendations

def main():
    """Fonction de test et démonstration"""
    optimizer = DhatuSetOptimizer()
    
    print("⚡ OPTIMISEUR DE SET MINIMAL DHĀTU")
    print("=" * 45)
    
    # Test avec différents objectifs de couverture
    targets = [80.0, 85.0, 90.0]
    
    for target in targets:
        print(f"\n🎯 OPTIMISATION POUR {target}% DE COUVERTURE")
        print("-" * 40)
        
        result = optimizer.find_minimal_optimal_set(
            target_coverage=target,
            max_dhatu=12
        )
        
        if result['optimal_result']:
            opt = result['optimal_result']
            print(f"Set optimal: {', '.join(opt.dhatu_set)}")
            print(f"Taille: {len(opt.dhatu_set)} dhātu")
            print(f"Couverture: {opt.coverage_score:.1f}%")
            print(f"Efficacité: {opt.efficiency_ratio:.1f}% par dhātu")
            print(f"Complétude sémantique: {opt.semantic_completeness:.1f}%")
            print(f"Redondance: {opt.redundancy_score:.1f}%")
            
            print("\n📋 Recommandations:")
            for rec in result['recommendations']:
                print(f"  • {rec}")
        
        # Afficher progression par taille
        if result['analysis']['coverage_progression']:
            print("\n📈 Progression par taille:")
            for size, metrics in result['analysis']['coverage_progression'].items():
                print(f"  {size} dhātu: {metrics['best_coverage']:.1f}% "
                      f"(eff: {metrics['best_efficiency']:.1f}%)")

if __name__ == "__main__":
    main()
