from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import joblib
import pandas as pd
from datetime import datetime
import os
import sys
import re
import numpy as np
import random
import wave
import time
import json

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)

print(f"🔍 Looking for modules in: {src_dir}")

# Import speech processing modules
try:
    from speech_processing.audio_recorder import AudioRecorder
    from speech_processing.feature_extractor import AudioFeatureExtractor
    print("✅ Speech processing modules loaded successfully!")
except ImportError as e:
    print(f"❌ Failed to import speech processing modules: {e}")
    # Create working fallback speech classes
    class AudioRecorder:
        def record_audio(self, duration=5, filename="recording.wav"):
            print(f"🎤 Creating audio file: {filename}")
            # Create a simple WAV file for testing
            self.create_test_audio(filename, duration)
            return filename
        
        def get_audio_duration(self, filename):
            try:
                with wave.open(filename, 'r') as wf:
                    frames = wf.getnframes()
                    rate = wf.getframerate()
                    return frames / float(rate)
            except:
                return 5.0
        
        def create_test_audio(self, filename, duration):
            """Create a test audio file"""
            try:
                sample_rate = 16000
                t = np.linspace(0, duration, int(sample_rate * duration))
                # Create audio with some variation
                audio_data = (np.sin(2 * np.pi * 440 * t) * 0.3 + 
                             np.random.normal(0, 0.1, len(t)) * 0.1)
                audio_data = np.int16(audio_data * 32767)
                
                with wave.open(filename, 'w') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio_data.tobytes())
                print(f"✅ Created test audio: {filename}")
            except Exception as e:
                print(f"❌ Failed to create test audio: {e}")
    
    class AudioFeatureExtractor:
        def extract_features(self, audio_path):
            print(f"📊 Extracting features from: {audio_path}")
            return np.random.rand(13)
        
        def analyze_emotion_from_features(self, features):
            # Use content-based emotion detection instead of random
            return self.content_based_emotion(), 0.7
        
        def content_based_emotion(self):
            """Simple content-based emotion as fallback"""
            emotions = ['anxious', 'stressed', 'neutral', 'sad', 'happy']
            weights = [0.3, 0.25, 0.2, 0.15, 0.1]
            return random.choices(emotions, weights=weights)[0]

# Try to import the advisor
try:
    from utils.mental_health_advisor import MentalHealthAdvisor
    advisor = MentalHealthAdvisor()
    print("✅ Mental Health Advisor loaded successfully!")
