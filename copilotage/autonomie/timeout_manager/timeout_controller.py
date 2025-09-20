#!/usr/bin/env python3
"""
Module TIMEOUT_MANAGER - Gestion timeouts adaptatifs et continuation missions

Objectif: Éliminer blocages par timeouts via système intelligent avec 
save/resume automatique et timeouts adaptatifs selon contexte opération.

Architecture:
- AdaptiveTimeoutController: Timeouts dynamiques selon historique
- StateCheckpointer: Sauvegarde continue état pour reprise
- ContinuationEngine: Reprise automatique missions interrompues
- TimeoutPredictor: Prédiction timeouts optimaux selon opération

Priorité: CRITIQUE - Élimination boucles d'attente infinies
"""

import asyncio
import json
import pickle
import time
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Awaitable
from dataclasses import dataclass, asdict
import threading
import signal
import sys


class TimeoutCategory(Enum):
    """Catégories timeouts selon type opération"""
    NETWORK_REQUEST = "network_request"      # API calls, downloads
    FILE_OPERATION = "file_operation"        # Read/write, processing
    COMPUTATION = "computation"              # CPU intensive tasks
    USER_INPUT = "user_input"               # Prompts, interactions
    EXTERNAL_TOOL = "external_tool"         # Subprocess, CLI tools
    DATABASE = "database"                   # DB operations
    UNKNOWN = "unknown"                     # Non classifié


class TimeoutStrategy(Enum):
    """Stratégies gestion timeout"""
    ADAPTIVE = "adaptive"           # Timeout adaptatif selon historique
    PROGRESSIVE = "progressive"     # Augmentation progressive timeout
    FIXED = "fixed"                # Timeout fixe
    CONTEXT_AWARE = "context_aware" # Timeout selon criticité contexte
    UNLIMITED = "unlimited"         # Pas de timeout (autonomie maximale)


@dataclass
class TimeoutConfig:
    """Configuration timeout pour opération"""
    category: TimeoutCategory
    strategy: TimeoutStrategy
    base_timeout: float
    max_timeout: float
    min_timeout: float
    retry_multiplier: float
    context_factors: Dict[str, float]


@dataclass
class OperationHistory:
    """Historique performance opération"""
    operation_type: str
    category: TimeoutCategory
    execution_times: list[float]
    success_rate: float
    average_time: float
    percentile_95: float
    last_updated: datetime


@dataclass
class CheckpointData:
    """Données checkpoint pour reprise"""
    checkpoint_id: str
    operation_type: str
    timestamp: datetime
    execution_context: Dict[str, Any]
    intermediate_state: Any
    progress_percentage: float
    estimated_remaining_time: float


