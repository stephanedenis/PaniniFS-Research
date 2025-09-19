#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUDA/GPU Kernels for Dhātu Processing
High-performance GPU implementations of core dhātu algorithms
"""

import numpy as np
import time
import json
from pathlib import Path
from typing import Dict, List, Any
import hashlib

try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    print("⚠️  CuPy not available - falling back to NumPy CPU implementation")
    import numpy as cp
    GPU_AVAILABLE = False


class DhatuGPUKernels:
    """High-performance GPU kernels for dhātu processing"""
    
    def __init__(self, use_gpu=True):
        self.use_gpu = use_gpu and GPU_AVAILABLE
        self.device_type = "GPU" if self.use_gpu else "CPU"
        
        # Dhātu names for vectorization
        self.dhatu_names = [
            'RELATE', 'MODAL', 'EXIST', 'EVAL', 'COMM', 
            'CAUSE', 'ITER', 'DECIDE', 'FEEL'
        ]
        
        # Prime numbers for base computations
        self.prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        
        print(f"🔧 Initializing Dhātu GPU Kernels ({self.device_type})")
        
    def benchmark_dhatu_vectorization(self, texts: List[str], iterations=100) -> Dict[str, Any]:
        """Benchmark dhātu vectorization performance"""
        
        print(f"\n⚡ BENCHMARKING DHĀTU VECTORIZATION ({self.device_type})")
        print("=" * 55)
        
        num_texts = len(texts)
        num_dhatus = len(self.dhatu_names)
        
        # Prepare data
        if self.use_gpu:
            # GPU implementation
            start_time = time.time()
            
            for _ in range(iterations):
                vectors = self._gpu_dhatu_vectorization(texts)
                
            gpu_time = (time.time() - start_time) / iterations
            
            # Transfer result back to CPU for verification
            if hasattr(vectors, 'get'):
                vectors_cpu = vectors.get()
            else:
                vectors_cpu = vectors
                
        else:
            # CPU implementation
            start_time = time.time()
            
            for _ in range(iterations):
                vectors_cpu = self._cpu_dhatu_vectorization(texts)
                
            gpu_time = (time.time() - start_time) / iterations
        
        # Performance metrics
        texts_per_second = num_texts / gpu_time
        time_per_text_ms = (gpu_time / num_texts) * 1000
        
        benchmark_results = {
            'device_type': self.device_type,
            'num_texts': num_texts,
            'num_dhatus': num_dhatus,
            'iterations': iterations,
            'total_time_seconds': gpu_time,
            'texts_per_second': texts_per_second,
            'time_per_text_ms': time_per_text_ms,
            'vectors_shape': vectors_cpu.shape,
            'memory_usage_mb': vectors_cpu.nbytes / (1024 * 1024),
            'sample_vector': vectors_cpu[0].tolist() if len(vectors_cpu) > 0 else []
        }
        
        return benchmark_results
    
    def _gpu_dhatu_vectorization(self, texts: List[str]) -> cp.ndarray:
        """GPU-accelerated dhātu vectorization using CuPy"""
        
        num_texts = len(texts)
        num_dhatus = len(self.dhatu_names)
        
        # Initialize output matrix on GPU
        vectors = cp.zeros((num_texts, num_dhatus), dtype=cp.float32)
        
        # Process each text-dhātu combination
        for text_idx, text in enumerate(texts):
            for dhatu_idx, dhatu in enumerate(self.dhatu_names):
                # Compute hash on CPU (crypto operations not easily GPU-accelerated)
                combined_input = f"{dhatu}::{text}".encode('utf-8')
                hash_obj = hashlib.sha256(combined_input)
                hash_bytes = hash_obj.digest()
                
                # Extract weight from hash bytes
                weight = (hash_bytes[0] + hash_bytes[5] + hash_bytes[13] + 
                         hash_bytes[21] + hash_bytes[29]) / 1024.0
                
                vectors[text_idx, dhatu_idx] = weight
        
        # L1 normalization on GPU
        row_sums = cp.sum(vectors, axis=1, keepdims=True)
        row_sums = cp.where(row_sums == 0, 1, row_sums)  # Avoid division by zero
        vectors = vectors / row_sums
        
        return vectors
    
    def _cpu_dhatu_vectorization(self, texts: List[str]) -> np.ndarray:
        """CPU-based dhātu vectorization for comparison"""
        
        num_texts = len(texts)
        num_dhatus = len(self.dhatu_names)
        
        # Initialize output matrix
        vectors = np.zeros((num_texts, num_dhatus), dtype=np.float32)
        
        # Process each text-dhātu combination
        for text_idx, text in enumerate(texts):
            for dhatu_idx, dhatu in enumerate(self.dhatu_names):
                # Compute hash
                combined_input = f"{dhatu}::{text}".encode('utf-8')
                hash_obj = hashlib.sha256(combined_input)
                hash_bytes = hash_obj.digest()
                
                # Extract weight from hash bytes
                weight = (hash_bytes[0] + hash_bytes[5] + hash_bytes[13] + 
                         hash_bytes[21] + hash_bytes[29]) / 1024.0
                
                vectors[text_idx, dhatu_idx] = weight
        
        # L1 normalization
        row_sums = np.sum(vectors, axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1, row_sums)
        vectors = vectors / row_sums
        
        return vectors
    
    def benchmark_prime_base_computation(self, dhatu_vectors: np.ndarray, iterations=50) -> Dict[str, Any]:
        """Benchmark prime base computation performance"""
        
        print(f"\n⚡ BENCHMARKING PRIME BASE COMPUTATION ({self.device_type})")
        print("=" * 60)
        
        num_documents, num_dhatus = dhatu_vectors.shape
        num_bases = len(self.prime_numbers)
        
        if self.use_gpu:
            # Transfer data to GPU
            dhatu_vectors_gpu = cp.asarray(dhatu_vectors)
            
            start_time = time.time()
            
            for _ in range(iterations):
                prime_bases = self._gpu_prime_base_computation(dhatu_vectors_gpu)
                
            gpu_time = (time.time() - start_time) / iterations
            
            # Transfer result back to CPU
            if hasattr(prime_bases, 'get'):
                prime_bases_cpu = prime_bases.get()
            else:
                prime_bases_cpu = prime_bases
                
        else:
            start_time = time.time()
            
            for _ in range(iterations):
                prime_bases_cpu = self._cpu_prime_base_computation(dhatu_vectors)
                
            gpu_time = (time.time() - start_time) / iterations
        
        # Performance metrics
        documents_per_second = num_documents / gpu_time
        time_per_document_ms = (gpu_time / num_documents) * 1000
        
        benchmark_results = {
            'device_type': self.device_type,
            'num_documents': num_documents,
            'num_dhatus': num_dhatus,
            'num_prime_bases': num_bases,
            'iterations': iterations,
            'total_time_seconds': gpu_time,
            'documents_per_second': documents_per_second,
            'time_per_document_ms': time_per_document_ms,
            'output_shape': prime_bases_cpu.shape,
            'memory_usage_mb': prime_bases_cpu.nbytes / (1024 * 1024),
            'sample_prime_bases': prime_bases_cpu[0].tolist() if len(prime_bases_cpu) > 0 else []
        }
        
        return benchmark_results
    
    def _gpu_prime_base_computation(self, dhatu_vectors: cp.ndarray) -> cp.ndarray:
        """GPU-accelerated prime base computation"""
        
        num_documents, num_dhatus = dhatu_vectors.shape
        num_bases = len(self.prime_numbers)
        
        # Initialize output matrix on GPU
        prime_bases = cp.zeros((num_documents, num_bases), dtype=cp.float32)
        
        # Convert prime numbers to GPU array
        primes_gpu = cp.array(self.prime_numbers, dtype=cp.float32)
        
        # Compute prime base activations
        for base_idx, prime in enumerate(self.prime_numbers):
            # Create power matrix for this prime base
            powers = cp.arange(num_dhatus, dtype=cp.float32)
            prime_powers = cp.power(prime, powers % prime)
            
            # Compute weighted sum for each document
            weighted_activations = dhatu_vectors * prime_powers[cp.newaxis, :]
            base_activations = cp.sum(weighted_activations, axis=1)
            
            prime_bases[:, base_idx] = base_activations
        
        return prime_bases
    
    def _cpu_prime_base_computation(self, dhatu_vectors: np.ndarray) -> np.ndarray:
        """CPU-based prime base computation for comparison"""
        
        num_documents, num_dhatus = dhatu_vectors.shape
        num_bases = len(self.prime_numbers)
        
        # Initialize output matrix
        prime_bases = np.zeros((num_documents, num_bases), dtype=np.float32)
        
        # Compute prime base activations
        for base_idx, prime in enumerate(self.prime_numbers):
            # Create power matrix for this prime base
            powers = np.arange(num_dhatus, dtype=np.float32)
            prime_powers = np.power(prime, powers % prime)
            
            # Compute weighted sum for each document
            weighted_activations = dhatu_vectors * prime_powers[np.newaxis, :]
            base_activations = np.sum(weighted_activations, axis=1)
            
            prime_bases[:, base_idx] = base_activations
        
        return prime_bases
    
    def benchmark_semantic_ambiguity(self, prime_bases: np.ndarray, iterations=50) -> Dict[str, Any]:
        """Benchmark semantic ambiguity detection performance"""
        
        print(f"\n⚡ BENCHMARKING SEMANTIC AMBIGUITY DETECTION ({self.device_type})")
        print("=" * 65)
        
        num_documents, num_bases = prime_bases.shape
        
        if self.use_gpu:
            # Transfer data to GPU
            prime_bases_gpu = cp.asarray(prime_bases)
            
            start_time = time.time()
            
            for _ in range(iterations):
                ambiguity_scores = self._gpu_semantic_ambiguity(prime_bases_gpu)
                
            gpu_time = (time.time() - start_time) / iterations
            
            # Transfer result back to CPU
            if hasattr(ambiguity_scores, 'get'):
                ambiguity_scores_cpu = ambiguity_scores.get()
            else:
                ambiguity_scores_cpu = ambiguity_scores
                
        else:
            start_time = time.time()
            
            for _ in range(iterations):
                ambiguity_scores_cpu = self._cpu_semantic_ambiguity(prime_bases)
                
            gpu_time = (time.time() - start_time) / iterations
        
        # Performance metrics
        documents_per_second = num_documents / gpu_time
        time_per_document_ms = (gpu_time / num_documents) * 1000
        
        benchmark_results = {
            'device_type': self.device_type,
            'num_documents': num_documents,
            'num_bases': num_bases,
            'iterations': iterations,
            'total_time_seconds': gpu_time,
            'documents_per_second': documents_per_second,
            'time_per_document_ms': time_per_document_ms,
            'output_shape': ambiguity_scores_cpu.shape,
            'memory_usage_mb': ambiguity_scores_cpu.nbytes / (1024 * 1024),
            'sample_scores': ambiguity_scores_cpu[:5].tolist() if len(ambiguity_scores_cpu) > 0 else [],
            'mean_ambiguity': float(np.mean(ambiguity_scores_cpu)),
            'std_ambiguity': float(np.std(ambiguity_scores_cpu))
        }
        
        return benchmark_results
    
    def _gpu_semantic_ambiguity(self, prime_bases: cp.ndarray) -> cp.ndarray:
        """GPU-accelerated semantic ambiguity detection"""
        
        num_documents, num_bases = prime_bases.shape
        
        # Compute variance across prime bases for each document
        mean_activations = cp.mean(prime_bases, axis=1, keepdims=True)
        variance_activations = cp.mean((prime_bases - mean_activations) ** 2, axis=1)
        
        # Compute entropy-like measure
        # Normalize activations to probabilities
        normalized_bases = prime_bases / (cp.sum(prime_bases, axis=1, keepdims=True) + 1e-8)
        
        # Compute entropy
        entropy = -cp.sum(normalized_bases * cp.log(normalized_bases + 1e-8), axis=1)
        
        # Combine variance and entropy for ambiguity score
        ambiguity_scores = 0.7 * entropy + 0.3 * variance_activations
        
        return ambiguity_scores
    
    def _cpu_semantic_ambiguity(self, prime_bases: np.ndarray) -> np.ndarray:
        """CPU-based semantic ambiguity detection for comparison"""
        
        num_documents, num_bases = prime_bases.shape
        
        # Compute variance across prime bases for each document
        mean_activations = np.mean(prime_bases, axis=1, keepdims=True)
        variance_activations = np.mean((prime_bases - mean_activations) ** 2, axis=1)
        
        # Compute entropy-like measure
        # Normalize activations to probabilities
        normalized_bases = prime_bases / (np.sum(prime_bases, axis=1, keepdims=True) + 1e-8)
        
        # Compute entropy
        entropy = -np.sum(normalized_bases * np.log(normalized_bases + 1e-8), axis=1)
        
        # Combine variance and entropy for ambiguity score
        ambiguity_scores = 0.7 * entropy + 0.3 * variance_activations
        
        return ambiguity_scores
    
    def full_pipeline_benchmark(self, texts: List[str]) -> Dict[str, Any]:
        """Benchmark complete dhātu processing pipeline"""
        
        print(f"\n🏁 FULL PIPELINE BENCHMARK ({self.device_type})")
        print("=" * 50)
        
        start_time = time.time()
        
        # Step 1: Dhātu vectorization
        step1_start = time.time()
        dhatu_results = self.benchmark_dhatu_vectorization(texts, iterations=10)
        step1_time = time.time() - step1_start
        
        # Get vectors for next steps
        if self.use_gpu:
            dhatu_vectors = self._gpu_dhatu_vectorization(texts)
            if hasattr(dhatu_vectors, 'get'):
                dhatu_vectors_cpu = dhatu_vectors.get()
            else:
                dhatu_vectors_cpu = dhatu_vectors
        else:
            dhatu_vectors_cpu = self._cpu_dhatu_vectorization(texts)
        
        # Step 2: Prime base computation
        step2_start = time.time()
        prime_results = self.benchmark_prime_base_computation(dhatu_vectors_cpu, iterations=10)
        step2_time = time.time() - step2_start
        
        # Get prime bases for next step
        if self.use_gpu:
            dhatu_vectors_gpu = cp.asarray(dhatu_vectors_cpu)
            prime_bases = self._gpu_prime_base_computation(dhatu_vectors_gpu)
            if hasattr(prime_bases, 'get'):
                prime_bases_cpu = prime_bases.get()
            else:
                prime_bases_cpu = prime_bases
        else:
            prime_bases_cpu = self._cpu_prime_base_computation(dhatu_vectors_cpu)
        
        # Step 3: Semantic ambiguity detection
        step3_start = time.time()
        ambiguity_results = self.benchmark_semantic_ambiguity(prime_bases_cpu, iterations=10)
        step3_time = time.time() - step3_start
        
        total_time = time.time() - start_time
        
        # Comprehensive pipeline results
        pipeline_results = {
            'device_type': self.device_type,
            'total_texts': len(texts),
            'total_pipeline_time_seconds': total_time,
            'texts_per_second_pipeline': len(texts) / total_time,
            'step_breakdown': {
                'dhatu_vectorization': {
                    'time_seconds': step1_time,
                    'percentage': (step1_time / total_time) * 100,
                    'results': dhatu_results
                },
                'prime_base_computation': {
                    'time_seconds': step2_time,
                    'percentage': (step2_time / total_time) * 100,
                    'results': prime_results
                },
                'ambiguity_detection': {
                    'time_seconds': step3_time,
                    'percentage': (step3_time / total_time) * 100,
                    'results': ambiguity_results
                }
            }
        }
        
        return pipeline_results


def create_test_corpus(size=100) -> List[str]:
    """Create test corpus for benchmarking"""
    
    base_texts = [
        "The quantum computational framework demonstrates significant algorithmic efficiency.",
        "Machine learning models require extensive parameter optimization techniques.",
        "Statistical analysis reveals correlation patterns in experimental data.",
        "Neural network architectures exhibit emergent computational properties.",
        "Mathematical formulations provide theoretical foundations for research.",
        "Scientific methodology ensures reproducible experimental results.",
        "Advanced algorithms solve complex optimization problems efficiently.",
        "Data structures implement efficient storage and retrieval mechanisms.",
        "Parallel processing enhances computational performance significantly.",
        "Research findings contribute to scientific knowledge advancement."
    ]
    
    # Replicate to desired size
    test_corpus = []
    for i in range(size):
        text = base_texts[i % len(base_texts)]
        # Add variation
        variation = f" Article {i+1}: {text}"
        test_corpus.append(variation)
    
    return test_corpus


def main():
    """Main GPU kernel benchmarking"""
    
    print("🚀 DHĀTU GPU KERNELS BENCHMARK SUITE")
    print("=" * 45)
    print("Testing GPU acceleration for dhātu processing components")
    print()
    
    # Create test data
    test_sizes = [10, 50, 100, 500] if GPU_AVAILABLE else [10, 50, 100]
    
    all_results = {}
    
    for size in test_sizes:
        print(f"\n📊 TESTING CORPUS SIZE: {size} articles")
        print("=" * 40)
        
        # Create test corpus
        test_texts = create_test_corpus(size)
        
        # Test GPU version if available
        if GPU_AVAILABLE:
            print("\n🔥 GPU ACCELERATION TESTS")
            gpu_kernels = DhatuGPUKernels(use_gpu=True)
            gpu_results = gpu_kernels.full_pipeline_benchmark(test_texts)
            all_results[f'gpu_size_{size}'] = gpu_results
        
        # Test CPU version for comparison
        print("\n💻 CPU BASELINE TESTS")
        cpu_kernels = DhatuGPUKernels(use_gpu=False)
        cpu_results = cpu_kernels.full_pipeline_benchmark(test_texts)
        all_results[f'cpu_size_{size}'] = cpu_results
        
        # Compare performance if GPU available
        if GPU_AVAILABLE:
            speedup = cpu_results['texts_per_second_pipeline'] / gpu_results['texts_per_second_pipeline']
            print(f"\n⚡ SPEEDUP ANALYSIS:")
            print(f"   CPU: {cpu_results['texts_per_second_pipeline']:.2f} texts/sec")
            print(f"   GPU: {gpu_results['texts_per_second_pipeline']:.2f} texts/sec")
            print(f"   Speedup: {speedup:.2f}x")
    
    # Save comprehensive results
    output_file = Path('./gpu_kernels_benchmark_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Summary
    print(f"\n📋 BENCHMARK SUMMARY:")
    if GPU_AVAILABLE:
        print(f"   GPU device: Available")
    else:
        print(f"   GPU device: Not available (using CPU)")
    
    print(f"   Test corpus sizes: {test_sizes}")
    print(f"   Components tested: Dhātu vectorization, Prime bases, Ambiguity detection")
    
    return all_results


if __name__ == "__main__":
    main()