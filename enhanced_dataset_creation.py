import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

class EnhancedMentalHealthDataset:
    def __init__(self):
        self.emotions = {
            'happy': {'mental_state': 'positive_mood'},
            'sad': {'mental_state': 'depressive_mood'},
            'anxious': {'mental_state': 'anxiety_disorder'},
            'angry': {'mental_state': 'anger_issues'},
            'stressed': {'mental_state': 'stress_disorder'},
            'depressed': {'mental_state': 'clinical_depression'},
            'neutral': {'mental_state': 'stable_mood'},
            'lonely': {'mental_state': 'social_isolation'},
            'confused': {'mental_state': 'cognitive_dissonance'},
            'guilty': {'mental_state': 'guilt_complex'},
            'proud': {'mental_state': 'healthy_self_esteem'},
            'grateful': {'mental_state': 'positive_mindset'}
        }
    
    def create_text_samples(self):
        emotion_texts = {}
        
        # Happy texts
        emotion_texts['happy'] = [
            "I feel wonderful today everything is going great",
            "Life is amazing and full of joy and happiness",
            "I am so happy and content with my life right now",
            "Everything is going perfectly well for me today",
            "This is the best day ever I feel absolutely amazing",
            "My heart is full of joy and positive energy today",
            "I feel blessed and grateful for everything in life",
            "Today has been absolutely wonderful and happy day",
            "I am overflowing with happiness and good feelings",
            "The world seems bright and beautiful today"
        ]
        
        # Sad texts
        emotion_texts['sad'] = [
            "I feel terrible and sad about everything happening",
            "Everything is going wrong in my life right now",
            "I am so unhappy and depressed today cannot smile",
            "This is the worst day I have ever had in my life",
            "Nothing makes me happy or brings me joy anymore",
            "I feel empty and hollow inside my heart today",
            "Tears keep coming and I cannot stop feeling sad",
            "The sadness is overwhelming and constant pain",
            "I feel like I lost all hope and happiness forever",
            "My heart aches with sadness that wont go away"
        ]
        
        # Anxious texts
        emotion_texts['anxious'] = [
            "I feel anxious and worried all the time constantly",
            "My mind wont stop racing with bad thoughts today",
            "I am constantly worried about everything in life",
            "The anxiety is making it hard to breathe properly",
            "I feel like something bad will happen very soon",
            "My heart is pounding with fear and worry nonstop",
            "I cannot stop thinking about worst case scenarios",
            "The uncertainty is making me very anxious today",
            "I feel nervous and on edge about everything now",
            "My anxiety is through the roof and overwhelming"
        ]
        
        # Angry texts
        emotion_texts['angry'] = [
            "I am so angry and furious right now at everything",
            "This situation makes me absolutely furious today",
            "I cannot believe how angry this makes me feel now",
            "I am really mad and upset about everything happening",
            "This injustice makes my blood boil inside my veins",
            "I feel betrayed and angry with everyone around me",
            "My patience has completely run out now I am done",
            "I am so frustrated and angry all day long today",
            "This makes me want to scream I am so angry now",
            "I cannot control my anger about this situation"
        ]
        
        # Stressed texts
        emotion_texts['stressed'] = [
            "I am so stressed and overwhelmed today completely",
            "There is too much pressure on me right now today",
            "I cannot handle all this stress anymore its too much",
            "Everything feels overwhelming and too much to handle",
            "The stress is affecting my sleep and health badly",
            "I feel completely stressed out and exhausted today",
            "There are too many demands and not enough time now",
            "I am stretched too thin in every direction possible",
            "The stress is making me sick and tired constantly",
            "I cannot cope with all this stress and pressure"
        ]
        
        # Depressed texts
        emotion_texts['depressed'] = [
            "I feel completely depressed and hopeless today",
            "There is no point in anything anymore in life",
            "I have lost interest in everything I loved before",
            "Getting out of bed feels impossible today too hard",
            "The depression is crushing and overwhelming me",
            "I feel like a burden to everyone around me now",
            "There is no hope or light in my life anymore",
            "I cannot see any reason to keep going forward",
            "The darkness is consuming me completely today",
            "I feel numb and dead inside from depression"
        ]
        
        # Neutral texts
        emotion_texts['neutral'] = [
            "I feel okay and neutral today nothing special",
            "Everything is normal and average as usual today",
            "Just a regular day nothing special happening now",
            "I am feeling neither good nor bad just neutral",
            "Today is pretty normal and uneventful as expected",
            "My mood is stable and balanced right now normal",
            "Nothing particularly exciting happening today",
            "Feeling calm and composed as usual today normal",
            "Today is neither good nor bad just average day",
            "I feel fine nothing special to report today"
        ]
        
        # Lonely texts
        emotion_texts['lonely'] = [
            "I feel completely alone and isolated from everyone",
            "No one understands how I truly feel inside me",
            "I am surrounded but feel completely alone today",
            "My heart aches for real connection with someone",
            "There is nobody I can really talk to about feelings",
            "I feel invisible and unimportant to other people",
            "The loneliness is painful and constant in my life",
            "I long for meaningful relationships with people",
            "I feel disconnected from everyone in the world",
            "The silence and loneliness are deafening today"
        ]
        
        # Confused texts
        emotion_texts['confused'] = [
            "I feel confused and unsure about everything now",
            "My thoughts are all mixed up and unclear today",
            "I dont know what to do or think anymore now",
            "Everything feels uncertain and confusing to me",
            "I am questioning all my life decisions today",
            "My mind is a maze with no way out right now",
            "I cannot make sense of anything right now today",
            "Everything seems complicated and confusing now",
            "I feel lost and dont know which way to go now",
            "My thoughts are going in circles confusing me"
        ]
        
        # Guilty texts
        emotion_texts['guilty'] = [
            "I feel guilty and terrible about everything done",
            "I cannot forgive myself for my past mistakes",
            "The guilt is eating me alive inside my soul",
            "I dont deserve happiness after what I have done",
            "I am filled with regret and self blame today",
            "I feel ashamed of who I have become now",
            "The weight of my guilt is crushing me down",
            "I keep replaying my mistakes constantly today",
            "I feel terrible about things I have done wrong",
            "The guilt is overwhelming and consuming me"
        ]
        
        # Proud texts
        emotion_texts['proud'] = [
            "I feel proud and accomplished today very happy",
            "I have achieved something meaningful in life",
            "My hard work has finally paid off very well",
            "I feel confident in my abilities and skills",
            "I am proud of the person I have become today",
            "My achievements fill me with great pride now",
            "I have overcome challenges successfully today",
            "I deserve to feel good about myself today",
            "I am proud of what I have accomplished now",
            "My success makes me feel proud and happy"
        ]
        
        # Grateful texts
        emotion_texts['grateful'] = [
            "I feel grateful and thankful for everything now",
            "My heart is full of gratitude today very happy",
            "I appreciate all the blessings in my life today",
            "I am thankful for the people around me now",
            "Life has given me so much to appreciate today",
            "I feel deeply grateful for this moment now",
            "There is so much to be thankful for in life",
            "Gratitude fills my heart and soul today",
            "I am grateful for all the good in my life",
            "Thankful for everything I have received"
        ]
        
        return emotion_texts
    
    def generate_dataset(self, samples_per_emotion=150):
        emotion_texts = self.create_text_samples()
        data = []
        
        for emotion, texts in emotion_texts.items():
            # Create base samples
            for text in texts:
                samples_from_text = samples_per_emotion // len(texts)
                for i in range(samples_from_text):
                    variation = self.create_variation(text, i)
                    data.append({
                        'text': variation,
                        'emotion': emotion,
                        'mental_state': self.emotions[emotion]['mental_state'],
                        'timestamp': datetime.now() - timedelta(days=random.randint(0, 365)),
                        'word_count': len(variation.split())
                    })
            
            # Add extra samples if needed
            extra_samples = samples_per_emotion - (len(texts) * (samples_per_emotion // len(texts)))
            for i in range(extra_samples):
                base_text = random.choice(texts)
                variation = self.create_variation(base_text, i)
                data.append({
                    'text': variation,
                    'emotion': emotion,
                    'mental_state': self.emotions[emotion]['mental_state'],
                    'timestamp': datetime.now() - timedelta(days=random.randint(0, 365)),
                    'word_count': len(variation.split())
                })
        
        df = pd.DataFrame(data)
        return df
    
    def create_variation(self, text, index):
        variations = [
            text,
            text.lower(),
            text.upper(),
            text + "!",
            text + ".",
            text + "?",
            "I feel that " + text,
            "To be honest " + text,
            "Really " + text,
            text + " right now",
            text + " today",
            "I must say " + text,
            "Honestly " + text,
            text + " and its true",
            text + " for sure"
        ]
        return variations[index % len(variations)]
    
    def save_dataset(self, filename='enhanced_mental_health_dataset.csv'):
        # Ensure directory exists
        os.makedirs('data/raw', exist_ok=True)
        
        df = self.generate_dataset(samples_per_emotion=150)
        filepath = f'data/raw/{filename}'
        df.to_csv(filepath, index=False)
        
        print(f"✅ Dataset created successfully!")
        print(f"📊 Total samples: {len(df)}")
        print(f"🎭 Emotions distribution:")
        print(df['emotion'].value_counts())
        print(f"💾 Saved to: {filepath}")
        
        return df

if __name__ == "__main__":
    print("🧠 Creating Enhanced Mental Health Dataset...")
    generator = EnhancedMentalHealthDataset()
    dataset = generator.save_dataset()