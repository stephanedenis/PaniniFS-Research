#!/usr/bin/env python3
"""
Générateur de Dhātu Candidats pour PaniniFS
Analyse les gaps sémantiques et propose de nouveaux dhātu pour améliorer la couverture
"""

import json
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
from semantic_coverage_analyzer import SemanticCoverageAnalyzer, SemanticGap

@dataclass
class DhatuCandidate:
    """Représente un candidat dhātu pour combler un gap sémantique"""
    name: str
    sanskrit_root: str
    concept_primitif: str
    semantic_category: str
    example_patterns: List[str]
    coverage_improvement: float  # Estimation du gain de couverture
    priority: int  # 1 = haute, 3 = basse

class DhatuCandidateGenerator:
    """Génère des candidats dhātu basés sur l'analyse des gaps"""
    
    def __init__(self):
        self.analyzer = SemanticCoverageAnalyzer()
        
        # Mapping des catégories de gaps vers des dhātu candidats
        self.gap_to_dhatu_mapping = {
            'Dimension Émotionnelle/Qualitative': {
                'candidates': [
                    {
                        'name': 'EVAL',
                        'sanskrit_root': '√man (penser, évaluer)',
                        'concept': 'Évaluer qualitativement',
                        'patterns': ['élégant', 'beau', 'efficace', 'robuste', 'clean', 'elegant'],
                        'priority': 1
                    },
                    {
                        'name': 'FEEL',
                        'sanskrit_root': '√bhū (ressentir, être)',
                        'concept': 'Ressentir émotionnellement',
                        'patterns': ['aime', 'déteste', 'préfère', 'love', 'hate', 'like'],
                        'priority': 2
                    }
                ]
            },
            'Dimension Causale/Temporelle': {
                'candidates': [
                    {
                        'name': 'CAUSE',
                        'sanskrit_root': '√nī (conduire, causer)',
                        'concept': 'Causer, provoquer',
                        'patterns': ['parce que', 'car', 'because', 'since', 'causes', 'results in'],
                        'priority': 1
                    },
                    {
                        'name': 'FLOW',
                        'sanskrit_root': '√gam (aller, s\'écouler)',
                        'concept': 'Progresser temporellement',
                        'patterns': ['alors', 'puis', 'ensuite', 'then', 'after', 'timeline'],
                        'priority': 2
                    }
                ]
            },
            'Dimension Relationnelle/Contextuelle': {
                'candidates': [
                    {
                        'name': 'RELATE',
                        'sanskrit_root': '√bandh (lier, relier)',
                        'concept': 'Mettre en relation',
                        'patterns': ['en relation avec', 'par rapport à', 'relates to', 'compared to'],
                        'priority': 1
                    },
                    {
                        'name': 'CONTRAST',
                        'sanskrit_root': '√vṛt (tourner, opposer)',
                        'concept': 'Contraster, opposer',
                        'patterns': ['opposé', 'versus', 'par opposition', 'contrary to', 'different'],
                        'priority': 2
                    }
                ]
            },
            'Dimension Existentielle/Ontologique': {
                'candidates': [
                    {
                        'name': 'EXIST',
                        'sanskrit_root': '√as (être, exister)',
                        'concept': 'Exister, être présent',
                        'patterns': ['existe', 'il y a', 'exists', 'there is', 'being', 'reality'],
                        'priority': 1
                    },
                    {
                        'name': 'MODAL',
                        'sanskrit_root': '√śak (pouvoir, être capable)',
                        'concept': 'Modalité (possible/probable)',
                        'patterns': ['peut-être', 'possible', 'might', 'could', 'maybe', 'potential'],
                        'priority': 2
                    }
                ]
            },
            'Dimension Temporelle Complexe': {
                'candidates': [
                    {
                        'name': 'SYNC',
                        'sanskrit_root': '√yuj (joindre, synchroniser)',
                        'concept': 'Synchroniser temporellement',
                        'patterns': ['pendant', 'en même temps', 'while', 'during', 'simultaneously'],
                        'priority': 2
                    }
                ]
            },
            'Dimension Spatiale/Géométrique': {
                'candidates': [
                    {
                        'name': 'POSITION',
                        'sanskrit_root': '√sthā (se tenir, positionner)',
                        'concept': 'Positionner spatialement',
                        'patterns': ['au-dessus', 'dedans', 'près de', 'above', 'inside', 'near'],
                        'priority': 3
                    }
                ]
            }
        }
    
    def analyze_corpus_for_gaps(self, texts: List[str]) -> Dict:
        """Analyse un corpus pour identifier les gaps sémantiques principaux"""
        
        all_gaps = []
        gap_frequency = defaultdict(int)
        gap_examples = defaultdict(list)
        
        print(f"🔍 Analyse de {len(texts)} textes pour identifier les gaps...")
        
        for text in texts:
            result = self.analyzer.analyze_text(text)
            
            for gap in result['semantic_gaps']:
                all_gaps.append(gap)
                gap_frequency[gap.semantic_category] += 1
                gap_examples[gap.semantic_category].append(gap.text_fragment)
        
        # Trier par fréquence pour identifier les gaps prioritaires
        sorted_gaps = sorted(gap_frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_gaps': len(all_gaps),
            'gap_frequency': dict(gap_frequency),
            'gap_examples': {k: list(set(v)) for k, v in gap_examples.items()},
            'priority_order': sorted_gaps,
            'analysis_summary': self._generate_gap_analysis_summary(sorted_gaps, len(texts))
        }
    
    def generate_dhatu_candidates(self, gap_analysis: Dict) -> List[DhatuCandidate]:
        """Génère une liste de candidats dhātu basée sur l'analyse des gaps"""
        
        candidates = []
        
        for gap_category, frequency in gap_analysis['priority_order']:
            if gap_category in self.gap_to_dhatu_mapping:
                category_candidates = self.gap_to_dhatu_mapping[gap_category]['candidates']
                
                for candidate_info in category_candidates:
                    # Calcul de l'amélioration de couverture estimée
                    coverage_improvement = self._estimate_coverage_improvement(
                        frequency, len(gap_analysis['gap_examples'][gap_category])
                    )
                    
                    candidate = DhatuCandidate(
                        name=candidate_info['name'],
                        sanskrit_root=candidate_info['sanskrit_root'],
                        concept_primitif=candidate_info['concept'],
                        semantic_category=gap_category,
                        example_patterns=candidate_info['patterns'],
                        coverage_improvement=coverage_improvement,
                        priority=candidate_info['priority']
                    )
                    
                    candidates.append(candidate)
        
        # Trier par priorité et amélioration de couverture
        candidates.sort(key=lambda x: (x.priority, -x.coverage_improvement))
        
        return candidates
    
    def _estimate_coverage_improvement(self, frequency: int, unique_examples: int) -> float:
        """Estime l'amélioration de couverture qu'apporterait un nouveau dhātu"""
        # Formule simple : fréquence * diversité des exemples / 100
        return min((frequency * unique_examples) / 10.0, 25.0)  # Max 25% d'amélioration
    
    def _generate_gap_analysis_summary(self, sorted_gaps: List[Tuple], total_texts: int) -> Dict:
        """Génère un résumé de l'analyse des gaps"""
        
        if not sorted_gaps:
            return {'message': 'Aucun gap sémantique identifié', 'recommendation': 'Les 7 dhātu actuels sont suffisants'}
        
        top_gap = sorted_gaps[0]
        total_gap_instances = sum(freq for _, freq in sorted_gaps)
        
        return {
            'main_gap_category': top_gap[0],
            'main_gap_frequency': top_gap[1],
            'gap_density': round(total_gap_instances / total_texts, 2),
            'categories_affected': len(sorted_gaps),
            'recommendation': self._get_recommendation(total_gap_instances, total_texts)
        }
    
    def _get_recommendation(self, total_gaps: int, total_texts: int) -> str:
        """Génère une recommandation basée sur la densité des gaps"""
        density = total_gaps / total_texts
        
        if density > 2:
            return "Gaps sémantiques élevés : ajout de nouveaux dhātu fortement recommandé"
        elif density > 1:
            return "Gaps modérés : considérer l'ajout de 2-3 nouveaux dhātu prioritaires"
        elif density > 0.5:
            return "Gaps faibles : évaluer l'ajout de 1-2 dhātu spécialisés"
        else:
            return "Gaps négligeables : les dhātu actuels sont largement suffisants"
    
    def optimize_dhatu_set(self, current_dhatu: List[str], candidates: List[DhatuCandidate], 
                          target_coverage: float = 85.0) -> Dict:
        """Optimise le set de dhātu pour atteindre la couverture cible"""
        
        # Simulation d'optimisation (approche greedy)
        optimized_set = current_dhatu.copy()
        coverage_improvement = 0.0
        added_dhatu = []
        
        # Trier les candidats par rapport amélioration/priorité
        sorted_candidates = sorted(candidates, 
                                 key=lambda x: (-x.coverage_improvement, x.priority))
        
        current_coverage = 66.7  # Score de base observé
        
        for candidate in sorted_candidates:
            projected_coverage = current_coverage + candidate.coverage_improvement
            
            if projected_coverage <= target_coverage and len(optimized_set) < 15:  # Limite à 15 dhātu max
                optimized_set.append(candidate.name)
                added_dhatu.append(candidate)
                current_coverage = projected_coverage
                coverage_improvement += candidate.coverage_improvement
                
                if current_coverage >= target_coverage:
                    break
        
        return {
            'optimized_dhatu_set': optimized_set,
            'added_dhatu': [d.name for d in added_dhatu],
            'projected_coverage': round(current_coverage, 2),
            'improvement': round(coverage_improvement, 2),
            'total_dhatu_count': len(optimized_set),
            'efficiency_ratio': round(current_coverage / len(optimized_set), 2)
        }

