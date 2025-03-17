import threading
from model_ import ChatModel

quest = ['Hi', '1+1=?', '讲解一下什么是决策树.']

def task(q, chat_model):
    res = chat_model.chat(q)
    print(res)

if __name__ == '__main__':
    chat_model = ChatModel(config={'model_name': 'gpt-4o', 'server': 'Common'}, typed='server')
    thread = []
    
    for i in range(3):
        t = threading.Thread(target=task, args=(quest[i], chat_model))
        thread.append(t)
        t.start()
    
    for t in thread:
        t.join()
    
    print('所有线程执行完毕.')