class TimeoutPredictor:
    """Prédicteur timeouts optimaux selon historique"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.history_dir = self.workspace_root / "copilotage" / "autonomie" / "timeout_data"
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.history_dir / "operation_history.json"
        self.operation_history = self._load_history()
        
    def _load_history(self) -> Dict[str, OperationHistory]:
        """Chargement historique opérations"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    
                history = {}
                for op_type, op_data in data.items():
                    op_data['last_updated'] = datetime.fromisoformat(op_data['last_updated'])
                    op_data['category'] = TimeoutCategory(op_data['category'])
                    history[op_type] = OperationHistory(**op_data)
                    
                return history
            except Exception:
                return {}
        return {}
    
    def _save_history(self):
        """Sauvegarde historique"""
        data = {}
        for op_type, history in self.operation_history.items():
            history_dict = asdict(history)
            history_dict['last_updated'] = history.last_updated.isoformat()
            history_dict['category'] = history.category.value
            data[op_type] = history_dict
            
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def record_execution(self, operation_type: str, category: TimeoutCategory, 
                        execution_time: float, success: bool):
        """Enregistrement temps exécution"""
        
        if operation_type not in self.operation_history:
            self.operation_history[operation_type] = OperationHistory(
                operation_type=operation_type,
                category=category,
                execution_times=[],
                success_rate=0.0,
                average_time=0.0,
                percentile_95=0.0,
                last_updated=datetime.now()
            )
        
        history = self.operation_history[operation_type]
        
        # Mise à jour historique (garde les 100 dernières mesures)
        history.execution_times.append(execution_time)
        if len(history.execution_times) > 100:
            history.execution_times = history.execution_times[-100:]
        
        # Recalcul statistiques
        times = history.execution_times
        history.average_time = sum(times) / len(times)
        history.percentile_95 = sorted(times)[int(len(times) * 0.95)]
        history.last_updated = datetime.now()
        
        # Sauvegarde
        self._save_history()
    
    def predict_timeout(self, operation_type: str, category: TimeoutCategory,
                       context: Dict[str, Any] = None) -> float:
        """Prédiction timeout optimal"""
        
        if operation_type in self.operation_history:
            history = self.operation_history[operation_type]
            
            # Base sur percentile 95 + marge sécurité
            base_timeout = history.percentile_95 * 1.5
            
            # Ajustement selon contexte
            if context:
                criticality = context.get('criticality', 'normal')
                data_size = context.get('data_size', 1.0)
                
                if criticality == 'high':
                    base_timeout *= 2.0  # Plus de temps pour opérations critiques
                elif criticality == 'low':
                    base_timeout *= 0.8  # Moins de temps pour opérations peu importantes
                    
                # Ajustement selon taille données
                if data_size > 1.0:
                    base_timeout *= (1.0 + (data_size - 1.0) * 0.5)
            
            return max(base_timeout, self._get_default_timeout(category))
        
        else:
            # Pas d'historique - utiliser défauts
            return self._get_default_timeout(category)
    
    def _get_default_timeout(self, category: TimeoutCategory) -> float:
        """Timeouts par défaut selon catégorie"""
        defaults = {
            TimeoutCategory.NETWORK_REQUEST: 30.0,
            TimeoutCategory.FILE_OPERATION: 60.0,
            TimeoutCategory.COMPUTATION: 300.0,
            TimeoutCategory.USER_INPUT: 5.0,  # Court pour autonomie
            TimeoutCategory.EXTERNAL_TOOL: 120.0,
            TimeoutCategory.DATABASE: 45.0,
            TimeoutCategory.UNKNOWN: 60.0
        }
        return defaults.get(category, 60.0)


class StateCheckpointer:
    """Gestionnaire checkpoints pour reprise automatique"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.checkpoint_dir = self.workspace_root / "copilotage" / "autonomie" / "checkpoints"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        self.active_checkpoints = {}  # operation_id -> checkpoint_data
        
    def create_checkpoint(self, operation_id: str, operation_type: str,
                         execution_context: Dict[str, Any],
                         intermediate_state: Any,
                         progress_percentage: float = 0.0) -> str:
        """Création checkpoint"""
        
        checkpoint_id = f"checkpoint_{operation_id}_{int(time.time())}"
        
        checkpoint_data = CheckpointData(
            checkpoint_id=checkpoint_id,
            operation_type=operation_type,
            timestamp=datetime.now(),
            execution_context=execution_context,
            intermediate_state=intermediate_state,
            progress_percentage=progress_percentage,
            estimated_remaining_time=0.0
        )
        
        # Sauvegarde sur disque
        checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.pkl"
        with open(checkpoint_file, 'wb') as f:
            pickle.dump(checkpoint_data, f)
            
        # Garde en mémoire pour accès rapide
        self.active_checkpoints[operation_id] = checkpoint_data
        
        return checkpoint_id
    
    def update_checkpoint(self, operation_id: str, progress_percentage: float,
                         intermediate_state: Any = None,
                         estimated_remaining_time: float = None):
        """Mise à jour checkpoint existant"""
        
        if operation_id in self.active_checkpoints:
            checkpoint = self.active_checkpoints[operation_id]
            checkpoint.progress_percentage = progress_percentage
            
            if intermediate_state is not None:
                checkpoint.intermediate_state = intermediate_state
                
            if estimated_remaining_time is not None:
                checkpoint.estimated_remaining_time = estimated_remaining_time
            
            # Sauvegarde mise à jour
            checkpoint_file = self.checkpoint_dir / f"{checkpoint.checkpoint_id}.pkl"
            with open(checkpoint_file, 'wb') as f:
                pickle.dump(checkpoint, f)
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointData]:
        """Chargement checkpoint depuis disque"""
        checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.pkl"
        
        if checkpoint_file.exists():
            try:
                with open(checkpoint_file, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                return None
        return None
    
    def list_resumable_operations(self) -> list[CheckpointData]:
        """Liste opérations resumables"""
        resumable = []
        
        for checkpoint_file in self.checkpoint_dir.glob("*.pkl"):
            try:
                with open(checkpoint_file, 'rb') as f:
                    checkpoint = pickle.load(f)
                    
                # Vérifie si checkpoint récent (< 24h)
                if (datetime.now() - checkpoint.timestamp).days < 1:
                    resumable.append(checkpoint)
                    
            except Exception:
                continue
                
        return sorted(resumable, key=lambda x: x.timestamp, reverse=True)
    
    def cleanup_old_checkpoints(self, max_age_hours: int = 48):
        """Nettoyage anciens checkpoints"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for checkpoint_file in self.checkpoint_dir.glob("*.pkl"):
            try:
                with open(checkpoint_file, 'rb') as f:
                    checkpoint = pickle.load(f)
                    
                if checkpoint.timestamp < cutoff_time:
                    checkpoint_file.unlink()
                    
            except Exception:
                # Fichier corrompu - supprimer
                checkpoint_file.unlink()


