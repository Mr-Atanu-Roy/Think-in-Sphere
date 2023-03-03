import threading
import pyttsx3

from unique_names_generator import get_random_name
from unique_names_generator.data import ADJECTIVES, STAR_WARS, NAMES

class Speak(threading.Thread):
    
    def __init__(self, answer):
        self.answer = answer
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 194)
                
            engine.say(self.answer)
            engine.runAndWait()
        except Exception as e:
            print(e) 
            
            
def random_name():
    return get_random_name(combo=[ADJECTIVES, STAR_WARS, NAMES])

