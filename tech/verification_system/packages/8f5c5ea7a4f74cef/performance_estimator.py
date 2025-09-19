#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance Estimation for Large-Scale Dhātu Analysis
Estimates processing times and computational requirements
"""

import time
import json
import psutil
import tracemalloc
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import statistics

@dataclass
class PerformanceMetrics:
    processing_time: float
    memory_peak: int  # bytes
    memory_current: int  # bytes
    cpu_percent: float
    papers_processed: int
    dhatu_operations: int
    
    @property
    def papers_per_second(self) -> float:
        return self.papers_processed / max(self.processing_time, 0.001)
    
    @property
    def time_per_paper(self) -> float:
        return self.processing_time / max(self.papers_processed, 1)
    
    @property
    def memory_per_paper(self) -> float:
        return self.memory_peak / max(self.papers_processed, 1)

class PerformanceEstimator:
    def __init__(self):
        self.baseline_metrics = None
        
    def measure_baseline_performance(self, corpus_file: Path) -> PerformanceMetrics:
        """Measure performance on current corpus"""
        
        print("📊 Measuring baseline performance...")
        
        # Start monitoring
        tracemalloc.start()
        process = psutil.Process()
        start_time = time.time()
        start_cpu_time = process.cpu_percent()
        
        # Load corpus
        with open(corpus_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        # Simulate processing all papers
        total_dhatu_ops = 0
        
        for paper in papers:
            text = paper['title'] + " " + paper['abstract']
            
            # Simulate dhātu analysis operations
            for dhatu in ['RELATE', 'MODAL', 'EXIST', 'EVAL', 'COMM', 
                         'CAUSE', 'ITER', 'DECIDE', 'FEEL']:
                
                # Simulate pattern matching (represents actual regex operations)
                _ = text.lower().count('the')  # Simple operation as proxy
                _ = len(text.split())  # Word counting
                total_dhatu_ops += 2
        
        # End monitoring
        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        end_cpu_time = process.cpu_percent()
        tracemalloc.stop()
        
        metrics = PerformanceMetrics(
            processing_time=end_time - start_time,
            memory_peak=peak_memory,
            memory_current=current_memory,
            cpu_percent=(start_cpu_time + end_cpu_time) / 2,
            papers_processed=len(papers),
            dhatu_operations=total_dhatu_ops
        )
        
        self.baseline_metrics = metrics
        return metrics
    
    def estimate_corpus_sizes(self) -> Dict[str, Dict[str, Any]]:
        """Estimate performance for different corpus sizes"""
        
        if not self.baseline_metrics:
            raise ValueError("Must measure baseline performance first")
        
        base = self.baseline_metrics
        
        # Corpus size scenarios
        scenarios = {
            'small_pilot': {
                'papers': 100,
                'description': 'Small pilot study'
            },
            'medium_research': {
                'papers': 1000, 
                'description': 'Medium research corpus'
            },
            'large_validation': {
                'papers': 10000,
                'description': 'Large validation corpus'
            },
            'industrial_scale': {
                'papers': 100000,
                'description': 'Industrial scale processing'
            },
            'full_arxiv': {
                'papers': 2000000,
                'description': 'Complete ArXiv corpus'
            }
        }
        
        estimates = {}
        
        for scenario_name, scenario in scenarios.items():
            target_papers = scenario['papers']
            scale_factor = target_papers / base.papers_processed
            
            # Linear scaling assumptions (conservative)
            estimated_time = base.processing_time * scale_factor
            estimated_memory = base.memory_peak * scale_factor
            
            # Add some overhead for larger datasets (sub-linear scaling in reality)
            if scale_factor > 10:
                efficiency_factor = 0.8  # 20% overhead for large datasets
                estimated_time *= (1 / efficiency_factor)
                estimated_memory *= 1.2  # 20% extra memory for indexing
            
            estimates[scenario_name] = {
                'target_papers': target_papers,
                'description': scenario['description'],
                'estimated_time_seconds': estimated_time,
                'estimated_time_hours': estimated_time / 3600,
                'estimated_time_days': estimated_time / (3600 * 24),
                'estimated_memory_mb': estimated_memory / (1024 * 1024),
                'estimated_memory_gb': estimated_memory / (1024 * 1024 * 1024),
                'papers_per_second': target_papers / estimated_time,
                'scale_factor': scale_factor
            }
        
        return estimates
    
    def estimate_hardware_requirements(self, estimates: Dict) -> Dict[str, Any]:
        """Estimate hardware requirements for different scenarios"""
        
        requirements = {}
        
        for scenario_name, estimate in estimates.items():
            memory_gb = estimate['estimated_memory_gb']
            time_hours = estimate['estimated_time_hours']
            
            # Hardware recommendations
            if memory_gb < 4:
                hw_tier = 'laptop'
                recommended_cores = 4
                recommended_ram = 8
            elif memory_gb < 16:
                hw_tier = 'workstation'
                recommended_cores = 8
                recommended_ram = 32
            elif memory_gb < 64:
                hw_tier = 'server'
                recommended_cores = 16
                recommended_ram = 128
            else:
                hw_tier = 'cluster'
                recommended_cores = 32
                recommended_ram = 256
            
            # Cost estimates (rough AWS pricing)
            if hw_tier == 'laptop':
                cost_per_hour = 0.0  # Local processing
            elif hw_tier == 'workstation':
                cost_per_hour = 0.5  # m5.2xlarge equivalent
            elif hw_tier == 'server':
                cost_per_hour = 2.0  # m5.8xlarge equivalent
            else:
                cost_per_hour = 8.0  # cluster of m5.16xlarge
            
            total_cost = cost_per_hour * time_hours
            
            requirements[scenario_name] = {
                'hardware_tier': hw_tier,
                'recommended_cores': recommended_cores,
                'recommended_ram_gb': recommended_ram,
                'estimated_cost_usd': total_cost,
                'parallelization_potential': min(recommended_cores, estimate['target_papers'] / 100)
            }
        
        return requirements
    
    def estimate_optimizations(self) -> Dict[str, Any]:
        """Estimate impact of various optimizations"""
        
        optimizations = {
            'parallel_processing': {
                'description': 'Multi-core parallel processing',
                'speedup_factor': 4.0,  # Conservative for 8-core system
                'memory_overhead': 1.2,
                'implementation_complexity': 'medium'
            },
            'compiled_patterns': {
                'description': 'Pre-compiled regex patterns',
                'speedup_factor': 2.0,
                'memory_overhead': 1.1,
                'implementation_complexity': 'low'
            },
            'streaming_processing': {
                'description': 'Stream processing for large files',
                'speedup_factor': 1.0,  # Same speed but constant memory
                'memory_overhead': 0.1,  # Constant memory usage
                'implementation_complexity': 'high'
            },
            'rust_implementation': {
                'description': 'Rust-based core processing',
                'speedup_factor': 5.0,
                'memory_overhead': 0.5,  # More memory efficient
                'implementation_complexity': 'high'
            },
            'gpu_acceleration': {
                'description': 'GPU-accelerated text processing',
                'speedup_factor': 10.0,
                'memory_overhead': 2.0,  # GPU memory requirements
                'implementation_complexity': 'very_high'
            }
        }
        
        # Calculate combined optimizations impact
        combined_speedup = 1.0
        combined_memory = 1.0
        
        # Conservative combination (not multiplicative)
        practical_optimizations = ['parallel_processing', 'compiled_patterns', 'rust_implementation']
        
        for opt_name in practical_optimizations:
            opt = optimizations[opt_name]
            combined_speedup *= opt['speedup_factor'] ** 0.7  # Diminishing returns
            combined_memory *= opt['memory_overhead'] ** 0.5  # Less memory impact combined
        
        optimizations['realistic_combined'] = {
            'description': 'Realistic combination of optimizations',
            'speedup_factor': combined_speedup,
            'memory_overhead': combined_memory,
            'implementation_complexity': 'high'
        }
        
        return optimizations
    
    def generate_performance_report(self, corpus_file: Path) -> Dict[str, Any]:
        """Generate complete performance analysis report"""
        
        print("🚀 Generating comprehensive performance report...")
        
        # Measure baseline
        baseline = self.measure_baseline_performance(corpus_file)
        
        # Generate estimates
        corpus_estimates = self.estimate_corpus_sizes()
        hardware_requirements = self.estimate_hardware_requirements(corpus_estimates)
        optimizations = self.estimate_optimizations()
        
        # Compile report
        report = {
            'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'baseline_performance': {
                'papers_processed': baseline.papers_processed,
                'processing_time_seconds': baseline.processing_time,
                'papers_per_second': baseline.papers_per_second,
                'time_per_paper_ms': baseline.time_per_paper * 1000,
                'memory_peak_mb': baseline.memory_peak / (1024 * 1024),
                'memory_per_paper_kb': baseline.memory_per_paper / 1024,
                'dhatu_operations': baseline.dhatu_operations,
                'cpu_utilization_percent': baseline.cpu_percent
            },
            'corpus_size_estimates': corpus_estimates,
            'hardware_requirements': hardware_requirements,
            'optimization_potential': optimizations,
            'recommendations': self._generate_recommendations(corpus_estimates, hardware_requirements, optimizations)
        }
        
        return report
    
    def _generate_recommendations(self, estimates: Dict, hardware: Dict, optimizations: Dict) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Performance recommendations
        if self.baseline_metrics.papers_per_second < 1.0:
            recommendations.append("⚡ Consider parallel processing - current speed is below 1 paper/second")
        
        if self.baseline_metrics.memory_per_paper > 10 * 1024 * 1024:  # 10MB per paper
            recommendations.append("💾 Memory usage is high - consider streaming processing")
        
        # Scale recommendations
        large_scenario = estimates.get('large_validation', {})
        if large_scenario.get('estimated_time_hours', 0) > 24:
            recommendations.append("🏗️ For large-scale processing, implement Rust core for 5x speedup")
        
        if large_scenario.get('estimated_memory_gb', 0) > 32:
            recommendations.append("🖥️ Large corpus will require server-class hardware (32+ GB RAM)")
        
        # Optimization recommendations
        recommendations.append("🔧 Priority optimizations: 1) Parallel processing 2) Compiled patterns 3) Rust core")
        recommendations.append("📊 Expected combined speedup: 8-15x with realistic optimizations")
        
        return recommendations


def main():
    """Main performance estimation"""
    
    print("⚡ Performance Estimation for Large-Scale Dhātu Analysis")
    print("=" * 65)
    
    # Check if corpus exists
    corpus_file = Path('./corpus_simple/corpus.json')
    if not corpus_file.exists():
        print("❌ Corpus file not found. Please run corpus collection first.")
        return
    
    # Run performance analysis
    estimator = PerformanceEstimator()
    report = estimator.generate_performance_report(corpus_file)
    
    # Save report
    output_file = Path('./corpus_simple/performance_report.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Report saved to: {output_file}")
    
    # Print summary
    baseline = report['baseline_performance']
    print(f"\n📊 Baseline Performance:")
    print(f"   Papers/second: {baseline['papers_per_second']:.2f}")
    print(f"   Time per paper: {baseline['time_per_paper_ms']:.1f}ms")
    print(f"   Memory per paper: {baseline['memory_per_paper_kb']:.1f}KB")
    
    print(f"\n🎯 Large-Scale Estimates:")
    large = report['corpus_size_estimates']['large_validation']
    print(f"   10K papers: {large['estimated_time_hours']:.1f} hours")
    print(f"   Memory needed: {large['estimated_memory_gb']:.1f}GB")
    
    industrial = report['corpus_size_estimates']['industrial_scale']
    print(f"   100K papers: {industrial['estimated_time_days']:.1f} days")
    print(f"   Memory needed: {industrial['estimated_memory_gb']:.1f}GB")
    
    print(f"\n💡 Key Recommendations:")
    for rec in report['recommendations'][:3]:
        print(f"   {rec}")


if __name__ == "__main__":
    main()