class ContinuationEngine:
    """Moteur continuation automatique missions"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.checkpointer = StateCheckpointer(workspace_root)
        
        # Registre fonctions continuation
        self.continuation_handlers = {}
        
    def register_continuation_handler(self, operation_type: str, 
                                    handler_func: Callable[[CheckpointData], Any]):
        """Enregistrement handler continuation pour type opération"""
        self.continuation_handlers[operation_type] = handler_func
    
    def can_continue_operation(self, checkpoint: CheckpointData) -> bool:
        """Vérifie si opération peut être continuée"""
        
        # Handler disponible ?
        if checkpoint.operation_type not in self.continuation_handlers:
            return False
            
        # Checkpoint pas trop ancien ?
        age_hours = (datetime.now() - checkpoint.timestamp).total_seconds() / 3600
        if age_hours > 24:  # 24h max
            return False
            
        # Contexte encore valide ?
        context = checkpoint.execution_context
        if context.get('context_invalid', False):
            return False
            
        return True
    
    async def continue_operation(self, checkpoint: CheckpointData) -> Any:
        """Continuation opération depuis checkpoint"""
        
        if not self.can_continue_operation(checkpoint):
            raise Exception(f"Cannot continue operation {checkpoint.operation_type}")
            
        handler = self.continuation_handlers[checkpoint.operation_type]
        
        # Appel handler continuation
        try:
            result = handler(checkpoint)
            
            # Si handler retourne coroutine
            if asyncio.iscoroutine(result):
                result = await result
                
            return result
            
        except Exception as e:
            raise Exception(f"Continuation failed: {e}")
    
    def auto_resume_interrupted_operations(self) -> list[Any]:
        """Reprise automatique opérations interrompues"""
        results = []
        
        # Recherche opérations resumables
        resumable_ops = self.checkpointer.list_resumable_operations()
        
        for checkpoint in resumable_ops:
            if self.can_continue_operation(checkpoint):
                try:
                    # Reprise asynchrone
                    loop = asyncio.get_event_loop()
                    result = loop.run_until_complete(self.continue_operation(checkpoint))
                    results.append({
                        "checkpoint_id": checkpoint.checkpoint_id,
                        "operation_type": checkpoint.operation_type,
                        "result": result,
                        "resumed_at": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    results.append({
                        "checkpoint_id": checkpoint.checkpoint_id,
                        "operation_type": checkpoint.operation_type,
                        "error": str(e),
                        "failed_at": datetime.now().isoformat()
                    })
        
        return results


class AdaptiveTimeoutController:
    """Contrôleur principal timeouts adaptatifs"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        
        # Composants timeout
        self.predictor = TimeoutPredictor(workspace_root)
        self.checkpointer = StateCheckpointer(workspace_root)
        self.continuation_engine = ContinuationEngine(workspace_root)
        
        # Configuration timeouts par défaut
        self.timeout_configs = self._load_timeout_configs()
        
        # Opérations actives avec timeouts
        self.active_operations = {}
        
    def _load_timeout_configs(self) -> Dict[TimeoutCategory, TimeoutConfig]:
        """Configuration timeouts par catégorie"""
        return {
            TimeoutCategory.NETWORK_REQUEST: TimeoutConfig(
                category=TimeoutCategory.NETWORK_REQUEST,
                strategy=TimeoutStrategy.ADAPTIVE,
                base_timeout=30.0,
                max_timeout=300.0,
                min_timeout=5.0,
                retry_multiplier=1.5,
                context_factors={'criticality_high': 2.0, 'criticality_low': 0.5}
            ),
            
            TimeoutCategory.FILE_OPERATION: TimeoutConfig(
                category=TimeoutCategory.FILE_OPERATION,
                strategy=TimeoutStrategy.CONTEXT_AWARE,
                base_timeout=60.0,
                max_timeout=600.0,
                min_timeout=1.0,
                retry_multiplier=1.3,
                context_factors={'large_file': 3.0, 'small_file': 0.5}
            ),
            
            TimeoutCategory.COMPUTATION: TimeoutConfig(
                category=TimeoutCategory.COMPUTATION,
                strategy=TimeoutStrategy.PROGRESSIVE,
                base_timeout=300.0,
                max_timeout=3600.0,
                min_timeout=10.0,
                retry_multiplier=2.0,
                context_factors={'complex_computation': 5.0}
            ),
            
            TimeoutCategory.USER_INPUT: TimeoutConfig(
                category=TimeoutCategory.USER_INPUT,
                strategy=TimeoutStrategy.FIXED,
                base_timeout=5.0,  # Court pour autonomie
                max_timeout=10.0,
                min_timeout=1.0,
                retry_multiplier=1.0,
                context_factors={}
            ),
            
            TimeoutCategory.EXTERNAL_TOOL: TimeoutConfig(
                category=TimeoutCategory.EXTERNAL_TOOL,
                strategy=TimeoutStrategy.ADAPTIVE,
                base_timeout=120.0,
                max_timeout=1800.0,
                min_timeout=5.0,
                retry_multiplier=1.8,
                context_factors={'heavy_tool': 4.0, 'light_tool': 0.3}
            )
        }
    
    def calculate_timeout(self, operation_type: str, category: TimeoutCategory,
                         context: Dict[str, Any] = None,
                         attempt_number: int = 1) -> float:
        """Calcul timeout adaptatif pour opération"""
        
        config = self.timeout_configs.get(category)
        if not config:
            return 60.0  # Défaut
            
        # Prédiction base selon historique
        predicted_timeout = self.predictor.predict_timeout(
            operation_type, category, context
        )
        
        # Application stratégie
        if config.strategy == TimeoutStrategy.ADAPTIVE:
            timeout = predicted_timeout
            
        elif config.strategy == TimeoutStrategy.PROGRESSIVE:
            timeout = config.base_timeout * (config.retry_multiplier ** (attempt_number - 1))
            
        elif config.strategy == TimeoutStrategy.FIXED:
            timeout = config.base_timeout
            
        elif config.strategy == TimeoutStrategy.CONTEXT_AWARE:
            timeout = config.base_timeout
            
            # Application facteurs contexte
            if context:
                for factor_key, multiplier in config.context_factors.items():
                    if context.get(factor_key, False):
                        timeout *= multiplier
                        
        elif config.strategy == TimeoutStrategy.UNLIMITED:
            return float('inf')  # Pas de timeout
            
        else:
            timeout = predicted_timeout
        
        # Contraintes min/max
        timeout = max(config.min_timeout, min(timeout, config.max_timeout))
        
        return timeout
    
    async def execute_with_timeout(self, operation_func: Callable,
                                 operation_type: str,
                                 category: TimeoutCategory,
                                 context: Dict[str, Any] = None,
                                 enable_checkpoints: bool = True) -> Any:
        """Exécution avec timeout adaptatif et checkpoints"""
        
        if context is None:
            context = {}
            
        operation_id = f"{operation_type}_{int(time.time())}"
        
        # Calcul timeout initial
        timeout_duration = self.calculate_timeout(operation_type, category, context)
        
        # Création checkpoint initial si activé
        checkpoint_id = None
        if enable_checkpoints:
            checkpoint_id = self.checkpointer.create_checkpoint(
                operation_id, operation_type, context, None, 0.0
            )
        
        start_time = time.time()
        
        try:
            # Exécution avec timeout
            if asyncio.iscoroutinefunction(operation_func):
                result = await asyncio.wait_for(operation_func(), timeout=timeout_duration)
            else:
                # Fonction sync - wrap dans coroutine
                async def _sync_wrapper():
                    return operation_func()
                result = await asyncio.wait_for(_sync_wrapper(), timeout=timeout_duration)
            
            # Enregistrement succès
            execution_time = time.time() - start_time
            self.predictor.record_execution(operation_type, category, execution_time, True)
            
            # Nettoyage checkpoint si succès
            if checkpoint_id:
                checkpoint_file = self.checkpointer.checkpoint_dir / f"{checkpoint_id}.pkl"
                if checkpoint_file.exists():
                    checkpoint_file.unlink()
            
            return result
            
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            
            # Enregistrement timeout
            self.predictor.record_execution(operation_type, category, execution_time, False)
            
            # Gestion timeout avec checkpoint
            if enable_checkpoints and checkpoint_id:
                
                # Mise à jour checkpoint avec état actuel
                self.checkpointer.update_checkpoint(
                    operation_id, 
                    progress_percentage=50.0,  # Estimation
                    estimated_remaining_time=timeout_duration
                )
                
                # En mode autonomie - tentative continuation automatique
                if context.get('autonomy_level') == 'full_autonomous':
                    
                    # Tentative retry avec timeout augmenté
                    retry_timeout = timeout_duration * 2.0
                    
                    try:
                        if asyncio.iscoroutinefunction(operation_func):
                            result = await asyncio.wait_for(operation_func(), timeout=retry_timeout)
                        else:
                            async def _sync_wrapper():
                                return operation_func()
                            result = await asyncio.wait_for(_sync_wrapper(), timeout=retry_timeout)
                        
                        # Succès retry
                        execution_time = time.time() - start_time
                        self.predictor.record_execution(operation_type, category, execution_time, True)
                        
                        return result
                        
                    except asyncio.TimeoutError:
                        # Double timeout - sauvegarde état et continue
                        timeout_result = context.get('timeout_fallback_value')
                        return timeout_result
            
            # Timeout sans récupération possible
            raise TimeoutError(f"Operation {operation_type} timed out after {timeout_duration}s")


