## 需要的环境.
```cmd
pip install openai
```

api.json替换为自己的api, 格式见示例文件. <br/>
model_.py中servers_pool中填入自己的api. <br/>

将你想要提取的论文放入MD文件夹中, 示例放入了几篇论文, 针对每个文献提出的问题在QU文件夹中.<br/>
`logging.txt`记录了一次运行的日志.<br/>

请确保填补了api.json和model_.py后, 再运行try.py, 在终端中执行
```python
python try.py
```
您应该能观察到logging.txt中的变化.
