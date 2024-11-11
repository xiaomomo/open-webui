import requests

def generate_image(prompt, style='<auto>', size='1024*1024', n=1):
    # API的URL
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

    # 请求头
    headers = {
        'X-DashScope-Async': 'enable',
        'Authorization': 'sk-de260915781943698204c066cb9e8881',  # 替换为你的API Key
        'Content-Type': 'application/json'
    }

    # 请求体
    data = {
        "model": "wanx-v1",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "style": style,
            "size": size,
            "n": n
        }
    }

    try:
        # 发送创建任务请求
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 如果请求失败，抛出异常

        task_id = response.json()['output']['task_id']
        print(f"任务创建成功，任务ID: {task_id}")

        # 根据任务ID查询结果
        getImageTaskResult(task_id)

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")


def getImageTaskResult(task_id):
    result_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    result_response = requests.get(result_url, headers={'Authorization': 'Bearer sk-de260915781943698204c066cb9e8881'})
    result_response.raise_for_status()
    results = result_response.json()['output']['results']
    for i, result in enumerate(results):
        print(f"图片{i + 1} URL: {result['url']}")


# prompt 待优化
prompt = '''
"lesson_story": "Mom, Dad, Freddie and Lisa are visiting the zoo. They are delighted to see swimming turtles and otters. This leads to a conversation on the differences between the animals in the zoo.",
    "vocabulary": [
        "Adjectives - Opposites",
        "big",
        "small",
        "fast",
        "tall",
        "colorful",
    ],

This is my course content. Please draw a picture for my course theme. Add some My Little Pony elements.
'''
# generate_image(prompt)

getImageTaskResult('235fbb17-eb5f-4766-a14f-149ba04ea434')