import re

class Content:
    def __init__(self, content):
        self.content = content

def lowercaseContent(r):
    origin_content = r.content
    # 使用正则表达式将内容按单词和非单词字符分割
    tokens = re.findall(r'\b\w+\b|\W', origin_content)
    lowercase_tokens = []

    for token in tokens:
        if token.isupper():
            lowercase_tokens.append(token.lower())
        else:
            lowercase_tokens.append(token)

    # 将处理后的令牌重新拼接成字符串
    lowercase = ''.join(lowercase_tokens)
    r.content = lowercase

def main():
    # 创建一个 Content 对象
    r = Content("HELLO, WORLD! THIS IS A Blippi, Yaya. HOW are You?")

    # 调用 lowercaseContent 函数
    lowercaseContent(r)

    # 输出处理后的内容
    print("HELLO, WORLD! THIS IS A Blippi, Yaya. HOW are You?")
    print("Original content:", r.content)

if __name__ == "__main__":
    main()