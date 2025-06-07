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
    return "Mock comment: Hyperbrowser can help with this issue by providing AI-native browsing support."
