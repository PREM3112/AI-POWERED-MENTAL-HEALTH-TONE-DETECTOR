def get_mental_health_suggestions(emotion):
    suggestions = {
        'Anger': [
            "Practice deep breathing exercises for 5 minutes",
            "Take a walk in nature to calm your mind",
            "Express your feelings through journaling",
            "Try progressive muscle relaxation techniques",
            "Count slowly to 10 before responding"
        ],
        'Anxiety': [
            "Practice the 5-4-3-2-1 grounding technique",
            "Use box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s",
            "Limit caffeine and sugar intake",
            "Try mindfulness meditation for 10 minutes",
            "Create a worry list and schedule worry time"
        ],
        'Depression': [
            "Establish a consistent daily routine",
            "Engage in 30 minutes of physical activity",
            "Connect with supportive friends or family",
            "Practice self-compassion and positive self-talk",
            "Consider speaking with a mental health professional"
        ],
        'Stress': [
            "Practice time management with the Pomodoro technique",
            "Take regular breaks throughout your day",
            "Try yoga or gentle stretching exercises",
            "Listen to calming music or nature sounds",
            "Prioritize self-care activities daily"
        ],
        'Sadness': [
            "Express emotions through creative outlets like art or music",
            "Spend time in sunlight or nature",
            "Practice gratitude by listing 3 things you're thankful for",
            "Listen to uplifting or comforting music",
            "Reach out to loved ones for support"
        ],
        'Loneliness': [
            "Join local community groups or clubs",
            "Volunteer for a cause you care about",
            "Reconnect with old friends via call or message",
            "Consider adopting a pet for companionship",
            "Explore online communities with shared interests"
        ],
        'Overwhelm': [
            "Break large tasks into smaller, manageable steps",
            "Use the Eisenhower Matrix to prioritize tasks",
            "Practice saying no to additional commitments",
            "Delegate tasks when possible",
            "Focus on one thing at a time"
        ],
        'Fear': [
            "Practice gradual exposure to what you fear",
            "Use positive affirmations and self-talk",
            "Visualize positive outcomes and success",
            "Learn facts about what you fear to reduce uncertainty",
            "Seek support from trusted individuals"
        ],
        'Joy': [
            "Savor and fully appreciate the present moment",
            "Share your happiness with others",
            "Express gratitude for your positive experiences",
            "Continue engaging in activities that bring you joy",
            "Spread positivity through small acts of kindness"
        ],
        'Contentment': [
            "Practice mindfulness to stay present",
            "Maintain healthy routines and habits",
            "Continue regular self-care practices",
            "Set new meaningful goals for personal growth",
            "Appreciate your current state while planning for the future"
        ],
        'Frustration': [
            "Take a short break and return with fresh perspective",
            "Identify the specific source of frustration",
            "Try a different approach to the problem",
            "Practice patience and understanding",
            "Seek help or advice from others"
        ],
        'Confusion': [
            "Break down information into smaller parts",
            "Ask clarifying questions",
            "Take notes and organize your thoughts",
            "Seek additional information or resources",
            "Give yourself time to process information"
        ]
    }
    
    # Default suggestions for emotions not in the dictionary
    default_suggestions = [
        "Practice mindfulness and meditation for 10 minutes",
        "Engage in 30 minutes of physical activity",
        "Connect with supportive people in your life",
        "Maintain a consistent sleep schedule of 7-9 hours",
        "Consider speaking with a mental health professional",
        "Practice deep breathing exercises",
        "Spend time in nature or fresh air"
    ]
    
    return suggestions.get(emotion, default_suggestions)[:5]  # Return top 5 suggestions