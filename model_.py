from openai import OpenAI
from typing import Dict, Union

servers_pool = {
    # https://api.gpts.vin/pricing
    'Common': {'api_key': 'sk-Zf8YtRXZ1U8aGwJbWQesWhXudYv6qmtmcn1hC69RkXlzwAbm', 'base_url': 'https://api.gpts.vin/v1'},
    # 'Common': {'api_key': 'sk-r8vgbWY4rMOFpYbmJURjMXlB5uAYSRGisBRNHmk2bvxwpqux', 'base_url': 'https://api.gpts.vin/v1'},
    # 'Common': {'api_key': 'sk-K4JQ7bPUAUePkPzWuqT7PDe0zUH3Dl4XXBJghRs4OIJDOUvN', 'base_url': 'https://api.gpts.vin/v1'},
    
    # https://gpulink.cc/ctrl-personal-center/setting
    '零氪云': {'api_key': 'sk-yn_RESofo9C3ipox74B-iYWzPM7skltYSFYfVfPpjvs', 'base_url': 'https://api.gpulink.cc/v1'},

    # https://cloud.siliconflow.cn/models
    'SiliconCloud': {'api_key': 'sk-mpfdcbyqolnxgsmetcqvoygavtorawxxcjdrlfnjgnwarkbz', 'base_url': 'https://api.siliconflow.cn/v1'},

    # https://www.dmxapi.com/
    'DMXAPI': {'api_key': 'sk-KpD3OBY04XUK7AHF9Ltc5gCpA72QVyuxXIJIaGm6J47v0iTd', 'base_url': 'https://www.dmxapi.com/v1'}
}

class ChatModel(object):
    def __init__(self, config, typed:str = 'server'): # type choice in ['server', 'api']
        if typed == 'server':
            self.model_name = config.get('model_name')
            self.client = OpenAI(**servers_pool.get(config.get('server')))
        elif typed == 'api':
            self.model_name = config.get('model_name')
            self.client = OpenAI(api_key=config.get('api_key'), base_url=config.get('base_url'))
        
        self.config = {
            'max_tokens': 4096,
            'temperature': 0.75,
            'n': 1,
            'stop': None,
            'seed': 0,
        }

    def chat(self, msg, stream: bool=False, is_print: bool=False):
        msg = self._package_msg(msg)
        res = self.client.chat.completions.create(
            model=self.model_name,
            messages=msg,
            stream=stream,
        )
        res = res.choices[0].message.content if not stream else res # 如果是流式传输直接输出流.
        if is_print:
            self.print_stream(res) if stream else print(res)
        return res
    
    def print_stream(self, stream):
        for chunk in stream:
            if chunk.choices and len(chunk.choices)>0:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end='', flush=True)
    
    def _package_msg(self, msg):
        if isinstance(msg, dict):
            return [msg]
        elif isinstance(msg, str):
            return [{"role": "user", "content": msg}]
        elif isinstance(msg, list) and isinstance(msg[0], dict):
            return msg
        else:
            raise TypeError("Expect ['str', 'Dict', 'List[Dict]'], but you give {}".format(type(msg)))


if __name__ == '__main__':
    chat_model = ChatModel(config={'model_name': 'gpt-4o', 'server': 'DMXAPI'}, typed='server')
    chat_model.chat(msg='帮我讲解一下决策树的原理.', stream=True, is_print=True)

    # chat_model = ChatModel(model_name='deepseek-r1', server='零氪云')
    # chat_model.chat(msg='帮我讲解一下决策树的原理.', stream=True, is_print=True)
