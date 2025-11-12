import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

class TextPreprocessor:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            self.nltk_available = True
        except:
            self.stop_words = set()
            self.lemmatizer = None
            self.nltk_available = False
        
        self.vectorizer = None
        
    def clean_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_and_lemmatize(self, text):
        """Tokenize and lemmatize text"""
        if not self.nltk_available:
            return ' '.join(text.split())
        
        try:
            tokens = word_tokenize(text)
            
            # Remove stopwords and lemmatize
            tokens = [self.lemmatizer.lemmatize(token) 
                     for token in tokens 
                     if token not in self.stop_words and len(token) > 2]
            
            return ' '.join(tokens)
        except:
            return ' '.join(text.split())
    
    def preprocess_dataset(self, df, text_column='text'):
        """Preprocess entire dataset"""
        print("Cleaning text...")
        df['cleaned_text'] = df[text_column].apply(self.clean_text)
        
        print("Tokenizing and lemmatizing...")
        df['processed_text'] = df['cleaned_text'].apply(self.tokenize_and_lemmatize)
        
        # Remove empty texts after preprocessing
        df = df[df['processed_text'].str.len() > 0]
        
        return df
    
    def create_features(self, texts, method='tfidf', max_features=5000):
        """Create feature vectors from text"""
        if method == 'tfidf':
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=(1, 3),
                stop_words='english',
                min_df=2,
                max_df=0.8
            )
        
        features = self.vectorizer.fit_transform(texts)
        return features
    
    def transform_new_text(self, text):
        """Transform new text using fitted vectorizer"""
        if self.vectorizer is None:
            raise ValueError("Vectorizer not fitted. Call create_features first.")
        
        cleaned = self.clean_text(text)
        processed = self.tokenize_and_lemmatize(cleaned)
        return self.vectorizer.transform([processed])