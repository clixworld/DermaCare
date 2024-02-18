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
                {"role": "system", "content": "You are a helpful assistant returning a general treatment option based on the type of acne and user skin type. If acne is birthmark just wrtie positive affirmation that its natural and by birth. Also when returning link, don't use healthline. Return a JSON with these keys: diagnosis, overview, suggestion. For diagnosis, just return the type of acne given. For overview, return a summary about 3 to 5 sentences about the type of acne. For suggestion, just recommend ingredients based on type of acne and skin type along with suggested routine."},
                {"role": "user", "content": f"{user_acne}, skin-type = {skin_type}."}
            ]
        )
        return(completion.choices[0].message.content)