import asyncio

import openai
import os

# Load OPENAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

async def async_openai_general_endpoint(prompt, token=2045, temperature=0.7):
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


async def get_notes(topic):
    prompt = f"generate detailed study notes on topic {topic}"
    result = await async_openai_general_endpoint(prompt, temperature=0.8)
    return result

async def get_summery(topic):
    prompt = f"generate detailed summery, important points on topic {topic}"
    result = await async_openai_general_endpoint(prompt, token=1200, temperature=0.5)
    return result

async def get_questions(topic):
    prompt = f"generate 20 to 40 important questions related to topic {topic}"
    result = await async_openai_general_endpoint(prompt, temperature=0.6)
    return result

async def main(topic):
    # Start all three functions concurrently using asyncio.gather()
    notes, summery, questions = await asyncio.gather(
        get_notes(topic), get_summery(topic), get_questions(topic)
    )
    
    return notes, summery, questions

# Run the main coroutine
def generate_content(topic):
    notes, summery, question = asyncio.run(main(topic))
    
    return notes, summery, question
