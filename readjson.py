import json
import sys
from collections import defaultdict


def print_duplicate_hash_venues(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.sort(key=lambda item: item.get("hash"))
    last = 42
    last_venue = ""
    print("conference,journal")
    for idx, item in enumerate(sorted_data):
        H = item.get("hash")
        if H == last:
            this_venue = item.get("venue")
            print(f'"{last_venue}","{this_venue}"')
        last = H
        last_venue = this_venue

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} data.json")
        sys.exit(1)

    print_duplicate_hash_venues(sys.argv[1])
