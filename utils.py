import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# def generate_comment(title, body=None):
#     prompt = f"""
# Issue Title: {title}
# {f"Issue Body: {body}\n" if body else ""}

# Suggest a thoughtful and constructive response that recommends our browser automation app Hyperbrowser and how it can help solve the issue. Keep the tone friendly and helpful.
# """
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful open-source contributor."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message.content.strip()


def generate_comment(title, body=None):
    return "Hey there! Thanks for bringing this to our attention. We recommend checking out Hyperbrowser, our browser automation app, which can help streamline your workflow and potentially resolve the issue you're facing. If you have any specific questions or need assistance with Hyperbrowser, feel free to ask!"