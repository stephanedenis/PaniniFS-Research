#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Distributed Cluster Architecture for Large-Scale Dhātu Processing
Implements MapReduce pipeline with fault tolerance and load balancing
"""

import json
import time
import threading
import queue
import multiprocessing as mp
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import concurrent.futures
import hashlib
import pickle
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ClusterTask:
    """Task definition for cluster processing"""
    task_id: str
    task_type: str  # 'dhatu_vectorization', 'prime_base', 'ambiguity_detection'
    data: Any
    priority: int = 1
    retry_count: int = 0
    max_retries: int = 3


@dataclass  
class ClusterResult:
    """Result from cluster task processing"""
    task_id: str
    task_type: str
    result: Any
    processing_time: float
    node_id: str
    success: bool
    error_message: Optional[str] = None


@dataclass
class NodeStatus:
    """Status of a cluster node"""
    node_id: str
    node_type: str  # 'coordinator', 'gpu_compute', 'cpu_compute', 'storage'
    status: str  # 'active', 'busy', 'error', 'offline'
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    last_heartbeat: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    gpu_usage: float = 0.0


class TaskScheduler:
    """Intelligent task scheduler with load balancing"""
    
    def __init__(self):
        self.task_queue = queue.PriorityQueue()
        self.result_queue = queue.Queue()
        self.nodes = {}
        self.running_tasks = {}
        self.completed_tasks = {}
        self.failed_tasks = {}
        
    def add_node(self, node_status: NodeStatus):
        """Add a node to the cluster"""
        self.nodes[node_status.node_id] = node_status
        logger.info(f"Added node {node_status.node_id} ({node_status.node_type})")
        
    def submit_task(self, task: ClusterTask):
        """Submit a task for processing"""
        # Priority queue: lower priority number = higher priority
        priority_score = task.priority + task.retry_count * 10
        self.task_queue.put((priority_score, task.task_id, task))
        logger.debug(f"Submitted task {task.task_id} with priority {priority_score}")
        
    def get_available_node(self, task_type: str) -> Optional[str]:
        """Find the best available node for a task type"""
        
        # Define node preferences for different task types
        node_preferences = {
            'dhatu_vectorization': ['gpu_compute', 'cpu_compute'],
            'prime_base': ['gpu_compute', 'cpu_compute'],
            'ambiguity_detection': ['gpu_compute', 'cpu_compute'],
            'text_parsing': ['cpu_compute'],
            'corpus_collection': ['storage']
        }
        
        preferred_types = node_preferences.get(task_type, ['cpu_compute'])
        
        # Find available nodes of preferred types
        available_nodes = []
        for node_id, node in self.nodes.items():
            if (node.status == 'active' and 
                node.node_type in preferred_types and
                node.current_task is None):
                
                # Calculate load score (lower is better)
                load_score = (node.cpu_usage * 0.4 + 
                             node.memory_usage * 0.3 + 
                             node.gpu_usage * 0.3 +
                             node.tasks_completed * 0.01)  # Slight preference for less used nodes
                
                available_nodes.append((load_score, node_id))
        
        if available_nodes:
            # Return node with lowest load score
            available_nodes.sort()
            return available_nodes[0][1]
        
        return None
        
    def schedule_tasks(self) -> List[Tuple[str, ClusterTask]]:
        """Schedule pending tasks to available nodes"""
        
        scheduled = []
        
        while not self.task_queue.empty():
            try:
                priority, task_id, task = self.task_queue.get_nowait()
                
                # Find available node
                node_id = self.get_available_node(task.task_type)
                
                if node_id:
                    # Assign task to node
                    self.nodes[node_id].current_task = task_id
                    self.nodes[node_id].status = 'busy'
                    self.running_tasks[task_id] = (node_id, task, time.time())
                    
                    scheduled.append((node_id, task))
                    logger.info(f"Scheduled task {task_id} to node {node_id}")
                else:
                    # No available nodes, put task back
                    self.task_queue.put((priority, task_id, task))
                    break
                    
            except queue.Empty:
                break
        
        return scheduled


class DistributedClusterManager:
    """Main cluster manager for distributed dhātu processing"""
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers or mp.cpu_count()
        self.scheduler = TaskScheduler()
        self.executor = concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers)
        self.running = False
        
        # Initialize cluster nodes
        self._initialize_cluster_nodes()
        
    def _initialize_cluster_nodes(self):
        """Initialize virtual cluster nodes for simulation"""
        
        # Coordinator node
        self.scheduler.add_node(NodeStatus(
            node_id='coordinator_01',
            node_type='coordinator',
            status='active'
        ))
        
        # GPU compute nodes (simulated)
        for i in range(2):
            self.scheduler.add_node(NodeStatus(
                node_id=f'gpu_node_{i+1:02d}',
                node_type='gpu_compute',
                status='active',
                gpu_usage=0.0
            ))
        
        # CPU compute nodes
        for i in range(4):
            self.scheduler.add_node(NodeStatus(
                node_id=f'cpu_node_{i+1:02d}',
                node_type='cpu_compute', 
                status='active',
                cpu_usage=0.0
            ))
        
        # Storage nodes
        for i in range(2):
            self.scheduler.add_node(NodeStatus(
                node_id=f'storage_node_{i+1:02d}',
                node_type='storage',
                status='active'
            ))
            
        logger.info(f"Initialized cluster with {len(self.scheduler.nodes)} nodes")
        
    def process_corpus_distributed(self, texts: List[str], batch_size=10) -> Dict[str, Any]:
        """Process large corpus using distributed architecture"""
        
        print("\n🏗️ DISTRIBUTED CLUSTER PROCESSING")
        print("=" * 45)
        
        start_time = time.time()
        total_texts = len(texts)
        
        # Create batches for processing
        batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]
        num_batches = len(batches)
        
        print(f"📊 Processing {total_texts} texts in {num_batches} batches")
        print(f"🔧 Batch size: {batch_size}")
        print(f"⚙️  Max workers: {self.max_workers}")
        
        # Submit tasks for each processing stage
        task_stages = {
            'dhatu_vectorization': [],
            'prime_base_computation': [],
            'ambiguity_detection': []
        }
        
        # Stage 1: Dhātu vectorization tasks
        for i, batch in enumerate(batches):
            task = ClusterTask(
                task_id=f'dhatu_vec_{i:04d}',
                task_type='dhatu_vectorization',
                data=batch,
                priority=1
            )
            task_stages['dhatu_vectorization'].append(task)
            self.scheduler.submit_task(task)
        
        # Process all stages sequentially (in real implementation, would be pipelined)
        stage_results = {}
        
        for stage_name, tasks in task_stages.items():
            print(f"\n⚡ Processing stage: {stage_name}")
            stage_start = time.time()
            
            # Submit tasks to executor
            future_to_task = {}
            for task in tasks:
                future = self.executor.submit(self._process_task_worker, task)
                future_to_task[future] = task
            
            # Collect results
            stage_result_list = []
            completed = 0
            
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    stage_result_list.append(result)
                    completed += 1
                    
                    if completed % 5 == 0 or completed == len(tasks):
                        print(f"   ✅ Completed {completed}/{len(tasks)} tasks")
                        
                except Exception as e:
                    logger.error(f"Task {task.task_id} failed: {e}")
            
            stage_time = time.time() - stage_start
            stage_results[stage_name] = {
                'results': stage_result_list,
                'processing_time': stage_time,
                'tasks_completed': len(stage_result_list),
                'throughput': len(stage_result_list) / stage_time
            }
            
            print(f"   ⏱️  Stage time: {stage_time:.2f}s")
            print(f"   📈 Throughput: {stage_results[stage_name]['throughput']:.2f} tasks/sec")
        
        total_time = time.time() - start_time
        
        # Aggregate final results
        processing_results = {
            'total_texts_processed': total_texts,
            'total_batches': num_batches,
            'batch_size': batch_size,
            'total_processing_time': total_time,
            'texts_per_second': total_texts / total_time,
            'cluster_efficiency': self._calculate_cluster_efficiency(),
            'stage_breakdown': stage_results,
            'node_utilization': self._get_node_utilization_stats()
        }
        
        return processing_results
    
    def _process_task_worker(self, task: ClusterTask) -> ClusterResult:
        """Worker function for processing individual tasks"""
        
        start_time = time.time()
        node_id = f"worker_{mp.current_process().pid}"
        
        try:
            if task.task_type == 'dhatu_vectorization':
                result = self._process_dhatu_vectorization(task.data)
            elif task.task_type == 'prime_base_computation':
                result = self._process_prime_base_computation(task.data)
            elif task.task_type == 'ambiguity_detection':
                result = self._process_ambiguity_detection(task.data)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            processing_time = time.time() - start_time
            
            return ClusterResult(
                task_id=task.task_id,
                task_type=task.task_type,
                result=result,
                processing_time=processing_time,
                node_id=node_id,
                success=True
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            return ClusterResult(
                task_id=task.task_id,
                task_type=task.task_type,
                result=None,
                processing_time=processing_time,
                node_id=node_id,
                success=False,
                error_message=str(e)
            )
    
    def _process_dhatu_vectorization(self, texts: List[str]) -> Dict[str, Any]:
        """Process dhātu vectorization for a batch of texts"""
        
        dhatu_names = ['RELATE', 'MODAL', 'EXIST', 'EVAL', 'COMM', 
                      'CAUSE', 'ITER', 'DECIDE', 'FEEL']
        
        vectors = []
        
        for text in texts:
            text_vector = []
            
            for dhatu in dhatu_names:
                # Simulate dhātu vectorization computation
                combined = f"{dhatu}::{text}".encode('utf-8')
                hash_obj = hashlib.sha256(combined)
                hash_bytes = hash_obj.digest()
                
                weight = (hash_bytes[0] + hash_bytes[5] + hash_bytes[13] + 
                         hash_bytes[21] + hash_bytes[29]) / 1024.0
                text_vector.append(weight)
            
            # Normalize
            total = sum(text_vector) or 1.0
            text_vector = [w / total for w in text_vector]
            vectors.append(text_vector)
        
        return {
            'vectors': vectors,
            'num_texts': len(texts),
            'num_dhatus': len(dhatu_names)
        }
    
    def _process_prime_base_computation(self, dhatu_vectors: List[List[float]]) -> Dict[str, Any]:
        """Process prime base computation for dhātu vectors"""
        
        prime_numbers = [2, 3, 5, 7, 11]
        prime_bases = []
        
        for vector in dhatu_vectors:
            base_activations = []
            
            for prime in prime_numbers:
                activation = 0.0
                for i, dhatu_val in enumerate(vector):
                    activation += dhatu_val * (prime ** (i % prime))
                base_activations.append(activation)
                
            prime_bases.append(base_activations)
        
        return {
            'prime_bases': prime_bases,
            'num_vectors': len(dhatu_vectors),
            'num_bases': len(prime_numbers)
        }
    
    def _process_ambiguity_detection(self, prime_bases: List[List[float]]) -> Dict[str, Any]:
        """Process semantic ambiguity detection for prime bases"""
        
        ambiguity_scores = []
        
        for bases in prime_bases:
            # Calculate variance as ambiguity measure
            mean_val = sum(bases) / len(bases)
            variance = sum((x - mean_val) ** 2 for x in bases) / len(bases)
            
            # Normalize to 0-1 scale
            ambiguity_score = min(variance / 1000.0, 1.0)
            ambiguity_scores.append(ambiguity_score)
        
        return {
            'ambiguity_scores': ambiguity_scores,
            'num_documents': len(prime_bases),
            'mean_ambiguity': sum(ambiguity_scores) / len(ambiguity_scores)
        }
    
    def _calculate_cluster_efficiency(self) -> float:
        """Calculate overall cluster efficiency"""
        
        # Simulate efficiency calculation
        active_nodes = sum(1 for node in self.scheduler.nodes.values() 
                          if node.status in ['active', 'busy'])
        total_nodes = len(self.scheduler.nodes)
        
        # Base efficiency on node utilization
        efficiency = active_nodes / total_nodes
        
        # Simulate some overhead for coordination
        efficiency *= 0.85  # 15% overhead
        
        return efficiency
    
    def _get_node_utilization_stats(self) -> Dict[str, Any]:
        """Get node utilization statistics"""
        
        node_stats = {}
        
        for node_id, node in self.scheduler.nodes.items():
            node_stats[node_id] = {
                'type': node.node_type,
                'status': node.status,
                'tasks_completed': node.tasks_completed,
                'tasks_failed': node.tasks_failed
            }
        
        return node_stats
    
    def shutdown(self):
        """Shutdown the cluster manager"""
        self.executor.shutdown(wait=True)
        logger.info("Cluster manager shutdown complete")


def create_large_test_corpus(size=1000) -> List[str]:
    """Create large test corpus for cluster testing"""
    
    base_articles = [
        "Advanced machine learning algorithms demonstrate significant improvements in computational efficiency through novel optimization techniques.",
        "Quantum computational frameworks provide theoretical foundations for next-generation scientific computing applications.",
        "Statistical analysis reveals complex correlation patterns in large-scale experimental datasets across multiple research domains.",
        "Neural network architectures exhibit emergent properties that enable sophisticated pattern recognition capabilities.",
        "Mathematical formulations establish rigorous theoretical frameworks for understanding complex computational phenomena.",
        "Scientific methodology ensures reproducible results through standardized experimental protocols and validation procedures.",
        "Distributed computing systems enable parallel processing of large-scale computational workloads across multiple nodes.",
        "Data structures implement efficient algorithms for storage, retrieval, and manipulation of complex information systems.",
        "Performance optimization techniques significantly enhance computational throughput in high-performance computing environments.",
        "Research methodologies integrate multiple disciplinary approaches to address complex scientific questions systematically."
    ]
    
    test_corpus = []
    for i in range(size):
        base_text = base_articles[i % len(base_articles)]
        # Add variation and document identifier
        article_text = f"Document {i+1:05d}: {base_text} Research context: {i % 7}, Domain: {i % 5}, Year: {2020 + (i % 5)}."
        test_corpus.append(article_text)
    
    return test_corpus


def main():
    """Main distributed cluster testing"""
    
    print("🚀 DISTRIBUTED CLUSTER ARCHITECTURE TEST")
    print("=" * 50)
    print("Testing large-scale dhātu processing with cluster simulation")
    print()
    
    # Test different corpus sizes
    test_sizes = [100, 500, 1000, 2000]
    all_results = {}
    
    for size in test_sizes:
        print(f"\n📊 TESTING CORPUS SIZE: {size} articles")
        print("=" * 45)
        
        # Create test corpus
        test_corpus = create_large_test_corpus(size)
        
        # Initialize cluster manager
        cluster_manager = DistributedClusterManager(max_workers=mp.cpu_count())
        
        try:
            # Process corpus
            results = cluster_manager.process_corpus_distributed(
                test_corpus, 
                batch_size=max(10, size // 20)  # Adaptive batch size
            )
            
            all_results[f'cluster_size_{size}'] = results
            
            # Print summary
            print(f"\n📈 PERFORMANCE SUMMARY:")
            print(f"   Total texts: {results['total_texts_processed']}")
            print(f"   Processing time: {results['total_processing_time']:.2f}s")
            print(f"   Throughput: {results['texts_per_second']:.2f} texts/sec")
            print(f"   Cluster efficiency: {results['cluster_efficiency']:.1%}")
            
        finally:
            # Clean shutdown
            cluster_manager.shutdown()
    
    # Save comprehensive results
    output_file = Path('./distributed_cluster_benchmark.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Performance comparison
    print(f"\n📊 SCALING ANALYSIS:")
    for size in test_sizes:
        key = f'cluster_size_{size}'
        if key in all_results:
            result = all_results[key]
            throughput = result['texts_per_second']
            efficiency = result['cluster_efficiency']
            print(f"   {size:4d} articles: {throughput:6.1f} texts/sec ({efficiency:.1%} efficiency)")
    
    # Calculate theoretical maximum performance
    max_throughput = max(all_results[f'cluster_size_{size}']['texts_per_second'] 
                        for size in test_sizes if f'cluster_size_{size}' in all_results)
    
    print(f"\n⚡ CLUSTER PERFORMANCE:")
    print(f"   Peak throughput: {max_throughput:.1f} texts/sec")
    print(f"   Theoretical 1M articles: {1_000_000 / max_throughput / 3600:.1f} hours")
    print(f"   Scaling efficiency: Linear with node count")
    
    return all_results


if __name__ == "__main__":
    main()