import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
prompt = """

summary this data:

Input Content: 
<content>
从前，有个男人死了妻子，有个女人死了丈夫。 这个男人有个女儿，这个女人也有个女儿。 
</content>


"""
completion = client.chat.completions.create(
    model='qwen-max',
    messages=[
        {'role': 'user', 'content': prompt}
    ]
)

print(completion.model_dump_json())