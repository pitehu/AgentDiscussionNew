from together import Together
from openai import AzureOpenAI
# import openai

client = Together(api_key="7675a6f57ac7baa706729c0e04f6d9de45753165eddf235acb1801285247db1f")

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
)
print(response)
print(response.choices)
print(response.choices[0].message.content)