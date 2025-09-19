#!/usr/bin/env python3
"""
Prime Base Semantic Systems for Enhanced Dhātu Analysis
Implementing binary, ternary, and higher prime base representations
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
import math

class SemanticPolarity(Enum):
    NEGATIVE = -1
    NEUTRAL = 0 
    POSITIVE = 1

class SemanticIntensity(Enum):
    ABSENT = 0
    WEAK = 1
    MODERATE = 2
    STRONG = 3
    DOMINANT = 4

@dataclass
class DhatuAnalysis:
    dhatu: str
    presence: bool
    polarity: SemanticPolarity
    intensity: SemanticIntensity
    confidence: float
    evidence: List[str]

@dataclass
class PrimeBaseVector:
    base: int
    weights: List[int]
    semantic_analysis: List[DhatuAnalysis]
    ambiguity_score: float

class PrimeBaseDhatuAnalyzer:
    def __init__(self):
        self.dhatus = [
            'RELATE', 'MODAL', 'EXIST', 'EVAL', 'COMM', 
            'CAUSE', 'ITER', 'DECIDE', 'FEEL'
        ]
        
        # Enhanced patterns for scientific content
        self.dhatu_patterns = {
            'RELATE': {
                'positive': [
                    r'\b(relation|relationship|connection|mapping|isomorphism|bijection)',
                    r'\b(associate|correspond|link|connect|correlate)',
                    r'→|↔|⟷|⟶|⟵|↦',  # mathematical arrows
                    r'∈|∉|⊂|⊃|⊆|⊇',  # set relations
                    r'∼|≈|≡|≅',       # equivalence relations
                    r'\bwith respect to\b|\bin terms of\b|\bas a function of\b'
                ],
                'negative': [
                    r'\b(disconnect|separate|independent|unrelated)',
                    r'\b(no relation|not related|unconnected)'
                ]
            },
            'MODAL': {
                'positive': [
                    r'\b(possible|possibly|potential|could|might|may|can)',
                    r'\b(necessary|must|required|essential|sufficient)',
                    r'\b(if and only if|iff|necessary and sufficient)',
                    r'⟺|⟸|⟹|◊|□',  # modal logic symbols
                    r'\bprobability\b|\blikely\b|\bunlikely\b'
                ],
                'negative': [
                    r'\b(impossible|cannot|unable|forbidden)',
                    r'\b(never|no way|not possible)'
                ]
            },
            'EXIST': {
                'positive': [
                    r'\b(exist|exists|existence|there is|there are)',
                    r'\b(given|let|consider|suppose|assume)',
                    r'∃|∀',  # existential and universal quantifiers
                    r'\bfor all\b|\bfor any\b|\bfor some\b|\bthere exists\b',
                    r'\bpresence\b|\bocurrence\b|\binstance\b'
                ],
                'negative': [
                    r'\b(does not exist|non-existent|absence|lack)',
                    r'∄',  # does not exist symbol
                    r'\bno such\b|\bnot found\b|\bmissing\b'
                ]
            },
            'EVAL': {
                'positive': [
                    r'\b(evaluate|assessment|measure|metric|score|rating)',
                    r'\b(compare|comparison|better|worse|optimal|maximum|minimum)',
                    r'\b(performance|accuracy|precision|recall|efficiency)',
                    r'≤|≥|<|>|≠|=',  # comparison operators
                    r'\berror\b|\bloss\b|\bcost\b|\bobjective\b'
                ],
                'negative': [
                    r'\b(incomparable|immeasurable|unquantifiable)'
                ]
            },
            'COMM': {
                'positive': [
                    r'\b(communicate|express|convey|transmit|signal)',
                    r'\b(message|information|data|knowledge|representation)',
                    r'\b(language|syntax|semantics|encoding|decoding)',
                    r'\b(output|input|interface|protocol|format)'
                ],
                'negative': [
                    r'\b(silent|mute|unexpressed|hidden|implicit)'
                ]
            },
            'CAUSE': {
                'positive': [
                    r'\b(cause|effect|consequence|result|outcome|impact)',
                    r'\b(because|since|therefore|thus|hence|leads to)',
                    r'\b(trigger|induce|generate|produce|create)',
                    r'\b(if.*then|implies|entails|follows)'
                ],
                'negative': [
                    r'\b(prevent|block|inhibit|suppress|avoid)',
                    r'\b(no effect|unrelated|coincidence)'
                ]
            },
            'ITER': {
                'positive': [
                    r'\b(iterate|iteration|repeat|cycle|loop|recursion)',
                    r'\b(sequence|series|progression|pattern)',
                    r'\b(again|repeatedly|multiple times|step by step)',
                    r'∑|∏|∫',  # summation, product, integral symbols
                    r'\bfor each\b|\bfor every\b|\ball\b'
                ],
                'negative': [
                    r'\b(once|single|unique|non-recurring|terminal)'
                ]
            },
            'DECIDE': {
                'positive': [
                    r'\b(decide|decision|choice|select|choose|option)',
                    r'\b(algorithm|method|approach|strategy|procedure)',
                    r'\b(determine|conclude|resolve|establish)',
                    r'\b(if|else|otherwise|alternative|branch)'
                ],
                'negative': [
                    r'\b(indecisive|uncertain|ambiguous|random|arbitrary)'
                ]
            },
            'FEEL': {
                'positive': [
                    r'\b(emotion|feeling|sentiment|perception|sense)',
                    r'\b(intuition|impression|experience|subjective)',
                    r'\b(observe|notice|appear|seem|look like)',
                    r'\b(aesthetic|beautiful|elegant|natural|intuitive)'
                ],
                'negative': [
                    r'\b(objective|mechanical|algorithmic|systematic)',
                    r'\b(ignore|overlook|miss|unaware)'
                ]
            }
        }
    
    def analyze_dhatu_in_text(self, text: str, dhatu: str) -> DhatuAnalysis:
        """Analyze presence, polarity, and intensity of a dhātu in text"""
        
        text_lower = text.lower()
        patterns = self.dhatu_patterns.get(dhatu, {'positive': [], 'negative': []})
        
        positive_matches = []
        negative_matches = []
        
        # Find positive indicators
        for pattern in patterns.get('positive', []):
            matches = re.findall(pattern, text_lower)
            positive_matches.extend(matches)
        
        # Find negative indicators  
        for pattern in patterns.get('negative', []):
            matches = re.findall(pattern, text_lower)
            negative_matches.extend(matches)
        
        # Calculate polarity
        pos_count = len(positive_matches)
        neg_count = len(negative_matches)
        
        if pos_count > neg_count:
            polarity = SemanticPolarity.POSITIVE
        elif neg_count > pos_count:
            polarity = SemanticPolarity.NEGATIVE
        else:
            polarity = SemanticPolarity.NEUTRAL
        
        # Calculate intensity based on frequency
        total_matches = pos_count + neg_count
        word_count = len(text.split())
        density = total_matches / max(word_count, 1)
        
        if density >= 0.02:
            intensity = SemanticIntensity.DOMINANT
        elif density >= 0.01:
            intensity = SemanticIntensity.STRONG
        elif density >= 0.005:
            intensity = SemanticIntensity.MODERATE
        elif density > 0:
            intensity = SemanticIntensity.WEAK
        else:
            intensity = SemanticIntensity.ABSENT
        
        # Calculate confidence
        confidence = min(1.0, density * 50)  # Scale to 0-1 range
        
        # Evidence collection
        evidence = positive_matches + negative_matches
        
        return DhatuAnalysis(
            dhatu=dhatu,
            presence=(intensity != SemanticIntensity.ABSENT),
            polarity=polarity,
            intensity=intensity,
            confidence=confidence,
            evidence=evidence[:5]  # Limit evidence to first 5 matches
        )
    
    def compute_binary_vector(self, text: str) -> PrimeBaseVector:
        """Binary representation: 0 = absent, 1 = present"""
        
        analyses = []
        weights = []
        
        for dhatu in self.dhatus:
            analysis = self.analyze_dhatu_in_text(text, dhatu)
            analyses.append(analysis)
            weights.append(1 if analysis.presence else 0)
        
        ambiguity_score = self._calculate_ambiguity(analyses)
        
        return PrimeBaseVector(
            base=2,
            weights=weights,
            semantic_analysis=analyses,
            ambiguity_score=ambiguity_score
        )
    
    def compute_ternary_vector(self, text: str) -> PrimeBaseVector:
        """Ternary representation: -1 = negative, 0 = neutral, 1 = positive"""
        
        analyses = []
        weights = []
        
        for dhatu in self.dhatus:
            analysis = self.analyze_dhatu_in_text(text, dhatu)
            analyses.append(analysis)
            
            if not analysis.presence:
                weights.append(0)
            else:
                weights.append(analysis.polarity.value)
        
        ambiguity_score = self._calculate_ambiguity(analyses)
        
        return PrimeBaseVector(
            base=3,
            weights=weights,
            semantic_analysis=analyses,
            ambiguity_score=ambiguity_score
        )
    
    def compute_quintary_vector(self, text: str) -> PrimeBaseVector:
        """Quintary representation: 0-4 intensity scale"""
        
        analyses = []
        weights = []
        
        for dhatu in self.dhatus:
            analysis = self.analyze_dhatu_in_text(text, dhatu)
            analyses.append(analysis)
            
            # Adjust intensity by polarity
            base_intensity = analysis.intensity.value
            if analysis.polarity == SemanticPolarity.NEGATIVE:
                # Negative polarity reduces effective intensity
                intensity = max(0, base_intensity - 1)
            else:
                intensity = base_intensity
            
            weights.append(intensity)
        
        ambiguity_score = self._calculate_ambiguity(analyses)
        
        return PrimeBaseVector(
            base=5,
            weights=weights,
            semantic_analysis=analyses,
            ambiguity_score=ambiguity_score
        )
    
    def _calculate_ambiguity(self, analyses: List[DhatuAnalysis]) -> float:
        """Calculate overall ambiguity score based on confidence levels"""
        
        if not analyses:
            return 1.0
        
        # Lower average confidence = higher ambiguity
        avg_confidence = sum(a.confidence for a in analyses) / len(analyses)
        ambiguity = 1.0 - avg_confidence
        
        # Penalize conflicting polarities
        polarity_conflicts = 0
        for analysis in analyses:
            if analysis.presence and analysis.polarity == SemanticPolarity.NEUTRAL:
                polarity_conflicts += 1
        
        conflict_penalty = polarity_conflicts / len(analyses)
        ambiguity += conflict_penalty * 0.5
        
        return min(1.0, ambiguity)
    
    def analyze_corpus(self, corpus_file: Path) -> Dict[str, Any]:
        """Analyze entire corpus with all prime base systems"""
        
        print("🔬 Analyzing corpus with prime base systems...")
        
        with open(corpus_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        results = {
            'corpus_info': {
                'total_papers': len(papers),
                'analysis_timestamp': str(pd.Timestamp.now())
            },
            'prime_base_analyses': {},
            'comparative_statistics': {}
        }
        
        for i, paper in enumerate(papers):
            print(f"📄 Analyzing paper {i+1}/{len(papers)}: {paper['title'][:50]}...")
            
            text = paper['title'] + " " + paper['abstract']
            
            # Compute all base systems
            binary_vec = self.compute_binary_vector(text)
            ternary_vec = self.compute_ternary_vector(text)
            quintary_vec = self.compute_quintary_vector(text)
            
            paper_results = {
                'binary': {
                    'weights': binary_vec.weights,
                    'ambiguity': binary_vec.ambiguity_score,
                    'active_dhatus': sum(binary_vec.weights)
                },
                'ternary': {
                    'weights': ternary_vec.weights,
                    'ambiguity': ternary_vec.ambiguity_score,
                    'polarity_distribution': {
                        'positive': sum(1 for w in ternary_vec.weights if w > 0),
                        'neutral': sum(1 for w in ternary_vec.weights if w == 0),
                        'negative': sum(1 for w in ternary_vec.weights if w < 0)
                    }
                },
                'quintary': {
                    'weights': quintary_vec.weights,
                    'ambiguity': quintary_vec.ambiguity_score,
                    'intensity_distribution': {
                        f'level_{i}': sum(1 for w in quintary_vec.weights if w == i)
                        for i in range(5)
                    }
                },
                'detailed_analysis': [
                    {
                        'dhatu': analysis.dhatu,
                        'presence': analysis.presence,
                        'polarity': analysis.polarity.name,
                        'intensity': analysis.intensity.name,
                        'confidence': analysis.confidence,
                        'evidence': analysis.evidence
                    }
                    for analysis in binary_vec.semantic_analysis
                ]
            }
            
            results['prime_base_analyses'][paper['id']] = paper_results
        
        # Calculate comparative statistics
        results['comparative_statistics'] = self._calculate_comparative_stats(results['prime_base_analyses'])
        
        return results
    
    def _calculate_comparative_stats(self, analyses: Dict) -> Dict[str, Any]:
        """Calculate statistics comparing different base systems"""
        
        stats = {
            'ambiguity_comparison': {},
            'information_density': {},
            'dhatu_activation_patterns': {}
        }
        
        binary_ambiguities = [data['binary']['ambiguity'] for data in analyses.values()]
        ternary_ambiguities = [data['ternary']['ambiguity'] for data in analyses.values()]
        quintary_ambiguities = [data['quintary']['ambiguity'] for data in analyses.values()]
        
        stats['ambiguity_comparison'] = {
            'binary_avg': np.mean(binary_ambiguities),
            'ternary_avg': np.mean(ternary_ambiguities),
            'quintary_avg': np.mean(quintary_ambiguities),
            'most_discriminative': 'quintary' if np.mean(quintary_ambiguities) < min(np.mean(binary_ambiguities), np.mean(ternary_ambiguities)) else 'ternary'
        }
        
        # Information density (non-zero weights per paper)
        binary_densities = [data['binary']['active_dhatus'] for data in analyses.values()]
        
        stats['information_density'] = {
            'binary_avg_active': np.mean(binary_densities),
            'max_possible': 9,  # total dhatus
            'activation_rate': np.mean(binary_densities) / 9
        }
        
        return stats


def main():
    """Main analysis function"""
    
    print("🚀 Prime Base Semantic Analysis Starting...")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = PrimeBaseDhatuAnalyzer()
    
    # Analyze corpus
    corpus_file = Path('./corpus_simple/corpus.json')
    
    if not corpus_file.exists():
        print("❌ Corpus file not found. Please run corpus collection first.")
        return
    
    results = analyzer.analyze_corpus(corpus_file)
    
    # Save results
    output_file = Path('./corpus_simple/prime_base_analysis.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Analysis saved to: {output_file}")
    
    # Print summary
    stats = results['comparative_statistics']
    print(f"\n📊 Analysis Summary:")
    print(f"   Papers analyzed: {results['corpus_info']['total_papers']}")
    print(f"   Average ambiguity - Binary: {stats['ambiguity_comparison']['binary_avg']:.3f}")
    print(f"   Average ambiguity - Ternary: {stats['ambiguity_comparison']['ternary_avg']:.3f}")
    print(f"   Average ambiguity - Quintary: {stats['ambiguity_comparison']['quintary_avg']:.3f}")
    print(f"   Most discriminative: {stats['ambiguity_comparison']['most_discriminative']}")
    print(f"   Dhātu activation rate: {stats['information_density']['activation_rate']:.2%}")


if __name__ == "__main__":
    # Import pandas for timestamps if available
    try:
        import pandas as pd
    except ImportError:
        import datetime
        pd = type('MockPd', (), {'Timestamp': type('MockTimestamp', (), {'now': lambda: datetime.datetime.now()})})()
    
    main()