#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur de couverture sémantique mis à jour avec 9 dhātu optimaux
Version post-découverte du 7 septembre 2025
"""
import re
import json
from typing import List, Dict, Set, Any
from dataclasses import dataclass

@dataclass
class DhatuMatch:
    dhatu: str
    pattern: str
    position: int
    context: str

@dataclass 
class SemanticGap:
    text: str
    position: int
    missing_concepts: List[str]

class OptimalDhatuAnalyzer:
    """Analyseur basé sur les 9 dhātu optimaux découverts"""
    
    def __init__(self):
        # 9 DHĀTU OPTIMAUX identifiés le 7 septembre 2025
        self.dhatu_patterns = {
            # Dhātu conservés (5) - Patterns étendus
            'COMM': [
                r'\b(communicat|talk|speak|tell|say|message|signal|transmit|send|receive|exchange|share|inform|discuss|chat|announce)\w*',
                r'\b(dialogue|conversation|report|notify|explain|describe|express|mention|state|declare)\w*'
            ],
            'ITER': [
                r'\b(repeat|iterate|loop|again|cycle|recur|traverse|scan|walk|each|every|all|while|continue)\w*',
                r'\b(process|procedure|step|sequence|series|chain|flow|running|moving|going)\w*'
            ],
            'DECIDE': [
                r'\b(decide|choose|select|pick|if|else|when|switch|case|option|alternative|decision)\w*',
                r'\b(condition|branch|determine|resolve|settle|choice|prefer|want|need|require)\w*'
            ],
            
            # Nouveaux dhātu essentiels (4) - Patterns étendus
            'EXIST': [
                r'\b(exist|be|is|are|was|were|being|presence|available|there|here|system|thing|object)\w*',
                r'\b(create|delete|new|remove|add|insert|define|declare|have|has|had|contain)\w*'
            ],
            'EVAL': [
                r'\b(evaluat|assess|judge|measure|test|check|verify|valid|correct|wrong|better|best)\w*',
                r'\b(quality|good|bad|worse|worst|compare|equal|different|help|improve|enhance)\w*'
            ],
            'CAUSE': [
                r'\b(cause|because|reason|why|trigger|initiate|start|begin|end|result|effect|make)\w*',
                r'\b(due to|leads to|results in|makes|forces|prevents|allows|enable|disable)\w*'
            ],
            'MODAL': [
                r'\b(can|could|may|might|must|should|would|will|shall|possible|impossible|able)\w*',
                r'\b(ability|capability|permission|obligation|necessity|probability|potential)\w*'
            ],
            'RELATE': [
                r'\b(relat|connect|link|join|bind|attach|associate|refer|point|belongs|with|between)\w*',
                r'\b(among|relationship|connection|reference|dependency|about|their|this|that)\w*'
            ],
            'FEEL': [
                r'\b(feel|emotion|happy|sad|angry|fear|love|hate|like|dislike|enjoy|experience)\w*',
                r'\b(sentiment|mood|attitude|preference|reaction|response|satisfaction|comfort)\w*'
            ]
        }
        
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyse un texte avec les 9 dhātu optimaux"""
        matches = []
        covered_positions = set()
        
        for dhatu, patterns in self.dhatu_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    matches.append(DhatuMatch(
                        dhatu=dhatu,
                        pattern=pattern,
                        position=match.start(),
                        context=text[max(0, match.start()-20):match.end()+20]
                    ))
                    covered_positions.update(range(match.start(), match.end()))
        
        # Calculer gaps sémantiques
        gaps = self._find_semantic_gaps(text, covered_positions)
        
        return {
            'text': text,
            'dhatu_matches': matches,
            'semantic_gaps': gaps,
            'coverage_stats': self._calculate_coverage(text, covered_positions),
            'dhatu_distribution': self._dhatu_distribution(matches)
        }
    
    def _find_semantic_gaps(self, text: str, covered_positions: Set[int]) -> List[SemanticGap]:
        """Identifie les gaps sémantiques non couverts par les 9 dhātu"""
        gaps = []
        words = re.finditer(r'\b\w+\b', text)
        
        for word_match in words:
            if not any(pos in covered_positions for pos in range(word_match.start(), word_match.end())):
                word = word_match.group()
                if len(word) > 3:  # Ignorer mots très courts
                    gaps.append(SemanticGap(
                        text=word,
                        position=word_match.start(),
                        missing_concepts=self._suggest_missing_concepts(word)
                    ))
        
        return gaps
    
    def _suggest_missing_concepts(self, word: str) -> List[str]:
        """Suggère concepts manquants pour un mot non couvert"""
        suggestions = []
        
        # Patterns de concepts potentiellement manqués
        concept_patterns = {
            'TIME': r'\b(time|when|before|after|during|now|then|today|yesterday|tomorrow)\b',
            'SPACE': r'\b(where|here|there|location|place|position|near|far|inside|outside)\b',  
            'QUANTITY': r'\b(how much|many|few|more|less|number|amount|size|big|small)\b',
            'IDENTITY': r'\b(who|what|which|this|that|same|different|other|another)\b'
        }
        
        for concept, pattern in concept_patterns.items():
            if re.search(pattern, word, re.IGNORECASE):
                suggestions.append(concept)
        
        return suggestions or ['UNKNOWN']
    
    def _calculate_coverage(self, text: str, covered_positions: Set[int]) -> Dict[str, float]:
        """Calcule statistiques de couverture"""
        total_chars = len(text)
        covered_chars = len(covered_positions)
        
        words = re.findall(r'\b\w+\b', text)
        total_words = len(words)
        
        # Compter mots couverts
        covered_words = 0
        for word_match in re.finditer(r'\b\w+\b', text):
            if any(pos in covered_positions for pos in range(word_match.start(), word_match.end())):
                covered_words += 1
        
        return {
            'char_coverage': covered_chars / total_chars if total_chars > 0 else 0,
            'word_coverage': covered_words / total_words if total_words > 0 else 0,
            'semantic_coverage': (covered_chars / total_chars * 0.7 + covered_words / total_words * 0.3) if total_chars > 0 else 0
        }
    
    def _dhatu_distribution(self, matches: List[DhatuMatch]) -> Dict[str, int]:
        """Distribution des dhātu dans le texte"""
        distribution = {}
        for match in matches:
            distribution[match.dhatu] = distribution.get(match.dhatu, 0) + 1
        return distribution

