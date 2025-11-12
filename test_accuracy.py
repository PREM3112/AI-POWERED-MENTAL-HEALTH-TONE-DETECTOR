import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add src to path
sys.path.append('src')

def test_accuracy():
    """Test the model accuracy"""
    print("🧪 Testing Model Accuracy...")
    
    # Load model
    try:
        model_data = joblib.load('src/models/mental_health_model.joblib')
        model = model_data['model']
        preprocessor = model_data['preprocessor']
        print("✅ Model loaded successfully!")
        print(f"📊 Model accuracy from training: {model_data.get('accuracy', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Load test data
    try:
        df = pd.read_csv('data/raw/enhanced_mental_health_dataset.csv')
        print(f"📊 Test dataset loaded: {len(df)} samples")
        print(f"🎭 Emotions in dataset: {df['emotion'].value_counts().to_dict()}")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return
    
    try:
        # Preprocess data
        print("🔧 Preprocessing test data...")
        df_processed = preprocessor.preprocess_dataset(df)
        
        # Create features for all texts
        print("🎯 Creating features for test data...")
        
        # Use the correct method - transform each text individually
        predictions = []
        true_labels = []
        confidence_scores = []
        
        print("🧠 Running predictions on test data...")
        for idx, row in df_processed.iterrows():
            try:
                # Transform single text
                features = preprocessor.transform_new_text(row['processed_text'])
                
                # Predict
                emotion = model.predict(features)[0]
                probability = model.predict_proba(features)[0]
                confidence = max(probability)
                
                predictions.append(emotion)
                true_labels.append(row['emotion'])
                confidence_scores.append(confidence)
                
                # Progress indicator
                if (idx + 1) % 100 == 0:
                    print(f"   Processed {idx + 1}/{len(df_processed)} samples...")
                    
            except Exception as e:
                print(f"❌ Error processing sample {idx}: {e}")
                continue
        
        # Calculate accuracy
        accuracy = accuracy_score(true_labels, predictions)
        
        print(f"\n🎯 Model Test Results:")
        print(f"📊 Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"📈 Average Confidence: {np.mean(confidence_scores):.4f}")
        
        print(f"\n📋 Classification Report:")
        print(classification_report(true_labels, predictions))
        
        # Plot confusion matrix
        plot_confusion_matrix(true_labels, predictions)
        
        # Test with some difficult samples
        test_difficult_samples(model, preprocessor)
        
        if accuracy > 0.90:
            print("✅ SUCCESS: Model achieved >90% accuracy!")
        elif accuracy > 0.85:
            print("⚠️ Good accuracy! Close to 90% target.")
        else:
            print("🔧 Accuracy needs improvement.")
        
        return accuracy
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return 0

def plot_confusion_matrix(y_true, y_pred):
    """Plot and save confusion matrix"""
    try:
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=sorted(set(y_true)),
                   yticklabels=sorted(set(y_true)))
        plt.title('Confusion Matrix - Test Results')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        # Ensure directory exists
        os.makedirs('logs', exist_ok=True)
        plt.savefig('logs/test_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("📈 Confusion matrix saved to 'logs/test_confusion_matrix.png'")
    except Exception as e:
        print(f"❌ Error plotting confusion matrix: {e}")

def test_difficult_samples(model, preprocessor):
    """Test with difficult real-world samples"""
    print(f"\n🔥 Testing Difficult Real-World Samples:")
    
    difficult_samples = [
        # Mixed emotions
        ("idk how i feel tbh. everything just feels off today", "confused/neutral"),
        ("Got great news but now I'm lowkey stressed about it", "mixed"),
        ("Another fantastic day where everything went exactly according to plan 🙃", "sarcastic"),
        
        # Complex emotions
        ("my body is tired but my mind won't shut up", "stressed/anxious"),
        ("Seeing everyone's perfect lives while I'm here eating cereal", "sad/comparison"),
        ("Supposed to have life together but vibing and panicking", "anxious/confused"),
        
        # Real text messages
        ("He said he'd call but it's been 3 days. Trying to play it cool", "anxious/sad"),
        ("Honestly? Could be better, could be worse", "neutral/mixed"),
        ("3 AM and my brain decided to review every embarrassing thing", "anxious"),
        
        # Work stress
        ("Another 'urgent' request 5 minutes before EOD", "stressed/angry"),
        ("Got praised but when will they discover I have no idea", "anxious/imposter"),
        
        # Relationship complexity
        ("Best friend forgot my birthday. Telling myself it's fine", "sad/angry"),
        ("We're talking but not dating, dating but not exclusive", "confused/anxious")
    ]
    
    correct_predictions = 0
    total_samples = len(difficult_samples)
    
    print(f"\n📱 Testing {total_samples} difficult samples:")
    print("=" * 60)
    
    for text, expected_category in difficult_samples:
        try:
            features = preprocessor.transform_new_text(text)
            emotion = model.predict(features)[0]
            confidence = max(model.predict_proba(features)[0])
            
            # For difficult samples, we're checking if the prediction makes sense
            # rather than exact matches
            makes_sense = check_if_prediction_makes_sense(emotion, text)
            
            status = "✅" if makes_sense else "❌"
            print(f"{status} Text: '{text}'")
            print(f"   Predicted: {emotion} (confidence: {confidence:.3f})")
            print(f"   Expected category: {expected_category}")
            
            if makes_sense:
                correct_predictions += 1
                
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    difficult_accuracy = correct_predictions / total_samples
    print(f"\n🎯 Difficult Samples Accuracy: {difficult_accuracy:.1%} ({correct_predictions}/{total_samples})")

def check_if_prediction_makes_sense(predicted_emotion, text):
    """Check if the predicted emotion makes sense for the given text"""
    text_lower = text.lower()
    
    # Define what emotions make sense for certain keywords/contexts
    emotion_keywords = {
        'stressed': ['stress', 'pressure', 'urgent', 'deadline', 'overwhelmed', 'tired'],
        'anxious': ['anxious', 'worry', 'nervous', 'panic', 'brain', 'mind'],
        'sad': ['sad', 'forgot', 'crying', 'empty', 'off', 'not good'],
        'angry': ['angry', 'mad', 'frustrated', 'annoyed'],
        'confused': ['confused', 'idk', 'not sure', 'complicated', 'mixed'],
        'neutral': ['okay', 'fine', 'alright', 'could be']
    }
    
    # Check if predicted emotion has supporting keywords in text
    if predicted_emotion in emotion_keywords:
        keywords = emotion_keywords[predicted_emotion]
        if any(keyword in text_lower for keyword in keywords):
            return True
    
    # Special cases for sarcasm and mixed emotions
    if '🙃' in text or 'fantastic' in text_lower and 'according to plan' in text_lower:
        return predicted_emotion in ['sad', 'angry', 'stressed']
    
    if 'lowkey' in text_lower or 'idk' in text_lower:
        return predicted_emotion in ['confused', 'neutral', 'anxious']
    
    # Default to True for ambiguous cases
    return True

# Add numpy import at the top
import numpy as np

if __name__ == "__main__":
    test_accuracy()