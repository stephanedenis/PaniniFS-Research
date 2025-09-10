#!/usr/bin/env python3
"""
Analyseur de Couverture Sémantique pour Dhātu PaniniFS
Mesure la couverture des 7 dhātu actuels et identifie les gaps sémantiques
"""

import re
import json
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class DhatuMatch:
    """Représente une détection de dhātu dans un texte"""
    dhatu: str
    concept: str
    text_fragment: str
    confidence: float
    position: Tuple[int, int]  # start, end

@dataclass
class SemanticGap:
    """Représente un concept non couvert par les dhātu actuels"""
    text_fragment: str
    semantic_category: str
    suggested_concepts: List[str]
    position: Tuple[int, int]

class SemanticCoverageAnalyzer:
    """Analyseur principal de couverture sémantique"""
    
    def __init__(self):
        self.dhatu_patterns = {
            'COMM': {
                'patterns': [
                    r'\b(print|echo|say|tell|communicate|speak|write|message|send|receive)\b',
                    r'\b(affiche|dit|communique|parle|écrit|message|envoie|reçoit)\b',
                    r'\b(console\.log|printf|puts|std::cout)\b'
                ],
                'concepts': ['communication', 'output', 'expression', 'transmission']
            },
            'ITER': {
                'patterns': [
                    r'\b(for|while|loop|repeat|each|iterate|map|forEach)\b',
                    r'\b(pour|tant que|boucle|répète|chaque|itère)\b',
                    r'\b(do.*while|for.*in|range\()\b'
                ],
                'concepts': ['repetition', 'iteration', 'traversal', 'enumeration']
            },
            'TRANS': {
                'patterns': [
                    r'\b(transform|convert|parse|filter|modify|change|update)\b',
                    r'\b(transforme|convertit|analyse|filtre|modifie|change|met à jour)\b',
                    r'\b(map\(|filter\(|reduce\()\b'
                ],
                'concepts': ['transformation', 'conversion', 'modification', 'processing']
            },
            'DECIDE': {
                'patterns': [
                    r'\b(if|else|switch|case|choose|decide|when|unless)\b',
                    r'\b(si|sinon|choisit|décide|quand|à moins que)\b',
                    r'\b(ternary|conditional|branch)\b'
                ],
                'concepts': ['decision', 'choice', 'branching', 'condition']
            },
            'LOCATE': {
                'patterns': [
                    r'\b(find|search|locate|seek|get|fetch|retrieve)\b',
                    r'\b(trouve|cherche|localise|obtient|récupère)\b',
                    r'\b(indexOf|querySelector|grep)\b'
                ],
                'concepts': ['location', 'search', 'retrieval', 'finding']
            },
            'GROUP': {
                'patterns': [
                    r'\b(group|cluster|collect|gather|aggregate|array|list)\b',
                    r'\b(groupe|rassemble|collecte|agrège|tableau|liste)\b',
                    r'\b(\[.*\]|Array\(|new.*\[\])\b'
                ],
                'concepts': ['grouping', 'collection', 'aggregation', 'clustering']
            },
            'SEQ': {
                'patterns': [
                    r'\b(sort|order|sequence|first|last|next|prev|step)\b',
                    r'\b(trie|ordonne|séquence|premier|dernier|suivant|précédent|étape)\b',
                    r'\b(before|after|then|finally)\b'
                ],
                'concepts': ['sequencing', 'ordering', 'progression', 'steps']
            }
        }
        
        # Patterns pour identifier les gaps sémantiques
        self.gap_patterns = {
            'EMOTIONAL': {
                'patterns': [
                    r'\b(elegant|beautiful|ugly|love|hate|like|prefer|enjoy)\b',
                    r'\b(élégant|beau|laid|aime|déteste|préfère|apprécie)\b',
                    r'\b(satisfying|frustrating|exciting|boring)\b'
                ],
                'category': 'Dimension Émotionnelle/Qualitative'
            },
            'CAUSAL': {
                'patterns': [
                    r'\b(because|since|therefore|thus|consequently|due to|results in)\b',
                    r'\b(parce que|puisque|donc|ainsi|par conséquent|à cause de|résulte en)\b',
                    r'\b(causes?|effects?|leads to|triggers)\b'
                ],
                'category': 'Dimension Causale/Temporelle'
            },
            'RELATIONAL': {
                'patterns': [
                    r'\b(relates to|in relation to|compared to|versus|opposite|similar)\b',
                    r'\b(en relation avec|par rapport à|comparé à|opposé|similaire)\b',
                    r'\b(analogy|metaphor|like|as)\b'
                ],
                'category': 'Dimension Relationnelle/Contextuelle'
            },
            'EXISTENTIAL': {
                'patterns': [
                    r'\b(exists?|there is|there are|being|essence|nature|reality)\b',
                    r'\b(existe|il y a|être|essence|nature|réalité)\b',
                    r'\b(possible|potential|maybe|might|could)\b'
                ],
                'category': 'Dimension Existentielle/Ontologique'
            },
            'TEMPORAL': {
                'patterns': [
                    r'\b(now|then|when|while|during|until|since|always|never)\b',
                    r'\b(maintenant|alors|quand|pendant|jusqu\'à|depuis|toujours|jamais)\b',
                    r'\b(timeline|schedule|chronology)\b'
                ],
                'category': 'Dimension Temporelle Complexe'
            },
            'SPATIAL': {
                'patterns': [
                    r'\b(above|below|inside|outside|near|far|between|around)\b',
                    r'\b(au-dessus|en-dessous|dedans|dehors|près|loin|entre|autour)\b',
                    r'\b(position|location|place|here|there)\b'
                ],
                'category': 'Dimension Spatiale/Géométrique'
            }
        }
    
    def analyze_text(self, text: str) -> Dict:
        """Analyse complète d'un texte pour identifier dhātu et gaps"""
        
        # Détection des dhātu existants
        dhatu_matches = self._detect_dhatu(text)
        
        # Détection des gaps sémantiques
        semantic_gaps = self._detect_semantic_gaps(text)
        
        # Calcul de la couverture
        coverage_score = self._calculate_coverage(text, dhatu_matches, semantic_gaps)
        
        return {
            'text': text,
            'dhatu_matches': dhatu_matches,
            'semantic_gaps': semantic_gaps,
            'coverage_score': coverage_score,
            'analysis_summary': self._generate_summary(dhatu_matches, semantic_gaps, coverage_score)
        }
    
    def _detect_dhatu(self, text: str) -> List[DhatuMatch]:
        """Détecte les occurrences des dhātu existants"""
        matches = []
        
        for dhatu_name, dhatu_info in self.dhatu_patterns.items():
            for pattern in dhatu_info['patterns']:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    matches.append(DhatuMatch(
                        dhatu=dhatu_name,
                        concept=dhatu_info['concepts'][0],  # Concept principal
                        text_fragment=match.group(),
                        confidence=0.8,  # Score par défaut
                        position=(match.start(), match.end())
                    ))
        
        return sorted(matches, key=lambda x: x.position[0])
    
    def _detect_semantic_gaps(self, text: str) -> List[SemanticGap]:
        """Détecte les concepts non couverts par les dhātu actuels"""
        gaps = []
        
        for gap_name, gap_info in self.gap_patterns.items():
            for pattern in gap_info['patterns']:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    gaps.append(SemanticGap(
                        text_fragment=match.group(),
                        semantic_category=gap_info['category'],
                        suggested_concepts=[gap_name.lower()],
                        position=(match.start(), match.end())
                    ))
        
        return sorted(gaps, key=lambda x: x.position[0])
    
    def _calculate_coverage(self, text: str, dhatu_matches: List[DhatuMatch], 
                          semantic_gaps: List[SemanticGap]) -> Dict:
        """Calcule le score de couverture sémantique"""
        
        total_semantic_units = len(dhatu_matches) + len(semantic_gaps)
        covered_units = len(dhatu_matches)
        
        if total_semantic_units == 0:
            coverage_percentage = 100.0
        else:
            coverage_percentage = (covered_units / total_semantic_units) * 100
        
        return {
            'percentage': round(coverage_percentage, 2),
            'covered_units': covered_units,
            'gap_units': len(semantic_gaps),
            'total_semantic_units': total_semantic_units,
            'dhatu_distribution': self._get_dhatu_distribution(dhatu_matches)
        }
    
    def _get_dhatu_distribution(self, matches: List[DhatuMatch]) -> Dict[str, int]:
        """Calcule la distribution des dhātu détectés"""
        distribution = defaultdict(int)
        for match in matches:
            distribution[match.dhatu] += 1
        return dict(distribution)
    
    def _generate_summary(self, dhatu_matches: List[DhatuMatch], 
                         semantic_gaps: List[SemanticGap], 
                         coverage_score: Dict) -> Dict:
        """Génère un résumé de l'analyse"""
        
        gap_categories = defaultdict(int)
        for gap in semantic_gaps:
            gap_categories[gap.semantic_category] += 1
        
        return {
            'coverage_percentage': coverage_score['percentage'],
            'dominant_dhatu': max(coverage_score['dhatu_distribution'].items(), 
                                 key=lambda x: x[1])[0] if coverage_score['dhatu_distribution'] else None,
            'main_gap_categories': dict(gap_categories),
            'recommendations': self._generate_recommendations(gap_categories, coverage_score)
        }
    
    def _generate_recommendations(self, gap_categories: Dict, coverage_score: Dict) -> List[str]:
        """Génère des recommandations pour améliorer la couverture"""
        recommendations = []
        
        if coverage_score['percentage'] < 70:
            recommendations.append("Couverture faible : considérer l'ajout de nouveaux dhātu")
        
        for category, count in gap_categories.items():
            if count > 2:
                recommendations.append(f"Gap significatif en {category} : {count} occurrences")
        
        if not gap_categories:
            recommendations.append("Excellente couverture avec les dhātu actuels")
        
        return recommendations

