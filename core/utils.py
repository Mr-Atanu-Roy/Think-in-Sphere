import threading
import pyttsx3

from unique_names_generator import get_random_name
from unique_names_generator.data import ADJECTIVES, STAR_WARS, NAMES


import openai
import os


# Load OPENAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")



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


def openai_completion_endpoint(query):
    
    prompt = f"The following is a conversation of a student with an AI assistant. The assistant is helpful, creative, clever, and very friendly and answers all the questions of the student very clearly.\n\nHuman: {query}\n\nAI:"
                                    
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=1500,
    temperature=0.9,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"],
    )
    
    result =  response["choices"][0]["text"]
    result = result.lstrip()
    
    return result


def openai_image_endpoint(query):
    
    response = openai.Image.create(
    prompt= query,
    n=2,
    size="256x256"
    )
    # print(response)
    imgURLS = []
    for img in response["data"]:
        imgURLS.append(img["url"])
    
    return imgURLS


def openai_general_endpoint(prompt, token=2045, temperature=0.7):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Generate subtopics for course {prompt}",
        temperature=temperature,
        max_tokens=token,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream = False,
    )
    result = response.choices[0].text.strip()
    
    return result

