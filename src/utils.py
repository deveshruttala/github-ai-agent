import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_comment(issue_title, issue_body):
#     prompt = f"""
#     Given this issue:
#     Title: {issue_title}
#     Body: {issue_body}

#     Write a short, helpful, and friendly comment showing how Hyperbrowser (an AI-native browser infra) could help.
#     """
    
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     return response.choices[0].message.content


def generate_comment(issue_title, issue_body):
    return (
        "👋 Hey there! This looks like something Hyperbrowser could assist with. "
        "We're building an AI-native browser that automates workflows, integrates smart tools, and enhances productivity directly inside the browser. "
        "If you're tackling tasks like this often, Hyperbrowser might be just what you need.\n\n"
        "🚀 Learn more and try it out: https://www.hyperbrowser.ai/\n"
        "We’d love your feedback!"
    )
