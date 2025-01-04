from openai import OpenAI
from models import State

client = OpenAI()

# embedding取得
def getEmbedding(state: State):
    input = state["abstract"]
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=input,
        encoding_format="float"
    )

    return {"embedding" :response.data[0].embedding }