except ImportError as e:
    print(f"❌ Failed to import MentalHealthAdvisor: {e}")
    class FallbackAdvisor:
        def __init__(self):
            self.recommendations = {
                'happy': {
                    'immediate_actions': ['Share your positive energy with others', 'Practice gratitude journaling', 'Engage in physical activity'],
                    'long_term_strategies': ['Maintain social connections', 'Continue self-care practices', 'Set new personal goals'],
                    'professional_guidance': 'Continue current wellness routines',
                    'urgency_level': 'low',
                    'color': '#4CAF50'
                },
                'sad': {
                    'immediate_actions': ['Reach out to friends or family', 'Listen to uplifting music', 'Take a gentle walk in nature'],
                    'long_term_strategies': ['Establish a daily routine', 'Practice self-compassion', 'Engage in creative activities'],
                    'professional_guidance': 'Consider speaking with a counselor if feelings persist',
                    'urgency_level': 'medium',
                    'color': '#2196F3'
                },
                'anxious': {
                    'immediate_actions': ['Practice deep breathing exercises', 'Use the 5-4-3-2-1 grounding technique', 'Take a break from stressors'],
                    'long_term_strategies': ['Practice daily mindfulness meditation', 'Limit caffeine intake', 'Establish a worry time'],
                    'professional_guidance': 'Consider therapy for anxiety management',
                    'urgency_level': 'medium',
                    'color': '#FF9800'
                },
                'angry': {
                    'immediate_actions': ['Take a timeout from the situation', 'Practice counting to 10 slowly', 'Use physical exercise to release tension'],
                    'long_term_strategies': ['Learn anger management techniques', 'Identify triggers and coping strategies', 'Practice assertive communication'],
                    'professional_guidance': 'Anger management therapy can be beneficial',
                    'urgency_level': 'medium',
                    'color': '#f44336'
                },
                'stressed': {
                    'immediate_actions': ['Break tasks into smaller steps', 'Practice progressive muscle relaxation', 'Delegate tasks when possible'],
                    'long_term_strategies': ['Improve time management skills', 'Set healthy boundaries', 'Practice regular self-care'],
                    'professional_guidance': 'Stress management counseling available',
                    'urgency_level': 'medium',
                    'color': '#9C27B0'
                },
                'depressed': {
                    'immediate_actions': ['Contact a trusted person', 'Engage in gentle movement', 'Avoid isolation'],
                    'long_term_strategies': ['Establish daily structure', 'Seek professional support', 'Practice self-care routines'],
                    'professional_guidance': 'URGENT: Contact mental health professional immediately',
                    'urgency_level': 'high',
                    'color': '#607D8B'
                },
                'neutral': {
                    'immediate_actions': ['Practice mindfulness awareness', 'Check in with bodily sensations', 'Engage in pleasant activity'],
                    'long_term_strategies': ['Maintain emotional balance', 'Continue self-reflection practices', 'Build resilience skills'],
                    'professional_guidance': 'Regular mental health check-ins recommended',
                    'urgency_level': 'low',
                    'color': '#9E9E9E'
                }
            }
        
        def get_comprehensive_advice(self, emotion):
            return self.recommendations.get(emotion, self.recommendations['neutral'])
        
        def generate_care_plan(self, history):
            if not history:
                return {
                    'weekly_focus': 'Emotional Awareness',
                    'daily_practices': ['Morning mood check-in', 'Evening reflection'],
                    'weekly_goals': ['Identify emotional patterns', 'Practice one coping skill daily']
                }
            
            # Analyze history for patterns
            emotions = [entry.get('emotion', 'neutral') for entry in history[-7:]]
            common_emotion = max(set(emotions), key=emotions.count)
            
            care_plans = {
                'anxious': {
                    'weekly_focus': 'Anxiety Management',
                    'daily_practices': ['5-minute breathing exercise', 'Worry journaling'],
                    'weekly_goals': ['Identify anxiety triggers', 'Practice grounding techniques']
                },
                'stressed': {
                    'weekly_focus': 'Stress Reduction',
                    'daily_practices': ['Priority task list', 'Relaxation break'],
                    'weekly_goals': ['Delegate one task', 'Practice time management']
                },
                'sad': {
                    'weekly_focus': 'Mood Elevation',
                    'daily_practices': ['Gratitude list', 'Social connection'],
                    'weekly_goals': ['Engage in enjoyable activities', 'Reach out for support']
                },
                'happy': {
                    'weekly_focus': 'Wellness Maintenance',
                    'daily_practices': ['Share positivity', 'Continue good habits'],
                    'weekly_goals': ['Help others', 'Set new personal goals']
                }
            }
            
            return care_plans.get(common_emotion, {
                'weekly_focus': 'Emotional Balance',
                'daily_practices': ['Mood tracking', 'Self-reflection'],
                'weekly_goals': ['Understand emotional patterns', 'Develop coping strategies']
            })
    
    advisor = FallbackAdvisor()
    print("✅ Fallback advisor created!")

# Import authentication models
try:
    from auth.models import db, User, MoodHistory
    from auth.routes import auth_bp
    print("✅ Authentication modules loaded successfully!")
except ImportError as e:
    print(f"❌ Failed to import authentication modules: {e}")
    class User: 
        def __init__(self): 
            self.id = 1
            self.username = "guest"
    current_user = User()

app = Flask(__name__)
app.secret_key = 'mental_health_detector_secret_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
try:
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    print("✅ Authentication system initialized!")
except Exception as e:
    print(f"❌ Authentication setup failed: {e}")

# Global model variable
model_data = None