def test_optimal_dhatu():
    """Test avec les 9 dhātu optimaux"""
    analyzer = OptimalDhatuAnalyzer()
    
    # Exemples multilingues du dossier experiments
    test_cases = [
        "The cat chases the mouse while running quickly.",
        "Le chat chasse la souris en courant rapidement.", 
        "If you can do this task, please communicate the results.",
        "We need to evaluate the decision and repeat the process.",
        "The system exists to help users feel better about their choices."
    ]
    
    results = []
    total_coverage = 0
    
    for test_text in test_cases:
        result = analyzer.analyze_text(test_text)
        results.append(result)
        total_coverage += result['coverage_stats']['semantic_coverage']
        
        print(f"\n📝 Text: {test_text}")
        print(f"🎯 Semantic Coverage: {result['coverage_stats']['semantic_coverage']:.3f}")
        print(f"🧬 Dhātu Found: {list(result['dhatu_distribution'].keys())}")
        print(f"❓ Gaps: {[gap.text for gap in result['semantic_gaps'][:3]]}")
    
    avg_coverage = total_coverage / len(test_cases)
    print(f"\n🏆 AVERAGE SEMANTIC COVERAGE: {avg_coverage:.3f}")
    print(f"📊 Total Test Cases: {len(test_cases)}")
    
    return results, avg_coverage

if __name__ == "__main__":
    print("🧬 OPTIMAL DHĀTU ANALYZER - 9 Dhātu Version")
    print("=" * 50)
    
    results, coverage = test_optimal_dhatu()
    
    print(f"\n✅ OPTIMAL DHĀTU PERFORMANCE:")
    print(f"   Coverage: {coverage:.1%}")
    print(f"   Target: >70% (Original 7 dhātu: ~66.7%)")
    print(f"   Improvement: +{(coverage - 0.667):.1%}")