def main():
    """Fonction de test et démonstration"""
    analyzer = SemanticCoverageAnalyzer()
    
    # Textes de test
    test_texts = [
        "for i in range(10): print(i) if i > 5",
        "Cette solution est élégante car elle transforme les données efficacement",
        "I love how this algorithm iterates through the array because it's so clean",
        "The function exists to convert input data, but it might fail sometimes"
    ]
    
    print("🔬 ANALYSE DE COUVERTURE SÉMANTIQUE DHĀTU")
    print("=" * 60)
    
    total_coverage = []
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 TEST {i}: {text}")
        print("-" * 40)
        
        result = analyzer.analyze_text(text)
        total_coverage.append(result['coverage_score']['percentage'])
        
        print(f"Couverture: {result['coverage_score']['percentage']}%")
        print(f"Dhātu détectés: {len(result['dhatu_matches'])}")
        print(f"Gaps sémantiques: {len(result['semantic_gaps'])}")
        
        if result['dhatu_matches']:
            print("Dhātu trouvés:", [m.dhatu for m in result['dhatu_matches']])
        
        if result['semantic_gaps']:
            print("Catégories de gaps:", [g.semantic_category for g in result['semantic_gaps']])
    
    avg_coverage = sum(total_coverage) / len(total_coverage)
    print(f"\n📊 COUVERTURE MOYENNE: {avg_coverage:.1f}%")
    print("\n🎯 Recommandation:", 
          "Excellent" if avg_coverage > 80 else 
          "Bon" if avg_coverage > 60 else 
          "Nécessite amélioration")

if __name__ == "__main__":
    main()
