"""
Production memory optimization configuration
For deployment on platforms with limited memory (512MB)
"""

import os
import gc


def optimize_memory():
    """
    Optimize memory usage for production deployment
    Call this after loading the model
    """
    import torch
    
    # Force garbage collection
    gc.collect()
    
    # Clear CUDA cache if available
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Set environment variables for memory optimization
    os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = '1'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'


def get_optimized_pipeline_kwargs():
    """
    Get optimized kwargs for pipeline creation
    """
    import torch
    
    return {
        "torch_dtype": torch.float32,
        "low_cpu_mem_usage": True,
    }


# Set optimization flags on import
os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
