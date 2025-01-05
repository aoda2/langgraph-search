import json
from models import State
from openai import OpenAI
from pydantic import BaseModel


client = OpenAI()

# https://platform.openai.com/docs/guides/structured-outputs
query_propmt = '''
あなたはInformation Retrievalの専門家であり、アクセス可能なVespaサーバーからユーザーの役に立つ論文を週出するためのプロフェッショナルです。

ユーザーから提供された検索意図を正確に理解し、Vespaサーバに適切な検索クエリを発行するために以下の形式で回答してください:

1. ユーザーの意図を正確に要約し、関連する検索キーワードを抽出してください。これらのキーワードは、`abstract`フィールドでOR検索するために使用します。多くの論文をhitさせるために関連のありそうな多くのキーワードをリストで提案してください。尚、論文はすべて英語なので検索キーワードも英語である必要があります。
2. 高次元埋め込みを用いた検索のために、ユーザーの意図に基づいた検索フレーズを生成してください。このフレーズは、`embedding`フィールドでランキングするために使用されます。

例:  
ユーザーの入力: "dense retrieval のスケーリング則が知りたい"  
あなたの出力形式:  
{{
    "keywords": ["dense retrieval", "scaling laws", "query embeddings"],
    "search_phrase": "dense retrieval scaling laws"
}}
では、以下のユーザー入力に基づいてクエリを生成してください。
ユーザー入力:{question}
'''
class Query(BaseModel):
    keywords: list[str]
    search_phrase: str
def getQuery(state: State):
    if state["question"]:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはInformation Retrievalの専門家であり、アクセス可能なVespaサーバーからユーザーの役に立つ論文を週出するためのプロフェッショナルです。"},
                {"role": "user", "content": query_propmt.format(question=state["question"])},
            ],
            response_format=Query,
        )
        return {
            "keywords": completion.choices[0].message.parsed.keywords,
            "search_phrase": completion.choices[0].message.parsed.search_phrase
        }

    return {"message": "No user input provided"}


# embedding取得
def getEmbedding(state: State):
    input = state["search_phrase"]
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=input,
        encoding_format="float"
    )

    return {"phrase_embedding": response.data[0].embedding }


translation_prompt = """
あなたはInformation Retrievalの専門家です
次のリストは、Vespaの検索結果です。各エントリを以下の形式で日本語訳し、読みやすく整形してください：
- タイトル: 英文をそのまま表示
- タイトル(翻訳): 日本語訳。
- 著者: 英文をそのまま表示。
- URL: そのまま表示。
- 発行年: そのまま表示。
- 要約: 英文を日本語訳。与えられたquestionを参照し関連する部分を要約してください。
- 関連性スコア: 数値をそのまま表示してください

例：
---
1. タイトル: **[原文]**
   タイトル(翻訳): **[日本語訳]**
   著者: **[原文]**
   URL: **[原文]**
   発行年: **[原文]**
   要約: **[日本語要約]**
   関連性スコア: **[数値]**
---
以下に従い、すべてのエントリを翻訳してください。
question:
{question}

エントリー：
{search_result}
"""
def translation(state: State):
    if state["search_result"]:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはInformation Retrievalの専門家であり、アクセス可能なVespaサーバーからユーザーの役に立つ論文を週出するためのプロフェッショナルです。"},
                {"role": "user", "content": translation_prompt.format(
                    search_result=json.dumps(state["search_result"]),
                    question=state["question"]
                )},
            ]
        )
        return {
            "answer": completion.choices[0].message.content,
        }

    return {"message": "No user input provided"}
