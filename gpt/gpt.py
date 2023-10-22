import openai

def readFile(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()
    
def GPTtranslate(words, key):
    result = ''
    example = readFile("example.txt")
    example_ans = readFile("example_ans.txt")
    Question = ' '.join(words)
    
    openai.api_key = key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{example}"},
            {"role": "assistant", "content": f"{example_ans}"},
            {"role": "user", "content": f"{Question}"}
        ]
    )  
    for choice in response.choices:
        result += choice.message.content
    return result
    

# Question = ['我', '小明', '高雄', '一起']
# key = readFile("key.txt")
# result = GPTtranslate(Question, key)
# print(' '.join(Question))
# print(result)

# with open('output.txt', 'w', encoding='utf-8') as output_file:
#     output_file.write(result)