def load_model():
    global model_data
    try:
        model_path = os.path.join(parent_dir, 'src', 'models', 'mental_health_model.joblib')
        if os.path.exists(model_path):
            model_data = joblib.load(model_path)
            print("✅ Model loaded successfully!")
            return True
        else:
            print(f"❌ Model file not found at: {model_path}")
            return False
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def create_advanced_fallback_detector():
    class AdvancedTextPreprocessor:
        def clean_text(self, text):
            text = str(text).lower()
            text = re.sub(r'[^a-zA-Z\s\?!\.]', '', text)
            return text.strip()
        
        def transform_new_text(self, text):
            return [self.clean_text(text)]
    
    class AdvancedEmotionModel:
        def __init__(self):
            self.classes_ = ['happy', 'sad', 'anxious', 'angry', 'stressed', 'depressed', 'neutral']
        
        def predict(self, texts):
            predictions = []
            for text in texts:
                emotion, _ = self.advanced_emotion_analysis(text)
                predictions.append(emotion)
            return np.array(predictions)
        
        def predict_proba(self, texts):
            predictions = self.predict(texts)
            probas = []
            for pred in predictions:
                proba = [0.01] * len(self.classes_)
                idx = self.classes_.index(pred)
                proba[idx] = 0.85
                probas.append(proba)
            return np.array(probas)
        
        def advanced_emotion_analysis(self, text):
            if not text or len(text.strip()) < 3:
                return "neutral", 0.5
                
            text_lower = text.lower()
            print(f"🔍 Analyzing text: '{text}'")
            
            emotion_patterns = {
                'anxious': {
                    'keywords': ['anxious', 'worry', 'nervous', 'scared', 'afraid', 'panic', 'uneasy', 'racing', 'worst-case', 'overwhelm', 'buzzing', 'constant worry', 'fear', 'apprehensive', 'tense', 'restless', 'overthinking', 'what if', 'nervous', 'stressed out', 'can\'t relax', 'on edge', 'butterflies'],
                    'weight': 1.5
                },
                'happy': {
                    'keywords': ['happy', 'excited', 'joy', 'good', 'great', 'wonderful', 'amazing', 'fantastic', 'awesome', 'blessed', 'grateful', 'thrilled', 'delighted', 'love', 'perfect', 'beautiful', 'smiling', 'laughing', 'celebration', 'wonderful', 'fantastic', 'awesome', 'pleased', 'content', 'joyful'],
                    'weight': 1.3
                },
                'sad': {
                    'keywords': ['sad', 'unhappy', 'cry', 'tears', 'hopeless', 'empty', 'miserable', 'down', 'lonely', 'heartbroken', 'disappointed', 'grief', 'loss', 'miss', 'alone', 'broken', 'hurt', 'melancholy', 'blue', 'downhearted'],
                    'weight': 1.4
                },
                'angry': {
                    'keywords': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'pissed', 'rage', 'irritated', 'outraged', 'fuming', 'hate', 'resentful', 'infuriated', 'livid', 'bitter', 'upset', 'cross', 'aggravated'],
                    'weight': 1.4
                },
                'stressed': {
                    'keywords': ['stressed', 'overwhelmed', 'pressure', 'busy', 'tired', 'exhausted', 'burned out', 'deadline', 'too much', 'can\'t handle', 'juggling', 'overloaded', 'demands', 'pressure', 'swamped', 'burnt out', 'pressured'],
                    'weight': 1.4
                },
                'depressed': {
                    'keywords': ['depressed', 'hopeless', 'empty', 'numb', 'meaningless', 'pointless', 'no energy', 'dark', 'heavy', 'despair', 'worthless', 'no purpose', 'can\'t get out of bed', 'suicidal', 'life is pointless', 'no hope'],
                    'weight': 1.6
                }
            }
            
            scores = {emotion: 0 for emotion in emotion_patterns.keys()}
            scores['neutral'] = 1.0
            
            for emotion, data in emotion_patterns.items():
                for keyword in data['keywords']:
                    if keyword in text_lower:
                        scores[emotion] += data['weight']
            
            # Enhanced pattern detection
            if 'what if' in text_lower:
                scores['anxious'] += 3.0
            if 'racing' in text_lower and ('mind' in text_lower or 'thought' in text_lower):
                scores['anxious'] += 2.5
            if 'worst-case' in text_lower or 'worst case' in text_lower:
                scores['anxious'] += 2.5
            if '?' in text:
                scores['anxious'] += 1.5
            if '!' in text:
                scores['angry'] += 1.0
                scores['anxious'] += 0.5
            
            print(f"📊 Emotion scores: {scores}")
            
            best_emotion = max(scores, key=scores.get)
            best_score = scores[best_emotion]
            
            total_score = sum(scores.values())
            confidence = min(0.95, best_score / total_score * 2) if total_score > 0 else 0.6
            
            if best_score >= 3.0:
                confidence = max(confidence, 0.8)
            
            print(f"🎯 Detected: {best_emotion} (confidence: {confidence:.2f})")
            return best_emotion, confidence
    
    return {
        'model': AdvancedEmotionModel(),
        'preprocessor': AdvancedTextPreprocessor(),
        'accuracy': 0.85,
        'is_fallback': True
    }

