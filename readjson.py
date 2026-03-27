import json
import sys
from collections import defaultdict


def print_duplicate_hash_venues(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.sort(key=lambda item: (item.get("hash"), item.get("type")))
    last = 42
    last_venue = ""
    last_type = ""
    print("conference,journal")
    for idx, item in enumerate(data):
        H = item.get("hash")
        this_venue = item.get("venue")
        this_type = item["type"]
        if H == last:
            if this_type == "journal" and last_type == "conference":
                print(f'"{last_venue}","{this_venue}"')
        last = H
        last_venue = this_venue
        last_type = this_type


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} data.json")
        sys.exit(1)

    print_duplicate_hash_venues(sys.argv[1])
