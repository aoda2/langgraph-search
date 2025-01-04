from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from openai_connector import getEmbedding
from models import State

def getGraph():
    # Graphの作成
    graph_builder = StateGraph(State)

    # Nodeの追加
    graph_builder.add_node("getEmbedding", getEmbedding)

    # Nodeをedgeに追加 
    graph_builder.add_edge(START, "getEmbedding")
    graph_builder.add_edge("getEmbedding", END)

    # Graphをコンパイル
    graph = graph_builder.compile()
    # Graphを出力
    print(graph.get_graph().draw_mermaid())

    return graph