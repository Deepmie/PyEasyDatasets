g_zh = \
"""
你现在要针对一个问题, 给出自己的思考.

<question>
{question}
</question>

问题已经被放入到<question></question>块中, 请将你的思考填入到<Thinking></Thinking>块中.

### 示例:
<question>
1+1=?
</question>
返回
<Thinking>
关于这个问题的思考.
</Thinking>
"""

g_en = \
"""
You are now required to provide your thoughts on a problem.

<question>
{question}
</question>

The question has been placed in the <question></question> block. Please provide your thoughts in the <Thinking></Thinking> block.

### Example:
<question>
1+1=?
</question>
you should return
<Thinking>
Reflections on the issue.
</Thinking>
"""