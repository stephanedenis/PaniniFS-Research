#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Hardware Analysis & Optimization Strategy
Analyse du matériel local + stratégie hybride gratuit/local pour dhātu processing
"""

import subprocess
import psutil
import platform
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time


@dataclass
class HardwareProfile:
    """Profile matériel local"""
    cpu_cores: int
    cpu_freq: float
    ram_total: float
    ram_available: float
    disk_space: float
    gpu_devices: List[Dict[str, Any]]
    os_info: str
    architecture: str


@dataclass
class GPUCapabilities:
    """Capacités GPU détaillées"""
    name: str
    memory_total: int
    memory_available: int
    cuda_support: bool
    opencl_support: bool
    compute_capability: Optional[str]
    power_efficiency: str
    recommended_tasks: List[str]


class LocalHardwareAnalyzer:
    """Analyseur de matériel local pour optimisation dhātu"""
    
    def __init__(self):
        self.profile = None
        self.gpu_analysis = {}
        
    def analyze_system(self) -> HardwareProfile:
        """Analyse complète du système local"""
        
        print("🔍 ANALYSE MATÉRIEL LOCAL")
        print("=" * 40)
        
        # CPU Analysis
        cpu_info = self._analyze_cpu()
        print(f"🖥️  CPU: {cpu_info['brand']} - {cpu_info['cores']} cores @ {cpu_info['freq']:.2f}GHz")
        
        # Memory Analysis
        memory_info = self._analyze_memory()
        print(f"💾 RAM: {memory_info['total']:.1f}GB total, {memory_info['available']:.1f}GB disponible")
        
        # Storage Analysis
        storage_info = self._analyze_storage()
        print(f"💿 Stockage: {storage_info['free']:.1f}GB libre sur {storage_info['total']:.1f}GB")
        
        # GPU Analysis
        gpu_info = self._analyze_gpus()
        print(f"🎮 GPU: {len(gpu_info)} dispositifs détectés")
        
        # OS Info
        os_info = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"
        print(f"🐧 OS: {os_info}")
        
        self.profile = HardwareProfile(
            cpu_cores=cpu_info['cores'],
            cpu_freq=cpu_info['freq'],
            ram_total=memory_info['total'],
            ram_available=memory_info['available'],
            disk_space=storage_info['free'],
            gpu_devices=gpu_info,
            os_info=os_info,
            architecture=platform.architecture()[0]
        )
        
        return self.profile
    
    def _analyze_cpu(self) -> Dict[str, Any]:
        """Analyse CPU détaillée"""
        try:
            # Get CPU brand from /proc/cpuinfo on Linux
            cpu_brand = "Unknown"
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            cpu_brand = line.split(':')[1].strip()
                            break
            except:
                cpu_brand = platform.processor()
            
            return {
                'brand': cpu_brand,
                'cores': psutil.cpu_count(logical=True),
                'physical_cores': psutil.cpu_count(logical=False),
                'freq': psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else 0.0,
                'freq_max': psutil.cpu_freq().max / 1000 if psutil.cpu_freq() else 0.0
            }
        except Exception as e:
            print(f"⚠️ Erreur analyse CPU: {e}")
            return {
                'brand': 'Unknown',
                'cores': psutil.cpu_count() or 4,
                'physical_cores': psutil.cpu_count(logical=False) or 2,
                'freq': 2.0,
                'freq_max': 3.0
            }
    
    def _analyze_memory(self) -> Dict[str, float]:
        """Analyse mémoire"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total / (1024**3),  # GB
            'available': memory.available / (1024**3),  # GB
            'used': memory.used / (1024**3),  # GB
            'percent': memory.percent
        }
    
    def _analyze_storage(self) -> Dict[str, float]:
        """Analyse stockage"""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total / (1024**3),  # GB
            'used': disk.used / (1024**3),  # GB
            'free': disk.free / (1024**3),  # GB
            'percent': (disk.used / disk.total) * 100
        }
    
    def _analyze_gpus(self) -> List[Dict[str, Any]]:
        """Analyse GPU disponibles"""
        gpus = []
        
        # Check for NVIDIA GPUs with nvidia-ml-py or nvidia-smi
        nvidia_gpus = self._check_nvidia_gpus()
        gpus.extend(nvidia_gpus)
        
        # Check for AMD GPUs
        amd_gpus = self._check_amd_gpus()
        gpus.extend(amd_gpus)
        
        # Check for Intel GPUs
        intel_gpus = self._check_intel_gpus()
        gpus.extend(intel_gpus)
        
        return gpus
    
    def _check_nvidia_gpus(self) -> List[Dict[str, Any]]:
        """Vérification GPU NVIDIA"""
        gpus = []
        
        try:
            # Try nvidia-smi command
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.free', 
                                   '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 3:
                            gpus.append({
                                'name': parts[0],
                                'vendor': 'NVIDIA',
                                'memory_total': int(parts[1]),
                                'memory_free': int(parts[2]),
                                'cuda_support': True,
                                'opencl_support': True
                            })
        except Exception as e:
            print(f"ℹ️ NVIDIA check: {e}")
        
        return gpus
    
    def _check_amd_gpus(self) -> List[Dict[str, Any]]:
        """Vérification GPU AMD"""
        gpus = []
        
        try:
            # Try rocm-smi or lspci for AMD GPUs
            result = subprocess.run(['lspci', '-nn'], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'VGA' in line and ('AMD' in line or 'Radeon' in line or 'ATI' in line):
                        # Extract GPU name
                        name_part = line.split(': ')[-1] if ': ' in line else line
                        gpus.append({
                            'name': name_part,
                            'vendor': 'AMD',
                            'memory_total': 'Unknown',
                            'memory_free': 'Unknown',
                            'cuda_support': False,
                            'opencl_support': True  # Most AMD GPUs support OpenCL
                        })
        except Exception as e:
            print(f"ℹ️ AMD check: {e}")
        
        return gpus
    
    def _check_intel_gpus(self) -> List[Dict[str, Any]]:
        """Vérification GPU Intel"""
        gpus = []
        
        try:
            result = subprocess.run(['lspci', '-nn'], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'VGA' in line and 'Intel' in line:
                        name_part = line.split(': ')[-1] if ': ' in line else line
                        gpus.append({
                            'name': name_part,
                            'vendor': 'Intel',
                            'memory_total': 'Shared',
                            'memory_free': 'Shared',
                            'cuda_support': False,
                            'opencl_support': True
                        })
        except Exception as e:
            print(f"ℹ️ Intel check: {e}")
        
        return gpus
    
    def analyze_target_gpus(self) -> Dict[str, GPUCapabilities]:
        """Analyse spécifique des GPU mentionnés"""
        
        target_gpus = {
            'rx480': GPUCapabilities(
                name="Radeon RX 480",
                memory_total=8192,  # 8GB GDDR5
                memory_available=7500,  # Estimation
                cuda_support=False,
                opencl_support=True,
                compute_capability=None,
                power_efficiency="Modérée (150W)",
                recommended_tasks=[
                    "Vectorisation dhātu (OpenCL)",
                    "Traitement parallèle corpus",
                    "Matrix operations",
                    "Large dataset processing"
                ]
            ),
            'quadro2000': GPUCapabilities(
                name="Quadro 2000",
                memory_total=1024,  # 1GB GDDR5
                memory_available=900,
                cuda_support=True,
                opencl_support=True,
                compute_capability="2.1",
                power_efficiency="Excellente (62W)",
                recommended_tasks=[
                    "CUDA kernels légers",
                    "Prototypage GPU",
                    "Tests développement",
                    "Small batch processing"
                ]
            ),
            'gtx750ti': GPUCapabilities(
                name="GTX 750 Ti",
                memory_total=2048,  # 2GB GDDR5
                memory_available=1800,
                cuda_support=True,
                opencl_support=True,
                compute_capability="5.0",
                power_efficiency="Très bonne (60W)",
                recommended_tasks=[
                    "CUDA development",
                    "Medium batch processing",
                    "ML inference",
                    "GPU computing tests"
                ]
            )
        }
        
        return target_gpus
    
    def generate_optimization_strategy(self) -> Dict[str, Any]:
        """Génère stratégie d'optimisation hybride"""
        
        if not self.profile:
            self.analyze_system()
        
        target_gpus = self.analyze_target_gpus()
        
        # Analyse des capacités locales
        local_capabilities = {
            'cpu_parallel': self.profile.cpu_cores >= 4,
            'memory_adequate': self.profile.ram_available >= 4.0,
            'storage_sufficient': self.profile.disk_space >= 10.0,
            'gpu_acceleration': len(self.profile.gpu_devices) > 0
        }
        
        # Stratégie d'utilisation
        strategy = {
            'local_strengths': [],
            'cloud_requirements': [],
            'hybrid_workflow': {},
            'gpu_recommendations': {},
            'cost_analysis': {}
        }
        
        # Analyse des forces locales
        if local_capabilities['cpu_parallel']:
            strategy['local_strengths'].append("Multi-core CPU processing")
        if local_capabilities['memory_adequate']:
            strategy['local_strengths'].append("RAM suffisante pour corpus moyens")
        if local_capabilities['storage_sufficient']:
            strategy['local_strengths'].append("Stockage pour données locales")
        
        # Recommandations GPU
        if self.profile.ram_available >= 6.0:
            strategy['gpu_recommendations']['rx480'] = {
                'priority': 'HIGH',
                'use_case': 'Large corpus processing avec OpenCL',
                'expected_speedup': '5-10x vs CPU',
                'memory_advantage': '8GB permet gros datasets'
            }
        
        if self.profile.cpu_cores >= 8:
            strategy['gpu_recommendations']['gtx750ti'] = {
                'priority': 'MEDIUM',
                'use_case': 'CUDA development et tests rapides',
                'expected_speedup': '3-5x vs CPU',
                'development_advantage': 'Cycle développement rapide'
            }
        
        strategy['gpu_recommendations']['quadro2000'] = {
            'priority': 'LOW',
            'use_case': 'Prototypage et tests légers uniquement',
            'expected_speedup': '2-3x vs CPU',
            'limitation': '1GB mémoire limite les datasets'
        }
        
        # Workflow hybride
        strategy['hybrid_workflow'] = {
            'local_tasks': [
                "Développement et prototypage",
                "Tests sur petits corpus (< 10k articles)",
                "Validation algorithmes",
                "Debugging et profiling"
            ],
            'colab_tasks': [
                "Traitement gros corpus (100k+ articles)",
                "Training ML models",
                "Benchmarks performance",
                "Validation finale algorithmes"
            ],
            'coordination': {
                'morning': 'Local development + small tests',
                'afternoon': 'Colab heavy processing (6h session)',
                'evening': 'Local analysis of Colab results'
            }
        }
        
        # Analyse coût-bénéfice
        strategy['cost_analysis'] = {
            'gpu_investment': {
                'rx480_benefits': '8GB mémoire = traitement local gros corpus',
                'cuda_benefits': 'Développement GPU kernels sans latence réseau',
                'power_cost': 'Estimation 50-100W = ~0.5€/jour si utilisé 10h'
            },
            'vs_cloud': {
                'colab_free': '12h/jour gratuit mais limité',
                'local_unlimited': 'Pas de quota, disponibilité 24/7',
                'hybrid_optimal': 'Meilleur des deux mondes'
            }
        }
        
        return strategy


def main():
    """Analyse principale et recommandations"""
    
    print("🏠 ANALYSE MATÉRIEL LOCAL + STRATÉGIE HYBRIDE")
    print("=" * 55)
    print("Optimisation dhātu processing avec ressources locales + gratuites")
    print()
    
    # Analyse système
    analyzer = LocalHardwareAnalyzer()
    profile = analyzer.analyze_system()
    
    print(f"\n📊 CAPACITÉS SYSTÈME:")
    print(f"   CPU: {profile.cpu_cores} cores @ {profile.cpu_freq:.1f}GHz")
    print(f"   RAM: {profile.ram_total:.1f}GB total, {profile.ram_available:.1f}GB libre")
    print(f"   Stockage: {profile.disk_space:.1f}GB disponible")
    print(f"   GPU: {len(profile.gpu_devices)} dispositifs")
    
    # Analyse GPU cibles
    target_gpus = analyzer.analyze_target_gpus()
    
    print(f"\n🎮 ANALYSE GPU CIBLES:")
    for gpu_key, gpu in target_gpus.items():
        print(f"   {gpu.name}:")
        print(f"     • Mémoire: {gpu.memory_total}MB")
        print(f"     • CUDA: {'✅' if gpu.cuda_support else '❌'}")
        print(f"     • OpenCL: {'✅' if gpu.opencl_support else '❌'}")
        print(f"     • Consommation: {gpu.power_efficiency}")
        print(f"     • Recommandé pour: {', '.join(gpu.recommended_tasks[:2])}")
    
    # Stratégie d'optimisation
    strategy = analyzer.generate_optimization_strategy()
    
    print(f"\n🚀 STRATÉGIE RECOMMANDÉE:")
    
    # GPU prioritaire
    if profile.ram_available >= 6.0:
        print(f"   🥇 GPU PRIORITAIRE: Radeon RX 480")
        print(f"     • 8GB mémoire = gros corpus locaux")
        print(f"     • OpenCL pour vectorisation dhātu")
        print(f"     • Speedup estimé: 5-10x vs CPU")
    
    # Workflow hybride
    print(f"\n📅 WORKFLOW HYBRIDE OPTIMAL:")
    print(f"   🌅 Matin (Local): Développement + tests rapides")
    print(f"   🌞 Après-midi (Colab): Gros processing 6h gratuit")
    print(f"   🌆 Soir (Local): Analyse résultats + itération")
    
    # Avantages locaux
    print(f"\n💪 AVANTAGES LOCAUX:")
    for strength in strategy['local_strengths']:
        print(f"   • {strength}")
    
    # Tasks distribution
    print(f"\n⚖️ RÉPARTITION TÂCHES:")
    print(f"   Local:")
    for task in strategy['hybrid_workflow']['local_tasks'][:3]:
        print(f"     • {task}")
    print(f"   Colab:")
    for task in strategy['hybrid_workflow']['colab_tasks'][:3]:
        print(f"     • {task}")
    
    # Recommandation finale
    if profile.ram_available >= 6.0 and profile.cpu_cores >= 4:
        recommendation = "INVESTIR dans RX 480 pour autonomie locale"
        priority = "HAUTE"
    elif profile.ram_available >= 4.0:
        recommendation = "GTX 750 Ti pour développement CUDA"
        priority = "MOYENNE"
    else:
        recommendation = "Focus sur Colab gratuit + optimisation CPU locale"
        priority = "CONTINUE ACTUEL"
    
    print(f"\n🎯 RECOMMANDATION FINALE:")
    print(f"   Priorité: {priority}")
    print(f"   Action: {recommendation}")
    
    # Sauvegarde analyse
    analysis_results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'hardware_profile': {
            'cpu_cores': profile.cpu_cores,
            'ram_gb': profile.ram_total,
            'disk_gb': profile.disk_space,
            'gpu_count': len(profile.gpu_devices)
        },
        'gpu_analysis': {k: {
            'name': v.name,
            'memory_mb': v.memory_total,
            'cuda': v.cuda_support,
            'priority_tasks': v.recommended_tasks[:3]
        } for k, v in target_gpus.items()},
        'strategy': strategy,
        'recommendation': {
            'priority': priority,
            'action': recommendation
        }
    }
    
    # Sauvegarder résultats
    with open('local_hardware_analysis.json', 'w') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Analyse sauvegardée: local_hardware_analysis.json")
    
    return analysis_results


if __name__ == "__main__":
    main()