import os
import openai
import time
import logging
import json
from dotenv import load_dotenv
load_dotenv()
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 

persona_template = """
You are {name}. {whoami} 
{conversationwith} 
{traits}
{conversationnavigator}
Reply based on conversation history provided in 'Context:'
Reply with prefix '{chatname}:'
Respond with {responselength} words max.
When {chatname} wants to end conversation, send a token *STOP* back.
"""

def loadContext(persona):
    return persona_template.format(name = persona['bot']['name'],whoami = persona['bot']['whoami'],
                                   conversationwith = persona['bot']['conversationwith'],
                                   traits = persona['bot']['traits'],
                                   chatname = persona['bot']['chatname'],
                                   responselength = persona['bot']['responselength'])

#logging.basicConfig(filename='logs/app.log', level=logging.INFO)
OPENAIKEY= os.environ.get('OPENAIKEY')
openai.api_key = OPENAIKEY

file_b = 'personas/'+os.environ.get('botdefinitionfile')
thebot = json.load(open(file_b))
botcontext = loadContext(thebot)

conversationBuffer = []

@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(2))
def completion_with_backoff(messages_):
    try:

     completion = openai.ChatCompletion.create(
                        model = "gpt-3.5-turbo",
                        messages = messages_,
                        temperature=1.75,
                        max_tokens=50,
                        stop="*STOP*",
                        #stream=True
                        )
     return completion.choices[0].message.content
    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass

print("Conversing as " + thebot['human']['name'] + ". Start your conversation with bot "+ thebot['bot']['name'] )

for x in range(20):
    if len(conversationBuffer) > 10:
        conversationBuffer.pop(0)
        conversationBuffer.pop(1)
    p1_ = input(thebot['human']['chatname']+": ")
    messages = [
                {"role": "system", "content": botcontext},
                {"role": "system", "content": "Context:\n"+"".join(conversationBuffer)},
                {"role": "user", "content": thebot['human']['chatname']+":"+ p1_}
              ]
    p2_ = completion_with_backoff(messages)
    print(p2_)
    conversationBuffer.append(thebot['human']['chatname']+":"+ p1_[0:150]+"\n")  
    conversationBuffer.append(p2_[0:150]+"\n")
    time.sleep(2)
print("End of Conversation")





