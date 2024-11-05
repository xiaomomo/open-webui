"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional
import re

# 这个对音频无效，因为页面输出的就先是纯大写了。可以给底层或者页面，需要思考下。
class Filter:
    class Valves(BaseModel):
#         priority: int = Field(
#             default=0, description="Priority level for the filter operations."
#         )
#         max_turns: int = Field(
#             default=8, description="Maximum allowable conversation turns for a user."
#         )
        pass

    class UserValves(BaseModel):
#         max_turns: int = Field(
#             default=4, description="Maximum allowable conversation turns for a user."
#         )
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")

#         if __user__.get("role", "admin") in ["user", "admin"]:
#             messages = body.get("messages", [])
#
#             max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)
#             if len(messages) > max_turns:
#                 raise Exception(
#                     f"Conversation turn limit exceeded. Max turns: {max_turns}"
#                 )

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        # 解析body，将 messages里role是assistant的content内容里全是大写的单词改成小写字母单词
        for message in body.get('messages', []):
            if message.get('role') == 'assistant':
                content = message.get('content', '')
                # 使用正则表达式匹配全大写的单词，并转换为小写
                print(f"origin_content:"+content)
                message['content'] = self.lowercaseContent(content)
                print(f"lowercase_content:"+ message['content'])

        print(f"outlet:user:{__user__}")
        return body

    def lowercaseContent(self, content: str) -> str:
            origin_content = content
            # 使用正则表达式将内容按单词和非单词字符分割
            tokens = re.findall(r'\b\w+\b|\W', origin_content)
            lowercase_tokens = []

            for token in tokens:
                if token.isupper():
                    lowercase_tokens.append(token.lower())
                else:
                    lowercase_tokens.append(token)

            # 将处理后的令牌重新拼接成字符串
            return ''.join(lowercase_tokens)