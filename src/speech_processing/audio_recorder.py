import os
import wave
import time
import numpy as np
from datetime import datetime

class AudioRecorder:
    def __init__(self):
        self.sample_rate = 16000
        self.channels = 1
        self.chunk = 1024
        self.frames = []
        
    def record_audio(self, duration=5, filename="recording.wav"):
        """Record audio for specified duration"""
        try:
            # Try to use pyaudio for actual recording
            import pyaudio
            
            print(f"🎤 Recording audio for {duration} seconds...")
            
            p = pyaudio.PyAudio()
            
            stream = p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.frames = []
            
            print("🔴 Recording started... Speak now!")
            for i in range(0, int(self.sample_rate / self.chunk * duration)):
                data = stream.read(self.chunk)
                self.frames.append(data)
                
            print("🟢 Recording finished")
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Save the recorded data as a WAV file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            
            print(f"💾 Audio saved as: {filename}")
            return filename
            
        except ImportError:
            print("⚠️ PyAudio not available, creating simulated audio file")
            return self.create_simulated_audio(duration, filename)
        except Exception as e:
            print(f"❌ Recording failed: {e}")
            return self.create_simulated_audio(duration, filename)
    
    def create_simulated_audio(self, duration, filename):
        """Create a simulated audio file for testing"""
        try:
            sample_rate = 16000
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Generate different audio patterns based on time (simulating speech)
            # Mix of frequencies to simulate human voice
            freq1 = 100 + 50 * np.sin(2 * np.pi * 0.5 * t)  # Varying base frequency
            freq2 = 200 + 100 * np.sin(2 * np.pi * 1.0 * t)  # Varying mid frequency
            
            audio_data = (np.sin(2 * np.pi * freq1 * t) * 0.4 + 
                         np.sin(2 * np.pi * freq2 * t) * 0.3 +
                         np.random.normal(0, 0.1, len(t)) * 0.3)
            
            # Normalize and convert to 16-bit integers
            audio_data = np.int16(audio_data * 32767)
            
            with wave.open(filename, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())
            
            print(f"📁 Created simulated audio file: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Failed to create simulated audio: {e}")
            return f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

    def get_audio_duration(self, filename):
        """Get duration of audio file"""
        try:
            with wave.open(filename, 'r') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return frames / float(rate)
        except:
            return 0