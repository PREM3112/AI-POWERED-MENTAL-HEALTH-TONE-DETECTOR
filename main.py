import os
import sys
import webbrowser
import threading
import time
from enhanced_dataset_creation import EnhancedMentalHealthDataset
from enhanced_train_model import main as train_main

def main():
    print("🧠 AI Mental Health Tone Detector - Enhanced Version")
    print("=" * 60)
    
    while True:
        print("\n📋 Main Menu:")
        print("1. 🗃️  Create Enhanced Dataset")
        print("2. 🤖 Train Enhanced Model")
        print("3. 🌐 Start Web Application")
        print("4. 🚀 Run Complete System")
        print("5. ❌ Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            create_dataset()
        elif choice == '2':
            train_model()
        elif choice == '3':
            start_webapp()
        elif choice == '4':
            run_complete_system()
        elif choice == '5':
            print("👋 Thank you for using AI Mental Health Tone Detector!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def create_dataset():
    """Create enhanced dataset"""
    print("\n🗃️ Creating Enhanced Dataset...")
    try:
        generator = EnhancedMentalHealthDataset()
        dataset = generator.save_dataset()
        print("✅ Dataset created successfully!")
    except Exception as e:
        print(f"❌ Error creating dataset: {e}")

def train_model():
    """Train the enhanced model"""
    print("\n🤖 Training Enhanced Model...")
    try:
        accuracy = train_main()
        if accuracy > 0.90:
            print("🎉 Model trained successfully with >90% accuracy!")
        else:
            print("⚠️ Model trained but accuracy needs improvement.")
    except Exception as e:
        print(f"❌ Error training model: {e}")

def start_webapp():
    """Start the web application"""
    print("\n🌐 Starting Web Application...")
    print("The application will open in your browser shortly...")
    
    def open_browser():
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
    
    # Open browser in separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask app
    try:
        os.chdir('webapp')
        from enhanced_app import app
        app.run(debug=True, port=5000, use_reloader=False)
    except Exception as e:
        print(f"❌ Error starting web app: {e}")

def run_complete_system():
    """Run the complete system"""
    print("\n🚀 Running Complete System...")
    try:
        create_dataset()
        train_model()
        start_webapp()
    except Exception as e:
        print(f"❌ Error running complete system: {e}")

if __name__ == "__main__":
    main()