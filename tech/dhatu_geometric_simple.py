# -*- coding: utf-8 -*-
"""
Analyseur de Relations Geometriques entre Dhatus - Version Simple
Modelisation des relations inclusion/exclusion/egalite comme geometries
"""

import numpy as np
import json
from enum import Enum

class RelationType(Enum):
    INCLUSION = "⊆"      # A inclus dans B
    EXCLUSION = "∩∅"     # A et B disjoints  
    EQUALITY = "≡"       # A equivalent a B
    INTERSECTION = "∩"   # Overlap partiel

class DhatuGeometricAnalyzer:
    """Analyseur geometrique des relations dhatu optimise pour GPU RX 480"""
    
    def __init__(self):
        # 9 Dhatus universels avec vecteurs 9D (float32)
        self.dhatus = {
            'EXIST': {
                'concept': 'etre/existence',
                'vector': np.array([1.0, 0.2, 0.1, 0.3, 0.0, 0.1, 0.4, 0.1, 0.2], dtype=np.float32)
            },
            'RELATE': {
                'concept': 'relations/spatial', 
                'vector': np.array([0.8, 1.0, 0.3, 0.2, 0.1, 0.4, 0.2, 0.1, 0.1], dtype=np.float32)
            },
            'COMM': {
                'concept': 'communication',
                'vector': np.array([0.2, 0.3, 1.0, 0.7, 0.1, 0.2, 0.3, 0.2, 0.4], dtype=np.float32)
            },
            'EVAL': {
                'concept': 'evaluation/cognition',
                'vector': np.array([0.3, 0.2, 0.6, 1.0, 0.2, 0.1, 0.5, 0.1, 0.8], dtype=np.float32)
            },
            'CAUSE': {
                'concept': 'causation/action',
                'vector': np.array([0.1, 0.2, 0.3, 0.4, 1.0, 0.7, 0.3, 0.2, 0.3], dtype=np.float32)
            },
            'FLOW': {
                'concept': 'mouvement/flux',
                'vector': np.array([0.0, 0.4, 0.2, 0.1, 0.6, 1.0, 0.2, 0.5, 0.1], dtype=np.float32)
            },
            'MODAL': {
                'concept': 'modalite/possibilite',
                'vector': np.array([0.4, 0.2, 0.4, 0.6, 0.3, 0.2, 1.0, 0.1, 0.5], dtype=np.float32)
            },
            'ITER': {
                'concept': 'iteration/repetition',
                'vector': np.array([0.1, 0.1, 0.2, 0.1, 0.2, 0.4, 0.1, 1.0, 0.2], dtype=np.float32)
            },
            'DECIDE': {
                'concept': 'decision/volition',
                'vector': np.array([0.2, 0.1, 0.3, 0.8, 0.4, 0.1, 0.6, 0.2, 1.0], dtype=np.float32)
            }
        }
        
        # Normalisation sur sphere unitaire (optimal pour GPU)
        for dhatu in self.dhatus.values():
            norm = np.linalg.norm(dhatu['vector'])
            if norm > 0:
                dhatu['vector'] = dhatu['vector'] / norm
        
        # Relations theoriques connues
        self.known_relations = {
            'inclusions': [
                ('EXIST', 'RELATE', 0.95, 'Existence implique position'),
                ('COMM', 'EVAL', 0.85, 'Communication implique cognition'),
                ('DECIDE', 'EVAL', 0.90, 'Decision implique evaluation')
            ],
            'intersections': [
                ('CAUSE', 'FLOW', 0.70, 'Actions causales avec mouvement'),
                ('ITER', 'FLOW', 0.65, 'Mouvements repetitifs'),
                ('MODAL', 'EVAL', 0.75, 'Modalite evaluative')
            ],
            'exclusions': [
                ('EXIST', 'FLOW', 0.80, 'Etre statique vs mouvement'),
                ('DECIDE', 'ITER', 0.75, 'Decision ponctuelle vs repetition')
            ]
        }
    
    def cosine_distance(self, dhatu_a, dhatu_b):
        """Distance cosinus entre deux dhatus (optimal pour semantique)"""
        vec_a = self.dhatus[dhatu_a]['vector']
        vec_b = self.dhatus[dhatu_b]['vector']
        
        cosine_sim = np.dot(vec_a, vec_b)
        return 1.0 - cosine_sim
    
    def test_inclusion(self, dhatu_a, dhatu_b, threshold=0.3):
        """Test inclusion geometrique A ⊆ B"""
        distance = self.cosine_distance(dhatu_a, dhatu_b)
        
        # Criteres inclusion:
        # 1. Distance faible (concepts proches)
        # 2. Magnitude A <= Magnitude B (A plus specifique)
        mag_a = np.linalg.norm(self.dhatus[dhatu_a]['vector'])
        mag_b = np.linalg.norm(self.dhatus[dhatu_b]['vector'])
        
        return distance < threshold and mag_a <= mag_b * 1.1
    
    def test_exclusion(self, dhatu_a, dhatu_b, threshold=0.7):
        """Test exclusion geometrique A ∩ B = ∅"""
        distance = self.cosine_distance(dhatu_a, dhatu_b)
        return distance > threshold
    
    def test_equality(self, dhatu_a, dhatu_b, epsilon=0.1):
        """Test egalite geometrique A ≡ B"""
        distance = self.cosine_distance(dhatu_a, dhatu_b)
        return distance < epsilon
    
    def analyze_all_relations(self):
        """Analyse systematique toutes relations possibles"""
        dhatu_names = list(self.dhatus.keys())
        results = {
            'inclusions': [],
            'exclusions': [], 
            'equalities': [],
            'intersections': []
        }
        
        for i, dhatu_a in enumerate(dhatu_names):
            for j, dhatu_b in enumerate(dhatu_names):
                if i >= j:  # Evite duplicatas et auto-relations
                    continue
                
                distance = self.cosine_distance(dhatu_a, dhatu_b)
                
                # Classification geometrique
                if self.test_inclusion(dhatu_a, dhatu_b):
                    results['inclusions'].append({
                        'dhatu_a': dhatu_a,
                        'dhatu_b': dhatu_b,
                        'relation': f'{dhatu_a} ⊆ {dhatu_b}',
                        'strength': 1.0 - distance,
                        'distance': distance
                    })
                elif self.test_inclusion(dhatu_b, dhatu_a):
                    results['inclusions'].append({
                        'dhatu_a': dhatu_b,
                        'dhatu_b': dhatu_a,
                        'relation': f'{dhatu_b} ⊆ {dhatu_a}',
                        'strength': 1.0 - distance,
                        'distance': distance
                    })
                elif self.test_exclusion(dhatu_a, dhatu_b):
                    results['exclusions'].append({
                        'dhatu_a': dhatu_a,
                        'dhatu_b': dhatu_b,
                        'relation': f'{dhatu_a} ∩ {dhatu_b} = ∅',
                        'strength': distance,
                        'distance': distance
                    })
                elif self.test_equality(dhatu_a, dhatu_b):
                    results['equalities'].append({
                        'dhatu_a': dhatu_a,
                        'dhatu_b': dhatu_b,
                        'relation': f'{dhatu_a} ≡ {dhatu_b}',
                        'strength': 1.0 - distance,
                        'distance': distance
                    })
                else:
                    # Intersection partielle par defaut
                    results['intersections'].append({
                        'dhatu_a': dhatu_a,
                        'dhatu_b': dhatu_b,
                        'relation': f'{dhatu_a} ∩ {dhatu_b}',
                        'strength': 0.5,
                        'distance': distance
                    })
        
        return results
    
    def create_distance_matrix(self):
        """Matrice distances pour GPU pipeline"""
        dhatu_names = list(self.dhatus.keys())
        n = len(dhatu_names)
        matrix = np.zeros((n, n), dtype=np.float32)
        
        for i, dhatu_a in enumerate(dhatu_names):
            for j, dhatu_b in enumerate(dhatu_names):
                if i == j:
                    matrix[i, j] = 0.0  # Distance a soi-meme
                else:
                    matrix[i, j] = self.cosine_distance(dhatu_a, dhatu_b)
        
        return matrix, dhatu_names
    
    def export_gpu_data(self, output_file):
        """Export donnees pour pipeline GPU RX 480"""
        matrix, names = self.create_distance_matrix()
        
        gpu_data = {
            'metadata': {
                'dhatu_count': len(self.dhatus),
                'vector_dimension': 9,
                'precision': 'float32',
                'gpu_target': 'RX 480 Polaris',
                'optimization': 'cosine_distance'
            },
            'dhatus': {
                name: {
                    'concept': data['concept'],
                    'vector': data['vector'].tolist(),
                    'magnitude': float(np.linalg.norm(data['vector']))
                }
                for name, data in self.dhatus.items()
            },
            'distance_matrix': matrix.tolist(),
            'dhatu_names': names,
            'gpu_config': {
                'texture_format': 'RGBA32F',  # 4 x float32 per texel
                'texture_size': '512x512',    # Support jusqu'a 262k vectors
                'shader_precision': 'highp',
                'normalization': 'unit_sphere'
            },
            'geometric_thresholds': {
                'inclusion': 0.3,
                'exclusion': 0.7,
                'equality': 0.1
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(gpu_data, f, indent=2, ensure_ascii=False)
        
        return gpu_data

def main():
    """Test analyseur geometrique dhatu"""
    print("🔺 ANALYSE GEOMETRIQUE RELATIONS DHATU")
    print("=" * 60)
    
    analyzer = DhatuGeometricAnalyzer()
    
    # Analyse relations
    relations = analyzer.analyze_all_relations()
    
    print("\n📊 RELATIONS GEOMETRIQUES DETECTEES:")
    for rel_type, rel_list in relations.items():
        if rel_list:
            print(f"\n{rel_type.upper()} ({len(rel_list)} relations):")
            for rel in rel_list[:5]:  # Top 5 par type
                print(f"  {rel['relation']} "
                      f"(force: {rel['strength']:.3f}, dist: {rel['distance']:.3f})")
    
    # Matrice distances
    print("\n📐 MATRICE DISTANCES COSINUS:")
    matrix, names = analyzer.create_distance_matrix()
    
    # Affichage matrice condensee
    print("       " + " ".join(f"{name[:4]:>6}" for name in names))
    for i, name in enumerate(names):
        row = " ".join(f"{matrix[i, j]:6.3f}" for j in range(len(names)))
        print(f"{name[:6]:>6} {row}")
    
    # Relations connues vs detectees
    print("\n🎯 VALIDATION RELATIONS THEORIQUES:")
    for rel_type, known_rels in analyzer.known_relations.items():
        print(f"\n{rel_type.upper()}:")
        for dhatu_a, dhatu_b, expected_strength, description in known_rels:
            actual_distance = analyzer.cosine_distance(dhatu_a, dhatu_b)
            actual_strength = 1.0 - actual_distance
            
            validation = "✅" if abs(actual_strength - expected_strength) < 0.2 else "⚠️"
            print(f"  {validation} {dhatu_a}-{dhatu_b}: "
                  f"theo={expected_strength:.2f} vs reel={actual_strength:.2f} "
                  f"({description})")
    
    # Export pour GPU
    output_file = "/home/stephane/GitHub/PaniniFS-Research/tech/dhatu_geometric_data.json"
    gpu_data = analyzer.export_gpu_data(output_file)
    
    print(f"\n🚀 DONNEES GPU EXPORTEES: {output_file}")
    print(f"   Format: {gpu_data['gpu_config']['texture_format']}")
    print(f"   Taille: {gpu_data['gpu_config']['texture_size']}")
    print(f"   Precision: {gpu_data['metadata']['precision']}")
    
    # Performance estimation RX 480
    dhatu_count = len(analyzer.dhatus)
    matrix_size = dhatu_count * dhatu_count
    
    rx480_specs = {
        'texture_operations_per_sec': 45_000_000_000,  # 45 Gtex/s
        'compute_units': 36,
        'memory_bandwidth': 256  # GB/s
    }
    
    estimated_throughput = rx480_specs['texture_operations_per_sec'] / matrix_size
    
    print(f"\n⚡ PERFORMANCE ESTIMEE RX 480:")
    print(f"   Relations/sec: {estimated_throughput:,.0f}")
    print(f"   Matrices 9x9/sec: {estimated_throughput/81:,.0f}")
    print(f"   Corpus comparisons: {estimated_throughput/1000:,.0f} k-texts/sec")

if __name__ == "__main__":
    main()