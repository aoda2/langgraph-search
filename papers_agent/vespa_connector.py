import requests
import json
from models import State

vespa_url = "http://localhost:8080/search/"

def search(state: State):
    keywords = state["keywords"]
    # テキストをベクトル化
    query_vector = state["phrase_embedding"]
    # 検索クエリの構築
    yql = "select title, authors, url, abstract from papers where ({{targetHits:10}}nearestNeighbor(embedding,q)) OR ({})"
    # 条件がある場合は追加、ない場合はtrue（すべてのドキュメントにマッチ）
    where_clause = " or ".join([f"abstract contains \"{k}\""  for k in keywords]) if keywords else "true"
    yql = yql.format(where_clause)

    search_request = {
        "yql": yql,
        "hits": 3,
        "ranking": {"profile" : "closeness"},
        "input.query(q)": query_vector,
        "timeout": "10s"
    }

    response = requests.post(vespa_url, json=search_request)
    results = response.json()

    # 結果の処理
    return {
        "search_result": [
            {
                "title": hit.get("fields", {}).get("title"),
                "authors": hit.get("fields", {}).get("authors"),
                "url": hit.get("fields", {}).get("url"),
                "abstract": hit.get("fields", {}).get("abstract", []),
                "relevance": hit.get("relevance"),
            }
            for hit in results.get("root", {}).get("children", [])
        ]
    }
