from groq import Groq
import base64
import os
import ast

def weight_identification(img: str) :
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Estimate the weight(in kg) and body condition score(out of 10) of the dog in the image. ONLY OUTPUT THE APPROXIMATE WEIGHT AND BODY CONDITION SCORE AND NOTHING ELSE.DO NOT RETURN RANGE VALUES. THE OUTPUT SHOULD BE IN THE FOLLOWING FORMAT: {'weight': <weight>, 'body_condition_score': <score>}."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )

    content= chat_completion.choices[0].message.content
    return ast.literal_eval(content)




