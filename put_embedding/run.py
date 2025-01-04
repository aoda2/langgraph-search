import json
import os
from tqdm import tqdm
from graphs import getGraph

# data jsonl に embedding 追加
def process_jsonl(input_file, output_file):
    graph = getGraph()
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in tqdm(infile):
            try:
                data = json.loads(line)
                abstract = data.get("fields", {}).get("abstract")

                if abstract:
                  result = graph.invoke({"abstract": abstract})
                  embedding = result.get("embedding")
                  if embedding:
                      data["fields"]["embedding"] = embedding
                
                outfile.write(json.dumps(data) + '\n')

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}, Skipping line: {line}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}, Skipping line: {line}")

# Example usage:
input_file = "../papers/ext/data.jsonl"
output_file = "../papers/ext/data-emb.jsonl" 


process_jsonl(input_file, output_file)

print(f"Processing complete. Output written to {output_file}")
