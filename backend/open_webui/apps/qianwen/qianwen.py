import os
from dashscope import MultiModalConversation

local_path = "/Users/liuqingjie/code/ai-tts/open-webui/backend/open_webui/apps/qianwen/content.png"
image_path = f"file://{local_path}"
messages = [{'role': 'system',
             'content': [{'text': 'You are a helpful assistant.'}]},
            {'role':'user',
             'content': [{'image': image_path},
                         {'text': ' 帮我识别下这个图片的内容，把内容信息以json的形式整理出来'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-vl-max-latest',
    messages=messages)
print(response["output"]["choices"][0]["message"].content[0]["text"])