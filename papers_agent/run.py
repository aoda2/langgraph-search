import json
import os
from graphs import getGraph

question = "Dense Retrieval のスケーリング則に関する論文."

graph = getGraph()

result = graph.invoke({"question": question},debug=True)

print(result["answer"])
