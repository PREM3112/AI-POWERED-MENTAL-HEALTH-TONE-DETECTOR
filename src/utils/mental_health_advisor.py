class MentalHealthAdvisor:
    def __init__(self):
        self.recommendations = {
            'happy': {
                'immediate': [
                    "Share your positive energy with others",
                    "Practice gratitude journaling",
                    "Engage in activities that bring you joy",
                    "Connect with loved ones and spread happiness"
                ],
                'long_term': [
                    "Maintain a gratitude practice daily",
                    "Continue engaging in hobbies you love",
                    "Build strong social connections",
                    "Set new positive goals for yourself"
                ],
                'professional': "Continue current mental wellness practices",
                'urgency': 'low',
                'color': '#4CAF50'
            },
            
            'sad': {
                'immediate': [
                    "Allow yourself to feel and process the sadness",
                    "Reach out to a trusted friend or family member",
                    "Engage in gentle self-care activities",
                    "Watch a comforting movie or listen to soothing music"
                ],
                'long_term': [
                    "Practice self-compassion and acceptance",
                    "Consider talking to a therapist about recurring sadness",
                    "Establish a daily routine with small enjoyable activities",
                    "Join a support group for emotional well-being"
                ],
                'professional': "If sadness persists for more than 2 weeks, consider consulting a mental health professional",
                'urgency': 'medium',
                'color': '#2196F3'
            },
            
            'anxious': {
                'immediate': [
                    "Practice deep breathing exercises (4-7-8 technique)",
                    "Use grounding techniques: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
                    "Take a short walk or do light stretching",
                    "Write down your worries to get them out of your head"
                ],
                'long_term': [
                    "Practice mindfulness meditation daily",
                    "Limit caffeine and sugar intake",
                    "Establish a consistent sleep schedule",
                    "Learn cognitive behavioral techniques"
                ],
                'professional': "Consider therapy if anxiety affects daily functioning",
                'urgency': 'medium',
                'color': '#FF9800'
            },
            
            'angry': {
                'immediate': [
                    "Take a timeout and count to 10 slowly",
                    "Express your feelings using 'I' statements",
                    "Engage in physical activity to release tension",
                    "Practice progressive muscle relaxation"
                ],
                'long_term': [
                    "Learn anger management techniques",
                    "Identify triggers and develop coping strategies",
                    "Practice assertive communication",
                    "Consider mindfulness-based stress reduction"
                ],
                'professional': "Anger management therapy can provide effective tools",
                'urgency': 'medium',
                'color': '#f44336'
            },
            
            'stressed': {
                'immediate': [
                    "Break tasks into smaller, manageable steps",
                    "Practice the 4-7-8 breathing technique",
                    "Take a 5-minute meditation break",
                    "Prioritize and delegate tasks when possible"
                ],
                'long_term': [
                    "Establish work-life boundaries",
                    "Practice time management techniques",
                    "Engage in regular physical exercise",
                    "Learn to say no to additional commitments"
                ],
                'professional': "Stress management counseling can be beneficial",
                'urgency': 'medium',
                'color': '#9C27B0'
            },
            
            'depressed': {
                'immediate': [
                    "Reach out to a crisis helpline if needed",
                    "Contact a trusted person immediately",
                    "Focus on getting through the next hour, not the whole day",
                    "Practice basic self-care: drink water, eat something light"
                ],
                'long_term': [
                    "Seek professional mental health support",
                    "Establish a daily routine with small achievable goals",
                    "Engage in gentle physical activity",
                    "Connect with support groups"
                ],
                'professional': "URGENT: Contact a mental health professional or crisis line immediately",
                'urgency': 'high',
                'color': '#607D8B'
            },
            
            'neutral': {
                'immediate': [
                    "Practice mindfulness of the present moment",
                    "Engage in a favorite hobby or activity",
                    "Connect with nature through a short walk",
                    "Read or listen to something inspiring"
                ],
                'long_term': [
                    "Maintain balanced lifestyle habits",
                    "Continue regular self-care practices",
                    "Stay connected with supportive relationships",
                    "Monitor emotional patterns over time"
                ],
                'professional': "Regular mental health check-ins are beneficial",
                'urgency': 'low',
                'color': '#9E9E9E'
            },
            
            'lonely': {
                'immediate': [
                    "Call a friend or family member",
                    "Visit a public place like a café or park",
                    "Join an online community with shared interests",
                    "Write about your feelings in a journal"
                ],
                'long_term': [
                    "Volunteer for causes you care about",
                    "Join clubs or groups with similar interests",
                    "Develop new hobbies that involve social interaction",
                    "Practice building social skills gradually"
                ],
                'professional': "Therapy can help address underlying social anxiety",
                'urgency': 'medium',
                'color': '#795548'
            },
            
            'confused': {
                'immediate': [
                    "Write down your thoughts to organize them",
                    "Talk through your confusion with someone",
                    "Take a break and return to the problem later",
                    "Break complex issues into smaller questions"
                ],
                'long_term': [
                    "Practice decision-making skills",
                    "Learn problem-solving techniques",
                    "Develop critical thinking habits",
                    "Seek mentorship or guidance"
                ],
                'professional': "Cognitive therapy can help with decision-making",
                'urgency': 'low',
                'color': '#FF5722'
            },
            
            'guilty': {
                'immediate': [
                    "Practice self-forgiveness and compassion",
                    "Write a letter of apology (send or don't send)",
                    "Learn from the experience without self-punishment",
                    "Focus on making amends where possible"
                ],
                'long_term': [
                    "Work on self-acceptance and self-worth",
                    "Practice mindfulness to stay present",
                    "Challenge perfectionistic tendencies",
                    "Develop healthy coping mechanisms"
                ],
                'professional': "Therapy can help process and release guilt",
                'urgency': 'medium',
                'color': '#673AB7'
            },
            
            'proud': {
                'immediate': [
                    "Acknowledge and celebrate your achievement",
                    "Share your success with supportive people",
                    "Reflect on the journey that led to this moment",
                    "Express gratitude for the support you received"
                ],
                'long_term': [
                    "Set new challenging but achievable goals",
                    "Maintain a success journal",
                    "Use this confidence to tackle other challenges",
                    "Mentor others who are on similar paths"
                ],
                'professional': "Continue building on this positive self-image",
                'urgency': 'low',
                'color': '#4CAF50'
            },
            
            'grateful': {
                'immediate': [
                    "Write down three specific things you're grateful for",
                    "Express your gratitude to someone directly",
                    "Practice mindful appreciation of small moments",
                    "Share your grateful thoughts with others"
                ],
                'long_term': [
                    "Maintain a daily gratitude practice",
                    "Volunteer to help others in need",
                    "Cultivate mindfulness in daily activities",
                    "Create gratitude rituals with family/friends"
                ],
                'professional': "Gratitude practices enhance overall well-being",
                'urgency': 'low',
                'color': '#4CAF50'
            }
            
        }
        
        self.crisis_resources = {
            'hotlines': [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "SAMHSA National Helpline: 1-800-662-4357",
                "The Trevor Project: 1-866-488-7386 (LGBTQ+)"
            ],
            'online_resources': [
                "Psychology Today Therapist Directory",
                "BetterHelp Online Counseling",
                "7 Cups of Tea Free Counseling",
                "Mindfulness Apps: Headspace, Calm"
            ]
        }
    
    def get_comprehensive_advice(self, emotion):
        """Get comprehensive mental health advice based on emotion"""
        
        if emotion not in self.recommendations:
            emotion = 'neutral'
        
        advice = self.recommendations[emotion]
        
        return {
            'emotion': emotion,
            'immediate_actions': advice['immediate'],
            'long_term_strategies': advice['long_term'],
            'professional_guidance': advice['professional'],
            'urgency_level': advice['urgency'],
            'color': advice['color'],
            'crisis_resources': self.crisis_resources if advice['urgency'] == 'high' else None
        }
    
    def generate_care_plan(self, emotion_history):
        """Generate a personalized mental health care plan"""
        
        if not emotion_history:
            return {
                'weekly_focus': "Emotional Awareness",
                'daily_practices': [
                    "Check in with your emotions each morning",
                    "Practice 5 minutes of mindfulness daily",
                    "Write one thing you're grateful for each day"
                ],
                'weekly_goals': [
                    "Track your emotions daily",
                    "Connect with one supportive person",
                    "Engage in one enjoyable activity"
                ]
            }
        
        # Analyze recent emotions
        recent_emotions = [entry['emotion'] for entry in emotion_history[-7:]]
        primary_emotion = max(set(recent_emotions), key=recent_emotions.count)
        
        primary_advice = self.recommendations[primary_emotion]
        
        return {
            'primary_concern': primary_emotion,
            'weekly_focus': f"Managing {primary_emotion} feelings",
            'daily_practices': primary_advice['immediate'][:2],
            'weekly_goals': [
                "Practice recommended strategies daily",
                "Check in with emotions each morning and evening",
                "Connect with support system at least 3 times",
                "Engage in self-care activities regularly"
            ],
            'progress_tracking': "Use this app daily to monitor emotional changes",
            'next_steps': "Continue with current plan and adjust as needed"
        }