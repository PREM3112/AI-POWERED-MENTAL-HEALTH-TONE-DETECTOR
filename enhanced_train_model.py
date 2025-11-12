import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import sys

# Add src to path
sys.path.append('src')
from preprocessing.text_preprocessor import TextPreprocessor

class EnhancedToneDetector:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.accuracy = 0
        
    def load_data(self):
        """Load and preprocess the dataset"""
        print("📊 Loading dataset...")
        try:
            df = pd.read_csv('data/raw/enhanced_mental_health_dataset.csv')
            print(f"Dataset loaded: {len(df)} samples")
            return df
        except FileNotFoundError:
            print("❌ Dataset not found. Please run enhanced_dataset_creation.py first.")
            return None
    
    def train(self):
        """Train the enhanced model"""
        df = self.load_data()
        if df is None:
            return 0
        
        # Preprocess data
        print("🔧 Preprocessing data...")
        df_processed = self.preprocessor.preprocess_dataset(df)
        
        # Create features
        print("🎯 Creating features...")
        X = self.preprocessor.create_features(df_processed['processed_text'])
        y = df_processed['emotion']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        print("🤖 Training model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate
        print("📊 Evaluating model...")
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        
        print(f"🎯 Model Accuracy: {self.accuracy:.4f}")
        print("\n📈 Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Plot confusion matrix
        self.plot_confusion_matrix(y_test, y_pred)
        
        # Save model
        self.save_model()
        
        return self.accuracy
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """Plot and save confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=sorted(set(y_true)),
                   yticklabels=sorted(set(y_true)))
        plt.title('Confusion Matrix - Mental Health Tone Detection')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        # Ensure directory exists
        os.makedirs('logs', exist_ok=True)
        plt.savefig('logs/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_model(self):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'preprocessor': self.preprocessor,
            'accuracy': self.accuracy
        }
        
        # Ensure directory exists
        os.makedirs('src/models', exist_ok=True)
        
        joblib.dump(model_data, 'src/models/mental_health_model.joblib')
        print("💾 Model saved to 'src/models/mental_health_model.joblib'")
    
    def load_model(self):
        """Load a trained model"""
        try:
            model_data = joblib.load('src/models/mental_health_model.joblib')
            self.model = model_data['model']
            self.preprocessor = model_data['preprocessor']
            self.accuracy = model_data['accuracy']
            print("✅ Model loaded successfully!")
            return True
        except FileNotFoundError:
            print("❌ No trained model found. Please train a model first.")
            return False

def main():
    print("🚀 Starting Enhanced Mental Health Tone Detector Training...")
    
    detector = EnhancedToneDetector()
    
    # Train or load model
    if not detector.load_model():
        print("Training new model...")
        accuracy = detector.train()
    else:
        accuracy = detector.accuracy
    
    print(f"\n🎉 Training completed!")
    print(f"📊 Final Accuracy: {accuracy:.4f}")
    
    if accuracy > 0.90:
        print("✅ SUCCESS: Model achieved >90% accuracy!")
    elif accuracy > 0.85:
        print("⚠️ Good accuracy! Close to 90% target.")
    else:
        print("🔧 Accuracy needs improvement. Consider:")
        print("   - Adding more training data")
        print("   - Trying different model parameters")
        print("   - Improving text preprocessing")
    
    return accuracy

if __name__ == "__main__":
    main()