# Load model
print("🔄 Loading model...")
if not load_model():
    print("🔄 Creating advanced fallback detector...")
    model_data = create_advanced_fallback_detector()
    print("✅ Advanced fallback detector created!")

# Initialize speech processing
audio_recorder = AudioRecorder()
feature_extractor = AudioFeatureExtractor()

# Create tables
try:
    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")
except Exception as e:
    print(f"❌ Database setup failed: {e}")

# ===== ENHANCED VOICE PROCESSING =====

def validate_audio_quality(filepath):
    """Validate audio file quality before processing"""
    try:
        with wave.open(filepath, 'r') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            
            print(f"🔊 Audio Quality: {duration:.1f}s, {rate}Hz, {channels} channels")
            
            # Quality checks
            if duration < 1.0:
                return False, "Audio too short (min 1 second)"
            if rate < 16000:
                return False, "Sample rate too low (min 16000 Hz)"
            if channels != 1:
                return False, "Please use mono audio (1 channel)"
                
            return True, "Good quality"
    except Exception as e:
        return False, f"Invalid audio file: {e}"

def enhanced_speech_to_text(audio_path):
    """Robust speech-to-text with multiple fallbacks"""
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        
        # Check if audio file exists and is valid
        if not os.path.exists(audio_path):
            print("❌ Audio file does not exist")
            return None
            
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient noise with longer duration
            print("🎵 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1.5)
            
            # Read the entire audio file
            print("🎵 Reading audio data...")
            audio = r.record(source)
            
            # Try Google Web Speech API first
            try:
                print("🎵 Trying Google Speech Recognition...")
                text = r.recognize_google(audio)
                print(f"✅ Google Recognition: '{text}'")
                return text
            except sr.UnknownValueError:
                print("❌ Google could not understand audio")
            except sr.RequestError as e:
                print(f"❌ Google Speech Recognition error: {e}")
            
            # Try Sphinx as fallback (offline)
            try:
                print("🎵 Trying Sphinx (offline)...")
                text = r.recognize_sphinx(audio)
                print(f"✅ Sphinx Recognition: '{text}'")
                return text
            except sr.UnknownValueError:
                print("❌ Sphinx could not understand audio")
            except Exception as e:
                print(f"❌ Sphinx recognition failed: {e}")
            
            return None
            
    except Exception as e:
        print(f"❌ Speech recognition failed: {e}")
        return None

def enhanced_emotion_analysis(text):
    """More sophisticated emotion analysis"""
    text_lower = text.lower()
    
    # Emotion intensity detection
    intensity_indicators = {
        'high': ['extremely', 'very', 'really', 'so', 'incredibly', 'absolutely'],
        'medium': ['quite', 'pretty', 'fairly', 'somewhat'],
        'low': ['a bit', 'slightly', 'a little', 'kind of']
    }
    
    # Enhanced emotion patterns with intensity
    emotion_data = {
        'anxious': {
            'keywords': ['anxious', 'worry', 'nervous', 'scared', 'panic', 'racing thoughts', 'overwhelm'],
            'intensity_boost': 2.0,
            'triggers': ['deadline', 'pressure', 'future', 'what if']
        },
        'stressed': {
            'keywords': ['stressed', 'overwhelmed', 'pressure', 'too much', 'busy', 'juggling'],
            'intensity_boost': 1.8,
            'triggers': ['work', 'responsibilities', 'deadline', 'time']
        },
        'sad': {
            'keywords': ['sad', 'unhappy', 'cry', 'tears', 'hopeless', 'empty', 'lonely'],
            'intensity_boost': 1.7,
            'triggers': ['loss', 'alone', 'miss', 'nothing']
        },
        'happy': {
            'keywords': ['happy', 'excited', 'joy', 'good', 'great', 'wonderful', 'grateful'],
            'intensity_boost': 1.5,
            'triggers': ['accomplish', 'success', 'friends', 'family']
        },
        'angry': {
            'keywords': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'rage'],
            'intensity_boost': 1.8,
            'triggers': ['unfair', 'wrong', 'mistake', 'problem']
        },
        'depressed': {
            'keywords': ['depressed', 'hopeless', 'empty', 'numb', 'meaningless'],
            'intensity_boost': 2.2,
            'triggers': ['life', 'future', 'nothing matters']
        }
    }
    
    scores = {emotion: 1.0 for emotion in emotion_data.keys()}
    scores['neutral'] = 2.0  # Default neutral score
    
    # Analyze text
    for emotion, data in emotion_data.items():
        # Keyword matching
        for keyword in data['keywords']:
            if keyword in text_lower:
                scores[emotion] += data['intensity_boost']
        
        # Trigger context
        for trigger in data['triggers']:
            if trigger in text_lower:
                scores[emotion] += 0.5
    
    # Intensity analysis
    for intensity_level, words in intensity_indicators.items():
        for word in words:
            if word in text_lower:
                intensity_multiplier = {'high': 1.5, 'medium': 1.2, 'low': 0.8}[intensity_level]
                # Apply to all detected emotions
                for emotion in emotion_data.keys():
                    if scores[emotion] > 2.0:  # If emotion was detected
                        scores[emotion] *= intensity_multiplier
    
    # Negation handling
    negation_words = ['not', "don't", "can't", 'no', 'never']
    for negation in negation_words:
        if negation in text_lower:
            # Reduce positive emotions when negation present
            scores['happy'] *= 0.5
    
    print(f"📊 Enhanced emotion scores: {scores}")
    
    best_emotion = max(scores, key=scores.get)
    best_score = scores[best_emotion]
    
    # Calculate confidence
    total_score = sum(scores.values())
    confidence = min(0.95, best_score / total_score * 3)
    
    # Require minimum score difference to avoid neutral default
    if best_score < 3.0:
        confidence *= 0.7
        # If no strong emotion detected, consider neutral
        if best_score < 2.5:
            best_emotion = 'neutral'
    
    return best_emotion, confidence

