import openai
import os
from dotenv import load_dotenv


class ChatGPT():
    load_dotenv()
    def messages(self, user_acne, skin_type):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        completion = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a helpful assistant returning a general treatment option based on the type of acne and user skin type. Return a JSON with these keys: diagnosis, suggestion1, suggestion2, suggestion3, link. And give the values you think would fit best."},
                {"role": "user", "content": f"Acne {user_acne}, Skin Type {skin_type}."}
            ]
        )
        return(completion.choices[0].message.content)