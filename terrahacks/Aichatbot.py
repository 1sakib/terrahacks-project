from openai import OpenAI

openai = OpenAI(
    api_key='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',
)

conversation = []

def get_gpt_response(user_input):
    message = {
        "role": "user",
        "content": user_input
    }
    conversation.append(message)
    
    response = openai.chat.completions.create(
        messages = conversation,
        model  =  "gpt-3.5-turbo"
    )

    conversation.append(response.choices[0].message)
    
    return response.choices[0].message.content

def chat(model):
    
    user_input = f"please tell me how ecofriendly a {model} is "
    print(user_input)
    response = get_gpt_response(user_input)
    x = response.split()
    return (response)