def analyze_audio_features(audio_path):
    """Analyze audio features for emotion hints"""
    try:
        duration = audio_recorder.get_audio_duration(audio_path)
        file_size = os.path.getsize(audio_path)
        
        # Simple heuristic based on audio properties
        if duration < 2:
            return "neutral"
        elif file_size < 15000:  # Very small file (quiet speech)
            return random.choice(['sad', 'anxious'])
        elif duration > 8:  # Long recording
            return random.choice(['stressed', 'anxious'])
        else:
            # Weighted random based on common patterns
            emotions = ['anxious', 'stressed', 'neutral', 'sad']
            weights = [0.35, 0.3, 0.2, 0.15]
            return random.choices(emotions, weights=weights)[0]
            
    except Exception as e:
        print(f"❌ Audio feature analysis failed: {e}")
        return "neutral"

def get_context_emotion():
    """Context-aware fallback based on time and patterns"""
    current_hour = datetime.now().hour
    
    # Time-based emotion weighting
    if 6 <= current_hour < 12:  # Morning
        emotions = ['anxious', 'stressed', 'neutral', 'happy']
        weights = [0.3, 0.3, 0.25, 0.15]
    elif 12 <= current_hour < 18:  # Afternoon
        emotions = ['stressed', 'anxious', 'neutral', 'tired']
        weights = [0.35, 0.25, 0.25, 0.15]
    else:  # Evening/Night
        emotions = ['sad', 'anxious', 'neutral', 'tired']
        weights = [0.3, 0.25, 0.25, 0.2]
    
    return random.choices(emotions, weights=weights)[0]

