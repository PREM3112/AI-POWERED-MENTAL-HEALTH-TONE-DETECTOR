import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from webapp.enhanced_app import create_app
from utils.mentalbert_handler import mentalbert_analyzer

def main():
    print("🚀 Starting Mental Health Detection System...")
    print("📊 Loading MentalBERT model...")
    
    # Initialize MentalBERT
    if mentalbert_analyzer.is_loaded:
        print("✅ MentalBERT loaded successfully!")
    else:
        print("❌ MentalBERT failed to load, using fallback")
    
    # Start Flask app
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()