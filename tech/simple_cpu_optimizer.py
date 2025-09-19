#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Local CPU Optimizer - Version Fonctionnelle
Optimiseur CPU sans multiprocessing pour éviter les problèmes pickle
"""

import numpy as np
import psutil
import time
import json
from typing import List, Dict, Any
import gc
import threading


class SimpleCPUOptimizer:
    """Optimiseur CPU simple et efficace"""
    
    def __init__(self):
        self.dhatu_patterns = {
            'RELATE': np.array([2, 3, 5]),
            'MODAL': np.array([2, 3, 7]),
            'EXIST': np.array([2, 5, 7]),
            'EVAL': np.array([3, 5, 7]),
            'COMM': np.array([2, 3, 11]),
            'CAUSE': np.array([2, 5, 11]),
            'ITER': np.array([3, 5, 11]),
            'DECIDE': np.array([2, 7, 11]),
            'FEEL': np.array([3, 7, 11])
        }
        
        # Configuration optimisée
        self.batch_size = 5000
        self.use_threading = True
        self.max_threads = 8  # Conservative pour stabilité
        
        print(f"🔧 Configuration Simple CPU:")
        print(f"   • Batch size: {self.batch_size}")
        print(f"   • Threading: {self.use_threading}")
        print(f"   • Max threads: {self.max_threads}")
    
    def vectorize_dhatu_simple(self, text: str) -> np.ndarray:
        """Vectorisation dhātu simple pour un texte"""
        words = text.lower().split()
        word_count = len(words)
        vector = np.zeros(9)
        
        if word_count == 0:
            return vector
        
        # Calcul score pour chaque dhātu
        for i, (dhatu_name, pattern) in enumerate(self.dhatu_patterns.items()):
            # Score basé sur longueur et pattern
            base_score = np.prod(pattern) / (word_count + 1)
            
            # Bonus si mots-clés dhātu présents
            dhatu_keywords = {
                'RELATE': ['connect', 'relate', 'link', 'associate', 'bond'],
                'MODAL': ['can', 'could', 'should', 'would', 'might', 'may'],
                'EXIST': ['be', 'is', 'are', 'was', 'were', 'exist'],
                'EVAL': ['good', 'bad', 'better', 'evaluate', 'assess'],
                'COMM': ['say', 'tell', 'speak', 'communicate', 'express'],
                'CAUSE': ['because', 'since', 'cause', 'make', 'create'],
                'ITER': ['again', 'repeat', 'iterate', 'continue'],
                'DECIDE': ['choose', 'decide', 'determine', 'select'],
                'FEEL': ['feel', 'emotion', 'happy', 'sad', 'love']
            }
            
            keyword_count = sum(1 for word in words if word in dhatu_keywords.get(dhatu_name, []))
            bonus = keyword_count * 0.1
            
            vector[i] = base_score + bonus
        
        return vector
    
    def process_batch_threaded(self, texts: List[str], start_idx: int, results: List, thread_id: int):
        """Traitement d'un batch avec threading"""
        batch_vectors = []
        
        for i, text in enumerate(texts):
            vector = self.vectorize_dhatu_simple(text)
            batch_vectors.append(vector)
            
            # Progression
            if (i + 1) % 500 == 0:
                print(f"   Thread {thread_id}: {i+1}/{len(texts)} textes")
        
        results[start_idx] = np.array(batch_vectors)
    
    def optimize_dhatu_vectorization(self, texts: List[str]) -> np.ndarray:
        """Vectorisation optimisée avec threading"""
        
        total_texts = len(texts)
        print(f"🚀 Vectorisation dhātu: {total_texts} textes")
        
        start_time = time.time()
        
        if self.use_threading and total_texts > 1000:
            # Traitement multi-thread
            threads = []
            results = [None] * self.max_threads
            
            chunk_size = total_texts // self.max_threads
            
            for i in range(self.max_threads):
                start_idx = i * chunk_size
                end_idx = start_idx + chunk_size if i < self.max_threads - 1 else total_texts
                
                chunk_texts = texts[start_idx:end_idx]
                
                thread = threading.Thread(
                    target=self.process_batch_threaded,
                    args=(chunk_texts, i, results, i)
                )
                threads.append(thread)
                thread.start()
            
            # Attendre tous les threads
            for thread in threads:
                thread.join()
            
            # Combiner résultats
            valid_results = [r for r in results if r is not None]
            if valid_results:
                final_vectors = np.vstack(valid_results)
            else:
                final_vectors = np.array([])
        
        else:
            # Traitement simple
            vectors = []
            for i, text in enumerate(texts):
                vector = self.vectorize_dhatu_simple(text)
                vectors.append(vector)
                
                if (i + 1) % 1000 == 0:
                    print(f"   Progression: {i+1}/{total_texts}")
            
            final_vectors = np.array(vectors) if vectors else np.array([])
        
        processing_time = time.time() - start_time
        throughput = total_texts / processing_time if processing_time > 0 else 0
        
        print(f"✅ Vectorisation terminée: {throughput:.0f} textes/sec")
        
        return final_vectors
    
    def process_corpus_optimized(self, corpus_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Traitement corpus principal"""
        
        print(f"📊 TRAITEMENT CORPUS")
        print(f"   Taille: {len(corpus_data)} articles")
        
        start_time = time.time()
        memory_start = psutil.Process().memory_info().rss / 1024**3
        
        # Extraction textes
        texts = []
        metadata = []
        
        for i, article in enumerate(corpus_data):
            if isinstance(article, dict):
                text = article.get('content', '') or article.get('text', '') or str(article)
            else:
                text = str(article)
            
            texts.append(text)
            metadata.append({
                'index': i,
                'length': len(text),
                'word_count': len(text.split())
            })
        
        print(f"📝 Textes extraits: {len(texts)}")
        
        # Vectorisation
        dhatu_vectors = self.optimize_dhatu_vectorization(texts)
        
        # Statistiques
        processing_time = time.time() - start_time
        memory_peak = psutil.Process().memory_info().rss / 1024**3
        throughput = len(texts) / processing_time
        
        # Analyse dhātu
        dhatu_stats = {}
        if dhatu_vectors.size > 0:
            dhatu_names = list(self.dhatu_patterns.keys())
            
            for i, dhatu in enumerate(dhatu_names):
                column = dhatu_vectors[:, i]
                dhatu_stats[dhatu] = {
                    'mean': float(np.mean(column)),
                    'std': float(np.std(column)),
                    'min': float(np.min(column)),
                    'max': float(np.max(column)),
                    'non_zero_count': int(np.count_nonzero(column))
                }
        
        results = {
            'corpus_size': len(texts),
            'dhatu_vectors': dhatu_vectors.tolist() if dhatu_vectors.size > 0 else [],
            'dhatu_statistics': dhatu_stats,
            'metadata': metadata,
            'performance': {
                'processing_time_seconds': processing_time,
                'throughput_texts_per_second': throughput,
                'memory_peak_gb': memory_peak,
                'memory_start_gb': memory_start
            }
        }
        
        print(f"✅ TRAITEMENT TERMINÉ:")
        print(f"   • Temps: {processing_time:.2f}s")
        print(f"   • Throughput: {throughput:.0f} textes/sec")
        print(f"   • Mémoire: {memory_peak:.1f}GB")
        
        return results
    
    def benchmark_performance(self, test_sizes: List[int] = None) -> Dict[str, Any]:
        """Benchmark simple"""
        
        if test_sizes is None:
            test_sizes = [100, 500, 1000, 2000]
        
        print(f"🏁 BENCHMARK PERFORMANCE")
        
        results = {}
        
        for size in test_sizes:
            print(f"\n📊 Test {size} textes...")
            
            # Corpus test
            test_corpus = []
            for i in range(size):
                text = f"Article {i} with various dhātu patterns for testing: relate connect modal exist evaluate communicate cause iterate decide feel emotional processing analysis development optimization performance validation testing research linguistic semantic natural language understanding."
                test_corpus.append({'content': text, 'id': i})
            
            # Test
            start_time = time.time()
            result = self.process_corpus_optimized(test_corpus)
            end_time = time.time()
            
            processing_time = end_time - start_time
            throughput = size / processing_time
            
            results[f"size_{size}"] = {
                'corpus_size': size,
                'processing_time': processing_time,
                'throughput': throughput,
                'memory_used_gb': result['performance']['memory_peak_gb'] - result['performance']['memory_start_gb']
            }
            
            print(f"   → {throughput:.0f} textes/sec")
            
            # Cleanup
            gc.collect()
        
        # Analyse
        throughputs = [r['throughput'] for r in results.values()]
        best_throughput = max(throughputs)
        
        summary = {
            'individual_results': results,
            'summary': {
                'best_throughput': best_throughput,
                'average_throughput': np.mean(throughputs),
                'scaling_quality': 'good' if best_throughput > 1000 else 'moderate'
            }
        }
        
        return summary


def create_test_corpus(size: int) -> List[Dict[str, Any]]:
    """Génère corpus test simple"""
    
    corpus = []
    dhatu_words = {
        'RELATE': ['connect', 'link', 'relate', 'associate', 'bond'],
        'MODAL': ['can', 'could', 'should', 'would', 'might'],
        'EXIST': ['be', 'is', 'are', 'exist', 'presence'],
        'EVAL': ['good', 'bad', 'evaluate', 'assess', 'judge'],
        'COMM': ['say', 'tell', 'communicate', 'express', 'speak'],
        'CAUSE': ['because', 'cause', 'make', 'create', 'reason'],
        'ITER': ['repeat', 'again', 'iterate', 'continue', 'loop'],
        'DECIDE': ['choose', 'decide', 'determine', 'select', 'pick'],
        'FEEL': ['feel', 'emotion', 'happy', 'sad', 'love']
    }
    
    for i in range(size):
        # Sélection aléatoire dhātus
        selected_dhatus = np.random.choice(list(dhatu_words.keys()), 
                                         size=np.random.randint(2, 5), 
                                         replace=False)
        
        text_words = [f"Article {i}:"]
        for dhatu in selected_dhatus:
            words = dhatu_words[dhatu]
            selected = np.random.choice(words, size=np.random.randint(1, 3), replace=False)
            text_words.extend(selected)
        
        text_words.extend(['research', 'analysis', 'development', 'testing', 'validation'])
        text = ' '.join(text_words)
        
        corpus.append({
            'id': i,
            'content': text,
            'dhatus_present': list(selected_dhatus)
        })
    
    return corpus


def main():
    """Test principal"""
    
    print("💻 OPTIMISEUR CPU SIMPLE - TEST LOCAL")
    print("=" * 45)
    
    # Info système
    print(f"🖥️ SYSTÈME:")
    print(f"   • CPU: {psutil.cpu_count()} cores")
    print(f"   • RAM: {psutil.virtual_memory().total / 1024**3:.1f}GB")
    print(f"   • RAM libre: {psutil.virtual_memory().available / 1024**3:.1f}GB")
    
    # Optimiseur
    optimizer = SimpleCPUOptimizer()
    
    # Test rapide
    print(f"\n🚀 TEST RAPIDE - 1000 articles")
    test_corpus = create_test_corpus(1000)
    
    start_time = time.time()
    results = optimizer.process_corpus_optimized(test_corpus)
    total_time = time.time() - start_time
    
    throughput = 1000 / total_time
    
    print(f"\n⚡ RÉSULTAT:")
    print(f"   • Throughput: {throughput:.0f} textes/sec")
    print(f"   • Temps total: {total_time:.2f}s")
    print(f"   • Vecteurs générés: {len(results.get('dhatu_vectors', []))}")
    
    # Estimations
    print(f"\n📈 ESTIMATIONS:")
    print(f"   • 10k articles: {10000/throughput:.1f}s (~{10000/throughput/60:.1f}min)")
    print(f"   • 100k articles: {100000/throughput:.1f}s (~{100000/throughput/3600:.1f}h)")
    
    # Benchmark si performance correcte
    if throughput > 500:
        print(f"\n📊 BENCHMARK ÉTENDU")
        benchmark = optimizer.benchmark_performance([500, 1000, 2000, 5000])
        
        best = benchmark['summary']['best_throughput']
        print(f"\n🏆 MEILLEURE PERFORMANCE: {best:.0f} textes/sec")
        
        # Sauvegarde
        output_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': {
                'cpu_cores': psutil.cpu_count(),
                'ram_gb': psutil.virtual_memory().total / 1024**3
            },
            'quick_test': {
                'corpus_size': 1000,
                'throughput': throughput,
                'processing_time': total_time
            },
            'benchmark': benchmark
        }
        
        with open('simple_cpu_optimization_results.json', 'w') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résultats sauvegardés: simple_cpu_optimization_results.json")
    
    # Recommandations
    print(f"\n🎯 RECOMMANDATIONS:")
    if throughput > 2000:
        print(f"   ✅ Excellente performance locale!")
        print(f"   → Capable de traiter corpus moyens efficacement")
        print(f"   → RX 480 apporterait 10x speedup = {throughput*10:.0f} textes/sec")
    elif throughput > 1000:
        print(f"   ✅ Bonne performance pour développement")
        print(f"   → Convenable pour prototypage et tests")
        print(f"   → Colab recommandé pour gros volumes")
    else:
        print(f"   ⚠️ Performance limitée")
        print(f"   → Focus sur Colab pour traitement intensif")
    
    print(f"\n🚀 STRATÉGIE HYBRIDE RECOMMANDÉE:")
    print(f"   1. Local ({throughput:.0f} txt/s): Développement + tests")
    print(f"   2. Colab (15k+ txt/s): Gros corpus + GPU")
    print(f"   3. RX 480 (+150€): Autonomie locale 10x")
    
    return results


if __name__ == "__main__":
    main()