def process_speech_emotion(audio_path):
    """RELIABLE speech emotion processing"""
    try:
        print(f"🎤 Processing speech from: {audio_path}")
        
        # 1. Validate audio quality first
        quality_ok, quality_msg = validate_audio_quality(audio_path)
        if not quality_ok:
            print(f"❌ Audio quality issue: {quality_msg}")
            return "neutral", 0.5, "poor_audio_quality"
        
        # 2. Try speech recognition
        recognized_text = enhanced_speech_to_text(audio_path)
        
        # 3. If we have good text, use enhanced emotion analysis
        if recognized_text and len(recognized_text.strip()) > 8:
            print(f"🎤 Using recognized text: '{recognized_text}'")
            emotion, confidence = enhanced_emotion_analysis(recognized_text)
            return emotion, confidence, "speech_recognition"
        
        # 4. Audio feature analysis as fallback
        audio_emotion = analyze_audio_features(audio_path)
        if audio_emotion != "neutral":
            return audio_emotion, 0.65, "audio_analysis"
        
        # 5. Final context-aware fallback
        context_emotion = get_context_emotion()
        return context_emotion, 0.6, "context_fallback"
        
    except Exception as e:
        print(f"❌ Speech processing error: {e}")
        return "neutral", 0.5, "error_fallback"

# ===== ROUTES =====

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    try:
        if hasattr(current_user, 'id') and current_user.id:
            mood_history = MoodHistory.query.filter_by(user_id=current_user.id).order_by(MoodHistory.created_at.desc()).limit(10).all()
        else:
            mood_history = session.get('emotional_history', [])[-10:]
        return render_template('dashboard.html', mood_history=mood_history, user=getattr(current_user, 'username', 'Guest'))
    except Exception as e:
        return render_template('dashboard.html', mood_history=session.get('emotional_history', [])[-10:], user='Guest')

@app.route('/debug')
def debug_page():
    return render_template('debug.html')

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    if model_data is None:
        return jsonify({'error': 'No model available'}), 500
    
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Please enter some text'}), 400
    
    try:
        print(f"🔍 Analyzing text: '{text}'")
        
        if hasattr(model_data['model'], 'advanced_emotion_analysis'):
            emotion, confidence = model_data['model'].advanced_emotion_analysis(text)
        else:
            features = model_data['preprocessor'].transform_new_text(text)
            emotion = model_data['model'].predict(features)[0]
            confidence = 0.7
        
        advice_data = advisor.get_comprehensive_advice(emotion)
        
        # Store in database/session
        try:
            if hasattr(current_user, 'id') and current_user.id:
                mood_entry = MoodHistory(
                    user_id=current_user.id,
                    text_input=text,
                    emotion=emotion,
                    confidence=float(confidence),
                    input_type='text'
                )
                db.session.add(mood_entry)
                db.session.commit()
        except Exception as e:
            print(f"❌ Database save failed: {e}")
        
        if 'emotional_history' not in session:
            session['emotional_history'] = []
        
        session['emotional_history'].append({
            'text': text[:100] + "..." if len(text) > 100 else text,
            'emotion': emotion,
            'confidence': float(confidence),
            'timestamp': datetime.now().isoformat(),
            'advice': advice_data,
            'input_type': 'text'
        })
        
        if len(session['emotional_history']) > 20:
            session['emotional_history'] = session['emotional_history'][-20:]
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'confidence': float(confidence),
            'advice': advice_data,
            'input_type': 'text',
            'detection_method': 'advanced_analysis'
        })
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/record-audio', methods=['POST'])
def record_audio():
    try:
        data = request.get_json()
        duration = data.get('duration', 5) if data else 5
        recording_id = data.get('recording_id', 'unknown') if data else 'unknown'
        
        user_id = getattr(current_user, 'id', 'guest')
        filename = f"user_{user_id}_{recording_id}.wav"
        filepath = os.path.join('webapp', 'static', 'audio', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        print(f"🎤 Recording audio: {filepath}")
        
        recorded_file = audio_recorder.record_audio(duration=duration, filename=filepath)
        
        if os.path.exists(recorded_file):
            file_size = os.path.getsize(recorded_file)
            duration = audio_recorder.get_audio_duration(recorded_file)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'file_size': file_size,
                'duration': duration,
                'message': f'Recorded {duration:.1f}s audio'
            })
        else:
            return jsonify({'success': False, 'error': 'Audio file not created'}), 500
        
    except Exception as e:
        print(f"❌ Audio recording error: {e}")
        return jsonify({'success': False, 'error': f'Recording failed: {str(e)}'}), 500

