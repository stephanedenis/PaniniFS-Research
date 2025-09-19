#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Prime Base Semantic System for Dhātu Analysis
Système avancé de bases nombres premiers pour analyse sémantique dhātu
avec gradation et polarisation des ambiguïtés
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import math


class SemanticPolarization(Enum):
    """Types de polarisation sémantique"""
    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1
    AMBIGUOUS = 0.5


@dataclass
class DhatuActivation:
    """Activation dhātu avec pondération et ambiguïté"""
    dhatu_name: str
    base_activation: float
    polarization: SemanticPolarization
    ambiguity_score: float
    confidence: float


class PrimeBaseSemanticAnalyzer:
    """Analyseur sémantique basé sur les bases de nombres premiers"""
    
    def __init__(self):
        # Les 9 dhātu universels optimaux
        self.dhatu_set = [
            'RELATE', 'MODAL', 'EXIST', 'EVAL', 'COMM', 
            'CAUSE', 'ITER', 'DECIDE', 'FEEL'
        ]
        
        # Bases de nombres premiers pour différentes granularités
        self.prime_bases = {
            'binary': 2,
            'ternary': 3, 
            'quintary': 5,
            'septenary': 7,
            'undenary': 11
        }
        
        # Patterns sémantiques par dhātu pour détection
        self.dhatu_patterns = self._build_dhatu_patterns()
        
    def _build_dhatu_patterns(self) -> Dict[str, List[str]]:
        """Construction des patterns sémantiques par dhātu"""
        return {
            'RELATE': ['with', 'between', 'connect', 'link', 'relationship', 
                      'among', 'together', 'correlation', 'association'],
            'MODAL': ['can', 'could', 'may', 'might', 'should', 'must', 
                     'possible', 'necessary', 'required', 'optional'],
            'EXIST': ['is', 'are', 'be', 'being', 'exist', 'present', 
                     'there', 'state', 'condition', 'status'],
            'EVAL': ['better', 'worse', 'good', 'bad', 'compare', 'measure',
                    'quality', 'performance', 'assess', 'evaluate'],
            'COMM': ['say', 'tell', 'speak', 'write', 'communicate', 
                    'express', 'message', 'language', 'word'],
            'CAUSE': ['because', 'since', 'due', 'reason', 'cause', 'effect',
                     'result', 'consequence', 'lead', 'trigger'],
            'ITER': ['repeat', 'again', 'iterate', 'loop', 'cycle', 
                    'continue', 'recurring', 'frequent', 'multiple'],
            'DECIDE': ['choose', 'select', 'decide', 'determine', 'pick',
                      'option', 'alternative', 'decision', 'choice'],
            'FEEL': ['feel', 'emotion', 'sense', 'perceive', 'experience',
                    'sentiment', 'mood', 'impression', 'intuition']
        }
    
    def analyze_text_semantic_spectrum(self, text: str) -> Dict[str, Any]:
        """Analyse complète du spectre sémantique avec bases premiers"""
        
        results = {
            'text_length': len(text),
            'dhatu_activations': {},
            'prime_base_analyses': {},
            'semantic_ambiguity': {},
            'polarization_analysis': {}
        }
        
        # Analyse pour chaque base de nombres premiers
        for base_name, base_value in self.prime_bases.items():
            base_analysis = self._analyze_with_prime_base(text, base_value)
            results['prime_base_analyses'][base_name] = base_analysis
        
        # Analyse des activations dhātu
        dhatu_activations = self._detect_dhatu_activations(text)
        results['dhatu_activations'] = dhatu_activations
        
        # Analyse des ambiguïtés sémantiques
        ambiguity_analysis = self._analyze_semantic_ambiguity(text, dhatu_activations)
        results['semantic_ambiguity'] = ambiguity_analysis
        
        # Analyse de polarisation
        polarization_analysis = self._analyze_polarization(text, dhatu_activations)
        results['polarization_analysis'] = polarization_analysis
        
        return results
    
    def _analyze_with_prime_base(self, text: str, base: int) -> Dict[str, Any]:
        """Analyse avec une base de nombres premiers spécifique"""
        
        words = text.lower().split()
        dhatu_weights = [0] * len(self.dhatu_set)
        
        # Attribution poids selon base premier
        for i, word in enumerate(words):
            for j, dhatu in enumerate(self.dhatu_set):
                if any(pattern in word for pattern in self.dhatu_patterns[dhatu]):
                    # Calcul pondération basée sur position et base premier
                    position_weight = (i % base) / base
                    dhatu_weights[j] += 1 + position_weight
        
        # Normalisation selon la base
        total_weight = sum(dhatu_weights)
        if total_weight > 0:
            normalized_weights = [w / total_weight for w in dhatu_weights]
        else:
            normalized_weights = [0] * len(self.dhatu_set)
        
        # Calcul distribution selon base premier
        base_distribution = {}
        for i, weight in enumerate(normalized_weights):
            if weight > 0:
                # Mappage sur échelle base premier avec gradation
                base_value = int(weight * (base - 1)) if weight < 1 else base - 1
                base_distribution[self.dhatu_set[i]] = base_value
        
        # Calcul ambiguïté selon base
        ambiguity_measure = self._calculate_base_ambiguity(normalized_weights, base)
        
        return {
            'base': base,
            'raw_weights': dhatu_weights,
            'normalized_weights': normalized_weights,
            'base_distribution': base_distribution,
            'ambiguity_measure': ambiguity_measure,
            'active_dhatus': len([w for w in normalized_weights if w > 0.1])
        }
    
    def _detect_dhatu_activations(self, text: str) -> Dict[str, DhatuActivation]:
        """Détection fine des activations dhātu avec pondération"""
        
        activations = {}
        words = text.lower().split()
        
        for dhatu in self.dhatu_set:
            patterns = self.dhatu_patterns[dhatu]
            matches = []
            
            # Recherche patterns dans texte
            for word in words:
                for pattern in patterns:
                    if pattern in word:
                        matches.append((word, pattern))
            
            if matches:
                # Calcul activation de base
                base_activation = len(matches) / len(words)
                
                # Détermination polarisation
                polarization = self._determine_polarization(text, matches)
                
                # Calcul score ambiguïté
                ambiguity_score = self._calculate_ambiguity_score(matches, words)
                
                # Calcul confiance
                confidence = min(1.0, len(matches) / 3.0)  # Confiance basée sur nombre matches
                
                activations[dhatu] = DhatuActivation(
                    dhatu_name=dhatu,
                    base_activation=base_activation,
                    polarization=polarization,
                    ambiguity_score=ambiguity_score,
                    confidence=confidence
                )
        
        return activations
    
    def _determine_polarization(self, text: str, matches: List[Tuple[str, str]]) -> SemanticPolarization:
        """Détermine la polarisation sémantique"""
        
        # Mots indicateurs de polarisation
        positive_indicators = ['good', 'better', 'improve', 'enhance', 'positive', 'success']
        negative_indicators = ['bad', 'worse', 'fail', 'error', 'negative', 'problem']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for indicator in positive_indicators if indicator in text_lower)
        neg_count = sum(1 for indicator in negative_indicators if indicator in text_lower)
        
        if pos_count > neg_count:
            return SemanticPolarization.POSITIVE
        elif neg_count > pos_count:
            return SemanticPolarization.NEGATIVE
        elif pos_count > 0 or neg_count > 0:
            return SemanticPolarization.AMBIGUOUS
        else:
            return SemanticPolarization.NEUTRAL
    
    def _calculate_ambiguity_score(self, matches: List[Tuple[str, str]], words: List[str]) -> float:
        """Calcule le score d'ambiguïté sémantique"""
        
        if not matches:
            return 0.0
        
        # Diversité des patterns matchés
        unique_patterns = len(set(match[1] for match in matches))
        total_patterns = len(matches)
        
        # Dispersion dans le texte
        match_positions = []
        for match_word, _ in matches:
            positions = [i for i, word in enumerate(words) if match_word in word]
            match_positions.extend(positions)
        
        if len(match_positions) > 1:
            position_variance = np.var(match_positions) / len(words)**2
        else:
            position_variance = 0
        
        # Score ambiguïté combiné
        pattern_diversity = unique_patterns / max(1, total_patterns)
        ambiguity_score = (pattern_diversity + position_variance) / 2
        
        return min(1.0, ambiguity_score)
    
    def _calculate_base_ambiguity(self, weights: List[float], base: int) -> float:
        """Calcule mesure d'ambiguïté selon base premier"""
        
        if not any(weights):
            return 0.0
        
        # Entropie normalisée selon base
        entropy = 0
        for weight in weights:
            if weight > 0:
                entropy -= weight * math.log(weight, base)
        
        # Normalisation par entropie maximale possible
        max_entropy = math.log(len([w for w in weights if w > 0]), base)
        
        return entropy / max_entropy if max_entropy > 0 else 0
    
    def _analyze_semantic_ambiguity(self, text: str, activations: Dict[str, DhatuActivation]) -> Dict[str, Any]:
        """Analyse globale des ambiguïtés sémantiques"""
        
        if not activations:
            return {'global_ambiguity': 0, 'ambiguity_sources': [], 'resolution_confidence': 0}
        
        # Ambiguïté globale
        ambiguity_scores = [activation.ambiguity_score for activation in activations.values()]
        global_ambiguity = np.mean(ambiguity_scores)
        
        # Sources d'ambiguïté
        ambiguity_sources = []
        for dhatu, activation in activations.items():
            if activation.ambiguity_score > 0.5:
                ambiguity_sources.append({
                    'dhatu': dhatu,
                    'score': activation.ambiguity_score,
                    'polarization': activation.polarization.name
                })
        
        # Confiance de résolution
        confidences = [activation.confidence for activation in activations.values()]
        resolution_confidence = np.mean(confidences)
        
        return {
            'global_ambiguity': global_ambiguity,
            'ambiguity_sources': ambiguity_sources,
            'resolution_confidence': resolution_confidence,
            'ambiguous_dhatus_count': len(ambiguity_sources)
        }
    
    def _analyze_polarization(self, text: str, activations: Dict[str, DhatuActivation]) -> Dict[str, Any]:
        """Analyse de la polarisation sémantique globale"""
        
        if not activations:
            return {'dominant_polarization': 'NEUTRAL', 'polarization_distribution': {}, 'polarization_strength': 0}
        
        # Distribution polarisation
        polarization_counts = {}
        for activation in activations.values():
            pol_name = activation.polarization.name
            polarization_counts[pol_name] = polarization_counts.get(pol_name, 0) + 1
        
        # Polarisation dominante
        dominant_polarization = max(polarization_counts.items(), key=lambda x: x[1])[0]
        
        # Force de polarisation
        total_activations = len(activations)
        dominant_count = polarization_counts[dominant_polarization]
        polarization_strength = dominant_count / total_activations
        
        return {
            'dominant_polarization': dominant_polarization,
            'polarization_distribution': polarization_counts,
            'polarization_strength': polarization_strength,
            'is_polarized': polarization_strength > 0.6
        }


