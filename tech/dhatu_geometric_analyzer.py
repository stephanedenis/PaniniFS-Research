#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur de Relations Geometriques entre Dhatus
Visualisation des relations inclusion/exclusion/egalite
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import json

class RelationType(Enum):
    INCLUSION = "⊆"      # A inclus dans B
    EXCLUSION = "∩∅"     # A et B disjoints
    EQUALITY = "≡"       # A équivalent à B
    INTERSECTION = "∩"   # Overlap partiel
    UNION = "∪"          # Composition

@dataclass
class DhatuVector:
    name: str
    concept: str
    vector: np.ndarray
    magnitude: float
    
@dataclass
class GeometricRelation:
    dhatu_a: str
    dhatu_b: str
    relation_type: RelationType
    strength: float
    geometric_distance: float
    examples: List[str]

class DhatuGeometricAnalyzer:
    """Analyseur géométrique des relations dhātu"""
    
    def __init__(self):
        # 9 Dhātus universels avec vecteurs initiaux
        self.dhatus = {
            'EXIST': DhatuVector('EXIST', 'être/existence', 
                               np.array([1.0, 0.2, 0.1, 0.3, 0.0, 0.1, 0.4, 0.1, 0.2]), 0.0),
            'RELATE': DhatuVector('RELATE', 'relations/spatial',
                                np.array([0.8, 1.0, 0.3, 0.2, 0.1, 0.4, 0.2, 0.1, 0.1]), 0.0),
            'COMM': DhatuVector('COMM', 'communication',
                              np.array([0.2, 0.3, 1.0, 0.7, 0.1, 0.2, 0.3, 0.2, 0.4]), 0.0),
            'EVAL': DhatuVector('EVAL', 'évaluation/cognition',
                              np.array([0.3, 0.2, 0.6, 1.0, 0.2, 0.1, 0.5, 0.1, 0.8]), 0.0),
            'CAUSE': DhatuVector('CAUSE', 'causation/action',
                               np.array([0.1, 0.2, 0.3, 0.4, 1.0, 0.7, 0.3, 0.2, 0.3]), 0.0),
            'FLOW': DhatuVector('FLOW', 'mouvement/flux', 
                              np.array([0.0, 0.4, 0.2, 0.1, 0.6, 1.0, 0.2, 0.5, 0.1]), 0.0),
            'MODAL': DhatuVector('MODAL', 'modalité/possibilité',
                               np.array([0.4, 0.2, 0.4, 0.6, 0.3, 0.2, 1.0, 0.1, 0.5]), 0.0),
            'ITER': DhatuVector('ITER', 'itération/répétition',
                              np.array([0.1, 0.1, 0.2, 0.1, 0.2, 0.4, 0.1, 1.0, 0.2]), 0.0),
            'DECIDE': DhatuVector('DECIDE', 'décision/volition',
                                np.array([0.2, 0.1, 0.3, 0.8, 0.4, 0.1, 0.6, 0.2, 1.0]), 0.0)
        }
        
        # Normalisation des vecteurs (sphère unitaire)
        for dhatu in self.dhatus.values():
            dhatu.vector = dhatu.vector / np.linalg.norm(dhatu.vector)
            dhatu.magnitude = np.linalg.norm(dhatu.vector)
            
        # Relations géométriques connues
        self.known_relations = self._build_known_relations()
        
    def _build_known_relations(self) -> List[GeometricRelation]:
        """Construction des relations géométriques identifiées"""
        return [
            # INCLUSIONS
            GeometricRelation('EXIST', 'RELATE', RelationType.INCLUSION, 0.95, 0.0,
                            ['je suis ici', 'être quelque part', 'located existence']),
            GeometricRelation('COMM', 'EVAL', RelationType.INCLUSION, 0.85, 0.0,
                            ['il dit que', 'cognitive speech', 'evaluated communication']),
            GeometricRelation('DECIDE', 'EVAL', RelationType.INCLUSION, 0.90, 0.0,
                            ['choose after thinking', 'evaluate options', 'cognitive decision']),
            
            # INTERSECTIONS
            GeometricRelation('CAUSE', 'FLOW', RelationType.INTERSECTION, 0.70, 0.0,
                            ['push forward', 'cause movement', 'action with motion']),
            GeometricRelation('ITER', 'FLOW', RelationType.INTERSECTION, 0.65, 0.0,
                            ['walk repeatedly', 'cyclic motion', 'repeated movement']),
            GeometricRelation('MODAL', 'EVAL', RelationType.INTERSECTION, 0.75, 0.0,
                            ['might think', 'possible evaluation', 'modal cognition']),
            
            # EXCLUSIONS
            GeometricRelation('EXIST', 'FLOW', RelationType.EXCLUSION, 0.80, 0.0,
                            ['static being vs movement', 'state vs action']),
            GeometricRelation('DECIDE', 'ITER', RelationType.EXCLUSION, 0.75, 0.0,
                            ['single choice vs repetition', 'punctual vs iterative'])
        ]
    
    def compute_geometric_distance(self, dhatu_a: str, dhatu_b: str) -> float:
        """Calcule distance géométrique entre deux dhātus"""
        vec_a = self.dhatus[dhatu_a].vector
        vec_b = self.dhatus[dhatu_b].vector
        
        # Distance cosinus (optimale pour relations sémantiques)
        cosine_sim = np.dot(vec_a, vec_b)
        return 1.0 - cosine_sim
    
    def test_inclusion(self, dhatu_a: str, dhatu_b: str, threshold: float = 0.3) -> bool:
        """Test si dhātu A inclus dans B (A ⊆ B)"""
        distance = self.compute_geometric_distance(dhatu_a, dhatu_b)
        magnitude_a = np.linalg.norm(self.dhatus[dhatu_a].vector)
        magnitude_b = np.linalg.norm(self.dhatus[dhatu_b].vector)
        
        # A ⊆ B si A "plus petit" et proche de B
        return distance < threshold and magnitude_a <= magnitude_b * 1.1
    
    def test_exclusion(self, dhatu_a: str, dhatu_b: str, threshold: float = 0.7) -> bool:
        """Test si dhātus A et B exclusifs (A ∩ B = ∅)"""
        distance = self.compute_geometric_distance(dhatu_a, dhatu_b)
        return distance > threshold
    
    def test_equality(self, dhatu_a: str, dhatu_b: str, epsilon: float = 0.1) -> bool:
        """Test si dhātus A et B équivalents (A ≡ B)"""
        distance = self.compute_geometric_distance(dhatu_a, dhatu_b)
        return distance < epsilon
    
    def analyze_all_relations(self) -> Dict[str, List[GeometricRelation]]:
        """Analyse toutes les relations géométriques possibles"""
        relations = {
            'inclusions': [],
            'exclusions': [],
            'equalities': [],
            'intersections': []
        }
        
        dhatu_names = list(self.dhatus.keys())
        
        for i, dhatu_a in enumerate(dhatu_names):
            for j, dhatu_b in enumerate(dhatu_names):
                if i >= j:  # Évite duplicatas
                    continue
                    
                distance = self.compute_geometric_distance(dhatu_a, dhatu_b)
                
                # Tests géométriques
                if self.test_inclusion(dhatu_a, dhatu_b):
                    relations['inclusions'].append(
                        GeometricRelation(dhatu_a, dhatu_b, RelationType.INCLUSION, 
                                        1.0 - distance, distance, [])
                    )
                elif self.test_inclusion(dhatu_b, dhatu_a):
                    relations['inclusions'].append(
                        GeometricRelation(dhatu_b, dhatu_a, RelationType.INCLUSION,
                                        1.0 - distance, distance, [])
                    )
                elif self.test_exclusion(dhatu_a, dhatu_b):
                    relations['exclusions'].append(
                        GeometricRelation(dhatu_a, dhatu_b, RelationType.EXCLUSION,
                                        distance, distance, [])
                    )
                elif self.test_equality(dhatu_a, dhatu_b):
                    relations['equalities'].append(
                        GeometricRelation(dhatu_a, dhatu_b, RelationType.EQUALITY,
                                        1.0 - distance, distance, [])
                    )
                else:
                    # Intersection partielle
                    relations['intersections'].append(
                        GeometricRelation(dhatu_a, dhatu_b, RelationType.INTERSECTION,
                                        0.5, distance, [])
                    )
        
        return relations
    
    def create_distance_matrix(self) -> np.ndarray:
        """Crée matrice distances entre tous dhātus"""
        dhatu_names = list(self.dhatus.keys())
        n = len(dhatu_names)
        matrix = np.zeros((n, n), dtype=np.float32)
        
        for i, dhatu_a in enumerate(dhatu_names):
            for j, dhatu_b in enumerate(dhatu_names):
                matrix[i, j] = self.compute_geometric_distance(dhatu_a, dhatu_b)
        
        return matrix
    
    def visualize_dhatu_space(self, save_path: str = None):
        """Visualisation 2D de l'espace dhātu (PCA projection)"""
        from sklearn.decomposition import PCA
        
        # Extraction vecteurs
        vectors = np.array([dhatu.vector for dhatu in self.dhatus.values()])
        names = list(self.dhatus.keys())
        
        # Projection PCA 2D
        pca = PCA(n_components=2)
        vectors_2d = pca.fit_transform(vectors)
        
        # Visualisation
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], 
                            c=range(len(names)), cmap='tab10', s=100)
        
        # Labels
        for i, name in enumerate(names):
            plt.annotate(name, (vectors_2d[i, 0], vectors_2d[i, 1]), 
                        xytext=(5, 5), textcoords='offset points')
        
        plt.title('Espace Géométrique des 9 Dhātus (Projection PCA)')
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def export_for_gpu_pipeline(self, output_path: str):
        """Export données pour pipeline GPU RX 480"""
        export_data = {
            'dhatu_vectors': {
                name: dhatu.vector.tolist() 
                for name, dhatu in self.dhatus.items()
            },
            'distance_matrix': self.create_distance_matrix().tolist(),
            'gpu_config': {
                'vector_dimension': 9,
                'precision': 'float32',
                'texture_format': 'RGBA32F',
                'normalization': 'unit_sphere'
            },
            'relations': {
                'inclusion_threshold': 0.3,
                'exclusion_threshold': 0.7,
                'equality_threshold': 0.1
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Données géométriques exportées vers: {output_path}")

def main():
    """Test de l'analyseur géométrique"""
    analyzer = DhatuGeometricAnalyzer()
    
    print("🔺 ANALYSE GÉOMÉTRIQUE DES RELATIONS DHĀTU")
    print("=" * 50)
    
    # Analyse toutes relations
    relations = analyzer.analyze_all_relations()
    
    print("\n📊 RELATIONS DÉTECTÉES:")
    for relation_type, relation_list in relations.items():
        if relation_list:
            print(f"\n{relation_type.upper()}:")
            for rel in relation_list:
                print(f"  {rel.dhatu_a} {rel.relation_type.value} {rel.dhatu_b} "
                      f"(force: {rel.strength:.2f}, distance: {rel.geometric_distance:.3f})")
    
    # Matrice distances
    print("\n📐 MATRICE DISTANCES:")
    matrix = analyzer.create_distance_matrix()
    dhatu_names = list(analyzer.dhatus.keys())
    
    print("     ", " ".join(f"{name:>6}" for name in dhatu_names))
    for i, name in enumerate(dhatu_names):
        row = " ".join(f"{matrix[i, j]:>6.3f}" for j in range(len(dhatu_names)))
        print(f"{name:>6} {row}")
    
    # Export pour GPU
    output_path = "/home/stephane/GitHub/PaniniFS-Research/tech/dhatu_geometric_data.json"
    analyzer.export_for_gpu_pipeline(output_path)
    
    # Visualisation si matplotlib disponible
    try:
        analyzer.visualize_dhatu_space()
    except ImportError:
        print("\n⚠️ matplotlib non disponible pour visualisation")

if __name__ == "__main__":
    main()