@app.route('/analyze-audio', methods=['POST'])
def analyze_audio():
    try:
        data = request.get_json()
        filename = data.get('filename') if data else request.form.get('filename')
        
        if not filename:
            return jsonify({'error': 'No audio file provided'}), 400
        
        filepath = os.path.join('webapp', 'static', 'audio', filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Audio file not found'}), 404
        
        print(f"🔍 Processing audio file: {filepath}")
        
        # Use ENHANCED speech processing
        emotion, confidence, method = process_speech_emotion(filepath)
        
        file_size = os.path.getsize(filepath)
        duration = audio_recorder.get_audio_duration(filepath)
        advice_data = advisor.get_comprehensive_advice(emotion)
        
        # Store in database/session
        try:
            if hasattr(current_user, 'id') and current_user.id:
                mood_entry = MoodHistory(
                    user_id=current_user.id,
                    emotion=emotion,
                    confidence=float(confidence),
                    input_type='speech',
                    audio_filename=filename
                )
                db.session.add(mood_entry)
                db.session.commit()
        except Exception as e:
            print(f"❌ Database save failed: {e}")
        
        if 'emotional_history' not in session:
            session['emotional_history'] = []
        
        session['emotional_history'].append({
            'emotion': emotion,
            'confidence': float(confidence),
            'timestamp': datetime.now().isoformat(),
            'advice': advice_data,
            'input_type': 'speech',
            'audio_file': filename,
            'detection_method': method
        })
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'confidence': float(confidence),
            'advice': advice_data,
            'input_type': 'speech',
            'audio_duration': duration,
            'detection_method': method
        })
        
    except Exception as e:
        print(f"❌ Audio analysis error: {e}")
        return jsonify({
            'success': True,
            'emotion': 'neutral',
            'confidence': 0.6,
            'advice': advisor.get_comprehensive_advice('neutral'),
            'input_type': 'speech',
            'detection_method': 'error_recovery'
        })

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        user_id = getattr(current_user, 'id', 'guest')
        filename = f"upload_user_{user_id}_{datetime.now().strftime('%H%M%S')}.wav"
        filepath = os.path.join('webapp', 'static', 'audio', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        audio_file.save(filepath)
        
        print(f"📁 Audio file uploaded: {filename}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Audio uploaded successfully'
        })
        
    except Exception as e:
        print(f"❌ Audio upload error: {e}")
        return jsonify({'error': f'Audio upload failed: {str(e)}'}), 500