def main():
    """Fonction de test et démonstration"""
    generator = DhatuCandidateGenerator()
    
    # Corpus de test étendu pour identifier les gaps
    test_corpus = [
        "I love this elegant solution because it efficiently transforms data",
        "Cette approche est robuste car elle gère bien les cas d'erreur",
        "The algorithm exists to solve the problem, but it might sometimes fail",
        "En relation avec notre discussion, ce code est plus lisible",
        "Cette fonction est belle et efficace comparée à l'ancienne version",
        "Le système pourrait être amélioré si nous ajoutons cette fonctionnalité",
        "Par opposition aux autres solutions, celle-ci est plus maintenable",
        "Il y a plusieurs façons d'implémenter cela, mais cette approche est préférable",
        "Pendant que le processus s'exécute, nous pouvons faire autre chose",
        "Cette méthode fonctionne bien parce qu'elle suit les bonnes pratiques"
    ]
    
    print("🧬 GÉNÉRATEUR DE DHĀTU CANDIDATS")
    print("=" * 50)
    
    # Étape 1: Analyser les gaps dans le corpus
    print("\n📊 ANALYSE DES GAPS SÉMANTIQUES")
    gap_analysis = generator.analyze_corpus_for_gaps(test_corpus)
    
    print(f"Total gaps identifiés: {gap_analysis['total_gaps']}")
    print(f"Catégories affectées: {len(gap_analysis['gap_frequency'])}")
    print(f"Densité de gaps: {gap_analysis['analysis_summary']['gap_density']}")
    
    print("\n🎯 Gaps prioritaires:")
    for category, freq in gap_analysis['priority_order'][:3]:
        print(f"  • {category}: {freq} occurrences")
        examples = gap_analysis['gap_examples'][category][:3]
        print(f"    Exemples: {', '.join(examples)}")
    
    # Étape 2: Générer les candidats dhātu
    print("\n🔬 CANDIDATS DHĀTU PROPOSÉS")
    candidates = generator.generate_dhatu_candidates(gap_analysis)
    
    for i, candidate in enumerate(candidates[:5], 1):  # Top 5
        print(f"\n{i}. **{candidate.name}** ({candidate.sanskrit_root})")
        print(f"   Concept: {candidate.concept_primitif}")
        print(f"   Catégorie: {candidate.semantic_category}")
        print(f"   Amélioration estimée: +{candidate.coverage_improvement:.1f}%")
        print(f"   Priorité: {candidate.priority}/3")
    
    # Étape 3: Optimisation du set complet
    print("\n⚡ OPTIMISATION DU SET DHĀTU")
    current_dhatu = ['COMM', 'ITER', 'TRANS', 'DECIDE', 'LOCATE', 'GROUP', 'SEQ']
    optimization = generator.optimize_dhatu_set(current_dhatu, candidates, target_coverage=85.0)
    
    print(f"Set actuel ({len(current_dhatu)} dhātu): {', '.join(current_dhatu)}")
    print(f"Set optimisé ({optimization['total_dhatu_count']} dhātu): {', '.join(optimization['optimized_dhatu_set'])}")
    print(f"Nouveaux dhātu ajoutés: {', '.join(optimization['added_dhatu'])}")
    print(f"Couverture projetée: {optimization['projected_coverage']}% (+{optimization['improvement']}%)")
    print(f"Efficacité: {optimization['efficiency_ratio']}% par dhātu")
    
    print(f"\n✅ Recommandation: {gap_analysis['analysis_summary']['recommendation']}")

if __name__ == "__main__":
    main()
