from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from openai_connector import getQuery, getEmbedding, translation
from vespa_connector import search

from models import State

def getGraph():
    # Graphの作成
    graph_builder = StateGraph(State)

    # Nodeの追加
    graph_builder.add_node("getQuery", getQuery)
    graph_builder.add_node("getEmbedding", getEmbedding)
    graph_builder.add_node("search", search)
    graph_builder.add_node("translation", translation)

    # Nodeをedgeに追加 
    graph_builder.add_edge(START, "getQuery")
    graph_builder.add_edge("getQuery", "getEmbedding")
    graph_builder.add_edge("getEmbedding", "search")
    graph_builder.add_edge("search", "translation")
    graph_builder.add_edge("translation", END)

    # Graphをコンパイル
    graph = graph_builder.compile()
    # Graphを出力
    print(graph.get_graph().draw_mermaid())

    return graph