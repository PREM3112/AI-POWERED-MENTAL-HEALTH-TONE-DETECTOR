import numpy as np
import os
import requests
import json

class AudioFeatureExtractor:
    def __init__(self):
        self.sample_rate = 22050
        self.emotions = ['neutral', 'happy', 'sad', 'angry', 'fearful', 'disgusted', 'surprised']
        
    def extract_features(self, audio_path):
        """Extract audio features - keeping this for compatibility"""
        try:
            import librosa
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Basic features for fallback
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features = np.mean(mfcc, axis=1)
            return features
        except:
            return np.random.rand(13)
    
    def analyze_emotion_from_features(self, features):
        """Use multiple approaches for better emotion detection"""
        try:
            # Try different emotion detection methods
            emotion, confidence = self._method_advanced_rules(features)
            
            print(f"🎭 Final Detection: {emotion} (confidence: {confidence:.2f})")
            return emotion, confidence
            
        except Exception as e:
            print(f"❌ Emotion analysis error: {e}")
            return "neutral", 0.5
    
    def _method_advanced_rules(self, features):
        """Advanced rule-based emotion detection"""
        if features is None or len(features) < 5:
            return "neutral", 0.5
            
        try:
            import librosa
            import numpy as np
            
            # Load audio for detailed analysis
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Extract comprehensive features
            rms = librosa.feature.rms(y=y)[0]
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Calculate statistics
            avg_rms = np.mean(rms)
            avg_centroid = np.mean(spectral_centroids)
            centroid_std = np.std(spectral_centroids)
            avg_zcr = np.mean(zcr)
            zcr_std = np.std(zcr)
            mfcc_std = np.std(mfcc, axis=1)
            avg_mfcc_std = np.mean(mfcc_std)
            
            print(f"📊 Detailed Analysis:")
            print(f"   Volume: {avg_rms:.4f}")
            print(f"   Pitch: {avg_centroid:.0f} Hz")
            print(f"   Pitch Variation: {centroid_std:.0f}")
            print(f"   Speech Rate: {avg_zcr:.4f}")
            print(f"   Speech Variation: {zcr_std:.4f}")
            print(f"   Spectral Variation: {avg_mfcc_std:.4f}")
            
            # HAPPY/EXCITED characteristics:
            # - Moderate volume (0.03-0.08)
            # - Medium-high pitch (2000-4000 Hz)
            # - Moderate pitch variation (300-800)
            # - Fast but smooth speech (ZCR 0.07-0.12)
            # - Moderate spectral variation
            
            # ANGRY characteristics:
            # - High volume (>0.08)
            # - Very high pitch (>4000 Hz) 
            # - High pitch variation (>800)
            # - Very fast, choppy speech (ZCR > 0.12, high ZCR std)
            
            happy_score = 0
            angry_score = 0
            sad_score = 0
            neutral_score = 0
            
            # Score for HAPPY
            if 0.03 <= avg_rms <= 0.08:
                happy_score += 2
            if 2000 <= avg_centroid <= 4000:
                happy_score += 2
            if 300 <= centroid_std <= 800:
                happy_score += 1
            if 0.07 <= avg_zcr <= 0.12:
                happy_score += 2
            if zcr_std < 0.03:  # Smooth speech
                happy_score += 1
                
            # Score for ANGRY
            if avg_rms > 0.08:
                angry_score += 3
            if avg_centroid > 4000:
                angry_score += 2
            if centroid_std > 800:
                angry_score += 2
            if avg_zcr > 0.12:
                angry_score += 2
            if zcr_std > 0.04:  # Choppy speech
                angry_score += 1
                
            # Score for SAD
            if avg_rms < 0.03:
                sad_score += 3
            if avg_centroid < 1800:
                sad_score += 2
            if avg_zcr < 0.06:
                sad_score += 2
                
            # Score for NEUTRAL
            if 0.02 <= avg_rms <= 0.05:
                neutral_score += 1
            if 1500 <= avg_centroid <= 3000:
                neutral_score += 1
            if centroid_std < 500:
                neutral_score += 1
            if 0.05 <= avg_zcr <= 0.09:
                neutral_score += 1
            
            scores = {
                'happy': happy_score,
                'angry': angry_score, 
                'sad': sad_score,
                'neutral': neutral_score
            }
            
            print(f"🎯 Emotion Scores: {scores}")
            
            # Find best emotion
            best_emotion = max(scores, key=scores.get)
            best_score = scores[best_emotion]
            
            # Calculate confidence
            total_possible = 10  # Maximum possible score
            confidence = min(0.95, best_score / total_possible)
            
            # If scores are too close or low, default to neutral
            if best_score < 3:
                best_emotion = "neutral"
                confidence = 0.6
                
            return best_emotion, confidence
            
        except Exception as e:
            print(f"❌ Advanced rules failed: {e}")
            return "neutral", 0.5

    def _method_simple_test(self, audio_path):
        """Simple test method that always returns happy for testing"""
        print("🎯 USING TEST MODE: Always returning 'happy'")
        return "happy", 0.85