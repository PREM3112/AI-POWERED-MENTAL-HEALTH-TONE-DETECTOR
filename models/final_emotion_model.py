import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    pass

class FinalEmotionAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        
        # PRECISE emotion mapping with priority ordering
        self.emotion_patterns = [
            # CRITICAL: Mental health crisis detection (highest priority)
            {'emotion': 'Depression', 'patterns': [
                "want to die", "end it all", "kill myself", "suicidal",
                "no point in anything", "everything feels meaningless"
            ], 'priority': 100},
            
            {'emotion': 'Panic', 'patterns': [
                "panic attack", "can't breathe", "freaking out"
            ], 'priority': 95},
            
            # Hopelessness (specific patterns)
            {'emotion': 'Hopelessness', 'patterns': [
                "so hopeless", "nothing works out", "never get better", 
                "always fail", "no hope", "completely hopeless"
            ], 'priority': 90},
            
            # Loneliness (specific patterns)
            {'emotion': 'Loneliness', 'patterns': [
                "completely alone", "no one cares", "isolated", "abandoned",
                "no friends", "by myself", "all alone"
            ], 'priority': 85},
            
            # Overwhelm (specific patterns)
            {'emotion': 'Overwhelm', 'patterns': [
                "so overwhelmed", "too much on my plate", "don't know where to start",
                "drowning in work", "can't handle everything", "swamped"
            ], 'priority': 85},
            
            # Stress (specific patterns)
            {'emotion': 'Stress', 'patterns': [
                "too many deadlines", "not enough time", "stretched thin",
                "pressure", "juggling too much", "exhausted from work"
            ], 'priority': 80},
            
            # Anxiety
            {'emotion': 'Anxiety', 'patterns': [
                "worrying about everything", "could go wrong", "heart racing",
                "can't stop thinking", "overthinking", "restless", "nervous"
            ], 'priority': 75},
            
            # Fear
            {'emotion': 'Fear', 'patterns': [
                "terrified", "scared to death", "what might happen",
                "fail this test", "afraid of", "fearful that"
            ], 'priority': 70},
            
            # Anger & Frustration
            {'emotion': 'Anger', 'patterns': [
                "so furious", "blood boil", "can't believe it",
                "enraged", "livid", "outraged"
            ], 'priority': 65},
            
            {'emotion': 'Frustration', 'patterns': [
                "so difficult", "tired of this", "why people",
                "frustrated", "stuck", "can't progress"
            ], 'priority': 60},
            
            {'emotion': 'Irritability', 'patterns': [
                "so irritated", "constant interruptions", "annoyed",
                "bothered", "aggravated", "on my nerves"
            ], 'priority': 55},
            
            # Positive Emotions
            {'emotion': 'Excitement', 'patterns': [
                "so excited", "can't wait", "promoted at work", "new opportunity",
                "thrilled about", "looking forward to"
            ], 'priority': 50},
            
            {'emotion': 'Joy', 'patterns': [
                "so happy", "overjoyed", "elated", "blissful", "ecstatic"
            ], 'priority': 45},
            
            {'emotion': 'Happiness', 'patterns': [
                "absolutely perfect", "great weather", "amazing food", 
                "wonderful company", "very happy", "good mood"
            ], 'priority': 40},
            
            {'emotion': 'Pride', 'patterns': [
                "achieved my goal", "proud of myself", "worked hard",
                "accomplished", "succeeded", "earned it"
            ], 'priority': 35},
            
            {'emotion': 'Gratitude', 'patterns': [
                "so grateful", "thankful for", "appreciate", "blessed",
                "fortunate to have", "lucky to be"
            ], 'priority': 30},
            
            # General fallbacks (lowest priority)
            {'emotion': 'Depression', 'patterns': [
                "empty inside", "nothing matters", "can't get out of bed"
            ], 'priority': 20},
            
            {'emotion': 'Anxiety', 'patterns': [
                "worried", "anxious", "stressed"
            ], 'priority': 15}
        ]
        
        # Emotion conflicts resolution
        self.conflict_resolution = {
            'Depression': ['Hopelessness', 'Loneliness'],  # Depression overrides these
            'Hopelessness': ['Depression'],  # But specific hopelessness patterns win
            'Loneliness': ['Depression'],    # Specific loneliness patterns win
            'Overwhelm': ['Stress', 'Anxiety'],  # Overwhelm is more specific than stress
            'Stress': ['Anxiety'],  # Stress is more specific than anxiety
            'Excitement': ['Joy', 'Happiness'],  # Excitement is more specific
        }

    def exact_pattern_match(self, text, patterns):
        """Check for exact phrase matches"""
        text_lower = text.lower()
        for pattern in patterns:
            if pattern in text_lower:
                return True
        return False

    def calculate_confidence(self, text, emotion, priority):
        """Calculate high confidence based on pattern match and priority"""
        base_confidence = 0.85 + (priority * 0.001)  # Higher priority = higher confidence
        
        # Boost for exact matches
        text_lower = text.lower()
        
        # Emotional intensity indicators
        if '!' in text:
            base_confidence += 0.03
        if any(word in text_lower for word in ['so', 'very', 'really', 'extremely']):
            base_confidence += 0.02
            
        # Crisis detection boost
        if emotion in ['Depression', 'Panic', 'Hopelessness']:
            base_confidence += 0.05
            
        return min(base_confidence, 0.98)

    def resolve_emotion_conflicts(self, detected_emotions):
        """Resolve conflicts between overlapping emotions"""
        if not detected_emotions:
            return None
            
        # Sort by priority (highest first)
        detected_emotions.sort(key=lambda x: x['priority'], reverse=True)
        
        # Get the highest priority emotion
        top_emotion = detected_emotions[0]
        
        # Check for conflicts
        for emotion_data in detected_emotions[1:]:
            emotion = emotion_data['emotion']
            if emotion in self.conflict_resolution.get(top_emotion['emotion'], []):
                # If current emotion should override the top one, swap them
                if top_emotion['emotion'] in self.conflict_resolution.get(emotion, []):
                    top_emotion = emotion_data
        
        return top_emotion

    def analyze_emotion(self, text):
        """Main analysis with conflict resolution"""
        if len(text.strip()) < 5:
            return "Neutral", 0.5
            
        text_lower = text.lower()
        detected_emotions = []
        
        # Check all emotion patterns in priority order
        for emotion_data in self.emotion_patterns:
            emotion = emotion_data['emotion']
            patterns = emotion_data['patterns']
            priority = emotion_data['priority']
            
            if self.exact_pattern_match(text_lower, patterns):
                confidence = self.calculate_confidence(text, emotion, priority)
                detected_emotions.append({
                    'emotion': emotion,
                    'confidence': confidence,
                    'priority': priority
                })
        
        # Resolve conflicts and get final emotion
        if detected_emotions:
            final_emotion_data = self.resolve_emotion_conflicts(detected_emotions)
            if final_emotion_data:
                return final_emotion_data['emotion'], round(final_emotion_data['confidence'], 3)
        
        # Fallback: Check for keyword presence
        text_words = set(text_lower.split())
        emotion_scores = {}
        
        for emotion_data in self.emotion_patterns:
            emotion = emotion_data['emotion']
            score = 0
            for pattern in emotion_data['patterns']:
                pattern_words = set(pattern.split())
                if pattern_words.issubset(text_words):
                    score += len(pattern_words) * 2
                else:
                    # Partial match
                    common_words = pattern_words.intersection(text_words)
                    score += len(common_words)
            
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            top_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            confidence = min(0.7 + (top_emotion[1] / 50), 0.85)
            return top_emotion[0], round(confidence, 3)
        
        # Final fallback: Sentiment analysis
        sentiment = self.sia.polarity_scores(text)['compound']
        if sentiment > 0.5:
            return "Positive", 0.7
        elif sentiment < -0.5:
            return "Negative", 0.7
        else:
            return "Neutral", 0.6

    def get_detailed_analysis(self, text):
        """Get comprehensive analysis"""
        emotion, confidence = self.analyze_emotion(text)
        
        return {
            'primary_emotion': emotion,
            'confidence': confidence,
            'intensity': 'High' if confidence > 0.9 else 'Medium' if confidence > 0.8 else 'Low'
        }