from typing_extensions import TypedDict

# Stateを宣言
class State(TypedDict):
    abstract: str
    embedding: list[float]
