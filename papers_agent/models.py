from typing_extensions import TypedDict, Optional

# Stateを宣言
class State(TypedDict):
    message: Optional[str] = None
    question: str
    keywords: list[str]
    search_phrase: str
    phrase_embedding: list[float]
    search_result: list[dict]
    answer: str
