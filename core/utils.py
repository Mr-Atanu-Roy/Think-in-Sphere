import threading
import os
from io import BytesIO
from gtts import gTTS
from playsound import playsound
from googletrans import Translator, LANGUAGES

from unique_names_generator import get_random_name
from unique_names_generator.data import ADJECTIVES, STAR_WARS, NAMES

import uuid

import openai

# Load OPENAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

class Speak(threading.Thread):
    
    def __init__(self, answer, speak_lang):
        self.answer = answer
        self.speak_lang = speak_lang
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            tts = gTTS(text=self.answer, lang=self.speak_lang)    # Create a gTTS object
            filename = f"{str(uuid.uuid4())}.mp3"
            tts.save(filename)
            playsound(filename)
            
            # fp = BytesIO()
            # tts.write_to_fp(fp)
            # fp.seek(0)
            # playsound(fp)
        except Exception as e:
            print(e) 

            
def random_name():
    '''function to check if given string contains any special charecter'''
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
        prompt=prompt,
        temperature=temperature,
        max_tokens=token,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream = False,
    )
    result = response.choices[0].text.strip()
    
    return result



def detect_language(text):
    '''func to detect language of a given text'''
    #return format : language-code, language, error
    
    try:
        translator = Translator()
        lang = translator.detect(text).lang
        return lang, LANGUAGES[lang], None
    
    except AttributeError:
        error = "Failed to detect lang"
        return None, None, error
    
    except Exception as e:
        print(e)
        return None, None, e


def translate_text(text, from_lang, to_lang):
    '''This func will convert given text from one lang to other'''
    #return format : translated-text, error
    
    translator = Translator()
    try:
        result = translator.translate(text, src=from_lang, dest=to_lang)
        return result.text, None
    
    except Exception as e:
        print(e)
        return None, e    

