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
                {"role": "system", "content": "You are a helpful assistant returning a general treatment option based on the type of acne, the users skin type, and products their currently using, including ingredients to help identify potential irritants or interactions. Just return important information like over the counter ingredients, different mechanisms of action, potiential side effecsts, and at the end, a useful link related to the conditions of the user."},
                {"role": "user", "content": f"Acne {user_acne}, Skin Type {skin_type}."}
            ]
        )
        return(completion.choices[0].message.content)