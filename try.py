import glob
from model_ import ChatModel
import threading
import json
from datetime import datetime
import os
from prompt import qu, ge
import random
import re
import json

class EasyDataset(object):
    def __init__(self):
        self._print_log('Start from {}'.format(datetime.now()))
        self.mds_path = 'MD/*.md'
        self.questions_path = 'QU'
        self.api_json_path = 'api.json'
        self.mds_file_path = glob.glob(self.mds_path)
        self.mds_cache_list = []
        self.qu_cache_list = []
        self.res_list = []
        self.threads = []
        self.questions_num = 5
        self.max_retry = 3

        # 实例化一个agent, 用于总结文档提出问题.
        self.questioner = ChatModel(config={'model_name': 'gpt-4o', 'server': 'DMXAPI'}, typed='server')
        self._load_all_agents()

    def test(self):
        self._generate_questions()

        with open('res.json', mode='w', encoding='utf-8') as f:
            f.write(json.dumps(self.res_list))
        
        self._print_log('Start from {}'.format(datetime.now()))

    def _generate_questions(self):
        def is_not_none(q):
            if isinstance(q, str):
                q = q.strip()
            return q is not None and len(q) > 0
        
        for idx, mp in enumerate(self.mds_file_path):
            self._print_log('Now operate the {} markdown: {} Time: {}'.format(idx, mp, datetime.now()))
            qp = os.path.basename(mp).replace('.md', '.txt')
            if qp in os.listdir(self.questions_path):
                continue
            else:
                qp = os.path.join(self.questions_path, qp)

            questions_pool = []
            with open(mp, encoding='utf-8', mode='r') as mdreader:
                mdcontent = mdreader.read()
            while len(questions_pool) < self.questions_num:
                q_en = qu.q_en.format(
                    questions_num=self.questions_num,
                    papers=mdcontent,
                )
                
                # 添加问题到问题池中.
                res = None
                retry = 0
                while res is None and retry < self.max_retry:
                    res = self._extract(self.questioner.chat(msg=q_en), mark=('<question>', '</question>'))
                    retry += 1
                
                res = list(filter(is_not_none, res.split('\n')))
                
                self._print_log('generate questions:\n{}'.format('\n'.join(res)))
                questions_pool += res
            
            questions_pool = random.sample(questions_pool, self.questions_num) # 如果生成多了, 随机抽取几个.
            with open(qp, encoding='utf-8', mode='w') as quwriter:
                quwriter.write('\n'.join(questions_pool))

            self._generate_think_batch(questions_pool) # 批量进行思考
        
        for t in self.threads:
            t.join()
    
    def _generate_think(self, question):
        # 随机抽取一个agent.
        idx, responser = random.sample(self.responser, k=1)[0]
        self._print_log('Choise the {} api, have send the request.'.format(idx))
        g_en = ge.g_en.format(
            question=question,
        )

        res = None
        retry = 0
        while res is None and retry < self.max_retry:
            res = self._extract(responser.chat(msg=g_en), mark=('<Thinking>', '</Thinking>'))
            retry += 1
        
        self.res_list.append((question, '<Thinking>\n{}\n</Thinking>'.format(res.strip())))

        with open('temp.jsonl', mode='a', encoding='utf-8') as ap:
            ap.write(json.dumps({'question': question, 'thinking': '<Thinking>\n{}\n</Thinking>'.format(res.strip())}, indent=4)+'\n')
        
        return res

    def _generate_think_batch(self, questions_list):
        for question in questions_list:
            t = threading.Thread(target=self._generate_think, args=(question, ))
            self.threads.append(t)
            t.start()

    def _load_all_agents(self):
        # agent组, 用于针对每个问题给出思维链回复.
        self.responser = []
        with open(self.api_json_path, encoding='utf-8', mode='r') as reader:
            api_pools = json.loads(reader.read())
        
        for idx, api in enumerate(api_pools):
            self.responser.append((idx, ChatModel(config=api, typed='api')))

    def _extract(self, txt, mark):
        pattern = r"{}(.*?){}".format(mark[0], mark[1])
        matches = re.findall(pattern, txt, re.IGNORECASE | re.DOTALL)
        if len(matches) == 0:
            return None
        return matches[0]
    
    def _print_log(self, s):
        with open('logging.txt', mode='a', encoding='utf-8') as f:
            f.write(s+'\n')



if __name__ == '__main__':
    easydataset = EasyDataset()
    easydataset.test()