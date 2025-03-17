q_zh = \
"""
下面是一份文档, 你现在要根据文档提出{questions_num}个有意义的问题.

<paper>
{papers}
</paper>

文档已经被放入到了<paper></paper>块中, 你需要将提出的问题放入到<question></question>块中, 不同问题之间以`\n`分割开.
### 示例:
<paper>
小明有一只狗.
</paper>
<question>
小明是如何收养的这只狗?\n小明喜欢这只狗吗?
</question>
"""

q_en = \
"""
Below is a document, and you are now required to propose {questions_num} meaningful questions based on the document.

<paper>
{papers}
</paper>

The document has been placed within the <paper></paper> block. You need to place the proposed questions within the <question></question> block, with different questions separated by `\n`.
### Example:
<paper>
Xiaoming has a dog.
</paper>
<question>
How did Xiaoming adopt this dog?\nDoes Xiaoming like this dog?
</question>
"""