def create_timeout_manager(workspace_root: str) -> AdaptiveTimeoutController:
    """Factory création gestionnaire timeouts"""
    return AdaptiveTimeoutController(Path(workspace_root))


# Décorateur timeout adaptatif
def adaptive_timeout(operation_type: str, category: TimeoutCategory, 
                    context: Dict[str, Any] = None,
                    enable_checkpoints: bool = True):
    """Décorateur timeout adaptatif"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Récupération manager depuis contexte global ou création
            manager = getattr(wrapper, '_timeout_manager', None)
            if not manager:
                manager = create_timeout_manager("/home/stephane/GitHub/PaniniFS-Research")
                wrapper._timeout_manager = manager
            
            # Exécution avec timeout adaptatif
            return await manager.execute_with_timeout(
                lambda: func(*args, **kwargs),
                operation_type,
                category,
                context,
                enable_checkpoints
            )
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test gestionnaire timeouts
    async def test_timeout_manager():
        manager = create_timeout_manager("/home/stephane/GitHub/PaniniFS-Research")
        
        # Test opération normale
        async def normal_operation():
            await asyncio.sleep(1)
            return "Success"
        
        result = await manager.execute_with_timeout(
            normal_operation,
            "test_operation",
            TimeoutCategory.COMPUTATION,
            {"criticality": "normal"}
        )
        print(f"Résultat normal: {result}")
        
        # Test opération avec timeout
        async def slow_operation():
            await asyncio.sleep(10)  # Plus long que timeout
            return "Should not reach here"
        
        try:
            result = await manager.execute_with_timeout(
                slow_operation,
                "slow_test",
                TimeoutCategory.NETWORK_REQUEST,
                {
                    "criticality": "low",
                    "autonomy_level": "full_autonomous",
                    "timeout_fallback_value": "Timeout fallback"
                }
            )
            print(f"Résultat timeout géré: {result}")
            
        except Exception as e:
            print(f"Erreur timeout: {e}")
    
    # Lancement test
    asyncio.run(test_timeout_manager())