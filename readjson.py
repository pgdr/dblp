import json
import sys
from collections import defaultdict


def print_duplicate_hash_venues(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sorted_data = sorted(data, key=lambda item: item.get("hash"))
    del data
    last = 42
    last_venue = ""
    for idx, item in enumerate(sorted_data):
        if item.get("hash") == last:
            print(
                item.get("title"),
                "\n\t",
                last_venue,
                "--->",
                item.get("venue"),
            )
        last = item.get("hash")
        last_venue = item.get("venue")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} data.json")
        sys.exit(1)

    print_duplicate_hash_venues(sys.argv[1])