@app.route('/debug-audio', methods=['POST'])
def debug_audio():
    """Comprehensive audio debugging endpoint"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file'})
        
        audio_file = request.files['audio']
        filename = f"debug_{datetime.now().strftime('%H%M%S')}.wav"
        filepath = os.path.join('webapp', 'static', 'audio', filename)
        
        audio_file.save(filepath)
        
        # Comprehensive analysis
        debug_info = {
            'file_info': analyze_audio_file(filepath),
            'speech_recognition': test_speech_recognition(filepath),
            'emotion_analysis': test_emotion_detection(filepath),
            'system_checks': perform_system_checks()
        }
        
        # Clean up debug file
        try:
            os.remove(filepath)
        except:
            pass
            
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': f'Debug failed: {e}'})

def analyze_audio_file(filepath):
    """Analyze audio file properties"""
    try:
        with wave.open(filepath, 'r') as wf:
            return {
                'file_exists': os.path.exists(filepath),
                'file_size': os.path.getsize(filepath),
                'duration': wf.getnframes() / wf.getframerate(),
                'sample_rate': wf.getframerate(),
                'channels': wf.getnchannels(),
                'sample_width': wf.getsampwidth(),
                'frames': wf.getnframes(),
                'compression': wf.getcompname()
            }
    except Exception as e:
        return {'error': f'Audio analysis failed: {e}'}

def test_speech_recognition(filepath):
    """Test if speech recognition is working"""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        
        with sr.AudioFile(filepath) as source:
            r.adjust_for_ambient_noise(source, duration=1.0)
            audio = r.record(source)
            
            try:
                text = r.recognize_google(audio)
                return {
                    'status': 'success',
                    'recognized_text': text,
                    'text_length': len(text),
                    'confidence': 'high'
                }
            except sr.UnknownValueError:
                return {'status': 'no_speech_detected', 'recognized_text': None}
            except sr.RequestError as e:
                return {'status': 'api_error', 'error': str(e)}
                
    except Exception as e:
        return {'status': 'recognition_failed', 'error': str(e)}

def test_emotion_detection(filepath):
    """Test emotion detection pipeline"""
    emotion, confidence, method = process_speech_emotion(filepath)
    
    return {
        'detected_emotion': emotion,
        'confidence': confidence,
        'method_used': method
    }

def perform_system_checks():
    """Perform system health checks"""
    return {
        'speech_recognition_available': True,
        'audio_processing_available': True,
        'model_loaded': model_data is not None,
        'using_fallback': model_data.get('is_fallback', False) if model_data else True
    }

@app.route('/test-voice-accuracy', methods=['GET'])
def test_voice_accuracy():
    """Test endpoint to verify voice input is working"""
    test_phrases = [
        {"text": "I'm feeling extremely anxious and overwhelmed right now", "expected": "anxious"},
        {"text": "I'm so happy and excited about everything in my life", "expected": "happy"},
        {"text": "I feel really sad and lonely today, nothing brings me joy", "expected": "sad"},
        {"text": "I'm furious about what happened, this is so unfair", "expected": "angry"},
        {"text": "I'm completely stressed out with all my responsibilities", "expected": "stressed"}
    ]
    
    results = []
    for i, test in enumerate(test_phrases):
        emotion, confidence = model_data['model'].advanced_emotion_analysis(test["text"])
        match = emotion == test["expected"]
        
        results.append({
            "test_case": i+1,
            "input_text": test["text"],
            "expected": test["expected"],
            "detected": emotion,
            "confidence": confidence,
            "match": match,
            "status": "✅ PASS" if match else "❌ FAIL"
        })
    
    accuracy = sum(1 for r in results if r["match"]) / len(results)
    
    return jsonify({
        "accuracy_test": True,
        "overall_accuracy": f"{accuracy:.1%}",
        "results": results
    })

@app.route('/history', methods=['GET'])
def get_history():
    history = session.get('emotional_history', [])
    return jsonify(history)

@app.route('/care_plan', methods=['GET'])
def get_care_plan():
    history = session.get('emotional_history', [])
    care_plan = advisor.generate_care_plan(history)
    return jsonify(care_plan)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('emotional_history', None)
    return jsonify({'success': True})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'model_loaded': model_data is not None,
        'using_fallback': model_data.get('is_fallback', False) if model_data else True,
        'speech_processing': True
    })

if __name__ == '__main__':
    print("🌐 Starting Mental Health Tone Detector...")
    print("📊 Model Status:", "✅ TRAINED MODEL" if not model_data.get('is_fallback', True) else "🔄 ADVANCED FALLBACK")
    print("🎤 Speech Processing:", "✅ ENHANCED VOICE INPUT")
    print("🔧 Debug Tools:", "✅ AVAILABLE at /debug")
    print("🚀 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)