def main():
    """Test du système de bases nombres premiers"""
    
    print("Système Avancé Bases Nombres Premiers - Analyse Dhātu")
    print("=" * 60)
    
    # Texte de test avec ambiguïtés
    test_text = """
    This analysis may compare different approaches to evaluate the relationship 
    between mathematical concepts. We can decide which method better represents 
    the iterative process that causes improved understanding. The communication 
    of these ideas feels important for future research.
    """
    
    # Création analyseur
    analyzer = PrimeBaseSemanticAnalyzer()
    
    # Analyse complète
    results = analyzer.analyze_text_semantic_spectrum(test_text)
    
    print(f"Texte analysé: {len(test_text)} caractères")
    print(f"Dhātu activés: {len(results['dhatu_activations'])}")
    
    # Résultats bases premiers
    print("\nAnalyse Bases Nombres Premiers:")
    for base_name, analysis in results['prime_base_analyses'].items():
        print(f"  {base_name} (base {analysis['base']}): {analysis['active_dhatus']} dhātu actifs, ambiguïté {analysis['ambiguity_measure']:.3f}")
    
    # Ambiguïtés détectées
    ambiguity = results['semantic_ambiguity']
    print(f"\nAmbiguïté globale: {ambiguity['global_ambiguity']:.3f}")
    print(f"Sources d'ambiguïté: {ambiguity['ambiguous_dhatus_count']}")
    
    # Polarisation
    polarization = results['polarization_analysis']
    print(f"\nPolarisation dominante: {polarization['dominant_polarization']}")
    print(f"Force polarisation: {polarization['polarization_strength']:.3f}")
    
    # Sauvegarde résultats
    with open('semantic_analysis_advanced.json', 'w') as f:
        # Conversion des objets pour JSON
        json_results = {}
        for key, value in results.items():
            if key == 'dhatu_activations':
                json_results[key] = {
                    dhatu: {
                        'base_activation': act.base_activation,
                        'polarization': act.polarization.name,
                        'ambiguity_score': act.ambiguity_score,
                        'confidence': act.confidence
                    } for dhatu, act in value.items()
                }
            else:
                json_results[key] = value
        
        json.dump(json_results, f, indent=2)
    
    print("\nAnalyse sauvegardée: semantic_analysis_advanced.json")
    print("Système de bases nombres premiers opérationnel ✓")


if __name__ == "__main__":
    main()