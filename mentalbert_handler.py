import torch
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List
import os

class MentalBERTAnalyzer:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.classifier = None
        self.is_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load MentalBERT model with fallbacks"""
        try:
            logging.info("🚀 Loading MentalBERT for mental health analysis...")
            
            # Try MentalBERT first (domain-specific)
            model_name = "mental/mental-bert"
            
            self.classifier = pipeline(
                "text-classification",
                model=model_name,
                tokenizer=model_name,
                return_all_scores=True,
                device=0 if torch.cuda.is_available() else -1,
                max_length=512,
                truncation=True
            )
            
            self.is_loaded = True
            logging.info("✅ MentalBERT loaded successfully!")
            
        except Exception as e:
            logging.warning(f"⚠️ MentalBERT failed: {e}. Loading fallback model...")
            self.load_fallback_model()
    
    def load_fallback_model(self):
        """Load fallback emotion model"""
        try:
            self.classifier = pipeline(
                "text-classification",
                model="bhadresh-savani/bert-base-uncased-emotion",
                return_all_scores=True
            )
            self.is_loaded = True
            logging.info("✅ Fallback emotion model loaded")
        except Exception as e:
            logging.error(f"❌ All models failed to load: {e}")
            self.is_loaded = False
    
    def analyze_text(self, text: str) -> Dict:
        """Main analysis function"""
        if not self.is_loaded:
            return self._error_response("Model not loaded")
        
        if not text or len(text.strip()) < 5:
            return self._empty_response()
        
        try:
            # Clean and truncate text
            clean_text = text.strip()[:1000]
            
            # Get predictions
            results = self.classifier(clean_text)
            
            # Process based on model type
            if isinstance(results[0], list):
                return self._process_mentalbert_output(results[0], clean_text)
            else:
                return self._process_emotion_output(results, clean_text)
                
        except Exception as e:
            logging.error(f"Analysis error: {e}")
            return self._error_response(str(e))
    
    def _process_mentalbert_output(self, scores: List[Dict], text: str) -> Dict:
        """Process MentalBERT specific output"""
        # Convert to simple dict
        score_dict = {item['label'].lower(): item['score'] for item in scores}
        
        # Map to standard mental health categories
        analysis = {
            'depression': score_dict.get('depression', 0.0),
            'anxiety': score_dict.get('anxiety', 0.0),
            'stress': score_dict.get('stress', 0.0),
            'suicide_risk': score_dict.get('suicide', 0.0),
            'neutral': score_dict.get('neutral', 0.1),
            'positive': score_dict.get('positive', score_dict.get('joy', 0.1))
        }
        
        # Find primary tone
        primary_tone = max(analysis.items(), key=lambda x: x[1])
        
        return {
            'primary_tone': primary_tone[0],
            'confidence': float(primary_tone[1]),
            'risk_level': self._assess_risk(analysis, text),
            'categories': analysis,
            'urgency': self._determine_urgency(analysis, text),
            'model_used': 'mentalbert'
        }
    
    def _process_emotion_output(self, results: List[Dict], text: str) -> Dict:
        """Process emotion model output"""
        emotions = {item['label'].lower(): item['score'] for item in results[0]}
        
        # Map emotions to mental health categories
        analysis = {
            'depression': emotions.get('sadness', 0.0),
            'anxiety': emotions.get('fear', 0.0),
            'stress': emotions.get('anger', 0.0),
            'suicide_risk': 0.0,  # Emotion model doesn't detect this
            'neutral': emotions.get('surprise', 0.1),
            'positive': emotions.get('joy', 0.0) + emotions.get('love', 0.0)
        }
        
        primary_tone = max(analysis.items(), key=lambda x: x[1])
        
        return {
            'primary_tone': primary_tone[0],
            'confidence': float(primary_tone[1]),
            'risk_level': self._assess_risk(analysis, text),
            'categories': analysis,
            'urgency': self._determine_urgency(analysis, text),
            'model_used': 'emotion-bert'
        }
    
    def _assess_risk(self, categories: Dict, text: str) -> str:
        """Assess overall risk level"""
        text_lower = text.lower()
        
        # Crisis keyword detection
        crisis_words = ['suicide', 'kill myself', 'end my life', 'want to die']
        if any(word in text_lower for word in crisis_words):
            return 'severe'
        
        # Score-based assessment
        risk_score = (
            categories['depression'] * 0.4 +
            categories['anxiety'] * 0.3 +
            categories['suicide_risk'] * 0.3
        )
        
        if risk_score > 0.7:
            return 'high'
        elif risk_score > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _determine_urgency(self, categories: Dict, text: str) -> str:
        """Determine urgency level"""
        risk_level = self._assess_risk(categories, text)
        return 'high' if risk_level in ['severe', 'high'] else 'medium'
    
    def _empty_response(self) -> Dict:
        return {
            'primary_tone': 'neutral',
            'confidence': 0.0,
            'risk_level': 'low',
            'categories': {
                'depression': 0.0, 'anxiety': 0.0, 'stress': 0.0,
                'suicide_risk': 0.0, 'neutral': 1.0, 'positive': 0.0
            },
            'urgency': 'low',
            'model_used': 'none'
        }
    
    def _error_response(self, error: str) -> Dict:
        response = self._empty_response()
        response['error'] = error
        return response

# Global instance for easy import
mentalbert_analyzer = MentalBERTAnalyzer()