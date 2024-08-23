import json
import requests
import sys
import convert


def getData(query: str, limit: str, filepath: str):
    print(f"\n\nGetting data from Core, searched for: {query}, limited to {limit} files, saving to {filepath}\n")
    limit = int(limit) + 2
    r = requests.get(f"https://api.core.ac.uk/v3/search/works/?q={query}&limit={limit}")
    results = r.json()["results"]
    for entry in results:
        #del entry["abstract"], entry["fullText"]
        del entry["fullText"]
    print(f"Data fetched succesfully, response time: {r.elapsed.total_seconds()}")
    #print(json.dumps(results, indent = 2))
    return results


if __name__ == "__main__":
    jsonObj = getData(sys.argv[1], sys.argv[2], sys.argv[3])
    convert.converter(sys.argv[3], jsonObj)
