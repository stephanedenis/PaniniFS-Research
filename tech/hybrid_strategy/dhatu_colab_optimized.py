# Dhātu Processing - Session Colab Optimisée

## Configuration GPU
```python
import torch
import tensorflow as tf

# Vérifier GPU disponible
print("GPU disponible:", torch.cuda.is_available())
print("GPU device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")

# Configuration TensorFlow
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
```

## Synchronisation avec Local
```python
from google.colab import drive
drive.mount('/content/drive')

# Sync code depuis GitHub
!git clone https://github.com/stephanedenis/PaniniFS-Research.git
%cd PaniniFS-Research/tech

# Download latest local data
!wget -O corpus_data.gz "https://your-sync-url/corpus_data.gz"
!gunzip corpus_data.gz
```

## Traitement Intensif
```python
# Import modules dhātu optimisés
from dhatu_gpu_kernels import DhatuGPUKernels
from empirical_performance_benchmarks import PerformanceBenchmarker

# Configuration pour session longue
config = {
    'batch_size': 10000,        # Large batches avec GPU
    'gpu_memory_fraction': 0.9,
    'checkpoint_every': 5000,   # Sauvegarde fréquente
    'max_articles': 500000      # Limite pour session 12h
}

# Lancement traitement
gpu_kernels = DhatuGPUKernels()
benchmarker = PerformanceBenchmarker()

results = gpu_kernels.process_large_corpus(
    corpus_path='corpus_data.json',
    **config
)
```

## Sauvegarde Résultats
```python
import json
import gzip
from datetime import datetime

# Compresser résultats
output_data = {
    'timestamp': datetime.now().isoformat(),
    'session_config': config,
    'results': results,
    'performance_metrics': benchmarker.get_metrics()
}

# Sauvegarder compressé
with gzip.open('/content/drive/MyDrive/dhatu_results.json.gz', 'wt') as f:
    json.dump(output_data, f, indent=2)

print("✅ Résultats sauvegardés dans Google Drive")
```

## Monitoring Session
```python
import time
import psutil
from IPython.display import clear_output

def monitor_session():
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        hours_left = 12 - (elapsed / 3600)
        
        clear_output(wait=True)
        print(f"⏰ Session time: {elapsed/3600:.1f}h / 12h")
        print(f"🚨 Time remaining: {hours_left:.1f}h")
        print(f"💾 RAM usage: {psutil.virtual_memory().percent:.1f}%")
        
        if hours_left < 0.5:
            print("🚨 ATTENTION: Moins de 30min restantes!")
            break
            
        time.sleep(300)  # Check every 5 minutes

# Lancer monitoring en background
import threading
threading.Thread(target=monitor_session, daemon=True).start()
```
