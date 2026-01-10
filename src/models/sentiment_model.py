"""
Sentiment Analysis Model Module
Uses pre-trained transformer models for sentiment classification
"""

import os
from typing import Dict, List, Union
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment Analysis class using HuggingFace Transformers
    """
    
    def __init__(
        self,
        model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
        device: str = None,
        cache_dir: str = None
    ):
        """
        Initialize the sentiment analyzer
        
        Args:
            model_name: Name of the pre-trained model from HuggingFace
            device: Device to run the model on ('cuda', 'cpu', or None for auto)
            cache_dir: Directory to cache the model
        """
        self.model_name = model_name
        self.cache_dir = cache_dir or os.getenv("MODEL_CACHE_DIR", "./models")
        
        # Determine device
        if device is None:
            self.device = 0 if torch.cuda.is_available() else -1
        else:
            self.device = 0 if device == "cuda" and torch.cuda.is_available() else -1
        
        logger.info(f"Initializing model: {model_name}")
        logger.info(f"Using device: {'GPU' if self.device == 0 else 'CPU'}")
        
        # Load model and create pipeline
        self._load_model()
    
    def _load_model(self):
        """Load the model and tokenizer with memory optimization"""
        try:
            import gc
            
            # Create sentiment analysis pipeline with memory optimization
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=self.device,
                model_kwargs={
                    "cache_dir": self.cache_dir,
                    "torch_dtype": torch.float32,
                    "low_cpu_mem_usage": True
                }
            )
            
            # Clear memory after loading
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            logger.info("Model loaded successfully with memory optimization")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def analyze(self, text: str, return_all_scores: bool = False) -> Dict[str, Union[str, float, List]]:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Text to analyze
            return_all_scores: If True, return scores for all labels
            
        Returns:
            Dictionary with sentiment label and score
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            # Run prediction
            result = self.pipeline(text, return_all_scores=return_all_scores)
            
            if return_all_scores:
                return {
                    "text": text,
                    "predictions": result[0]
                }
            else:
                return {
                    "text": text,
                    "label": result[0]["label"],
                    "score": round(result[0]["score"], 4)
                }
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            raise
    
    def analyze_batch(
        self,
        texts: List[str],
        batch_size: int = 8,
        return_all_scores: bool = False
    ) -> List[Dict[str, Union[str, float, List]]]:
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts: List of texts to analyze
            batch_size: Batch size for processing
            return_all_scores: If True, return scores for all labels
            
        Returns:
            List of dictionaries with sentiment results
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")
        
        # Filter empty texts
        valid_texts = [t for t in texts if t and t.strip()]
        
        if not valid_texts:
            raise ValueError("All texts are empty")
        
        try:
            # Run batch prediction
            results = self.pipeline(
                valid_texts,
                batch_size=batch_size,
                return_all_scores=return_all_scores
            )
            
            # Format results
            formatted_results = []
            for text, result in zip(valid_texts, results):
                if return_all_scores:
                    formatted_results.append({
                        "text": text,
                        "predictions": result
                    })
                else:
                    formatted_results.append({
                        "text": text,
                        "label": result["label"],
                        "score": round(result["score"], 4)
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error in batch analysis: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "device": "GPU" if self.device == 0 else "CPU",
            "cache_dir": self.cache_dir
        }


# Singleton instance for the API
_analyzer_instance = None


def get_analyzer(
    model_name: str = None,
    device: str = None,
    cache_dir: str = None
) -> SentimentAnalyzer:
    """
    Get or create a singleton instance of SentimentAnalyzer
    
    This ensures we only load the model once for the entire application
    """
    global _analyzer_instance
    
    if _analyzer_instance is None:
        model_name = model_name or os.getenv(
            "MODEL_NAME",
            "distilbert-base-uncased-finetuned-sst-2-english"
        )
        _analyzer_instance = SentimentAnalyzer(
            model_name=model_name,
            device=device,
            cache_dir=cache_dir
        )
    
    return _analyzer_instance
