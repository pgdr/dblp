#!/usr/bin/env python3
import csv
import sys
from collections import defaultdict
import math


def R(x, r=1):
    return math.ceil(100 * x)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    rows = []
    totals = defaultdict(int)

    # Read rows and accumulate total count per conference
    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["count"] = int(row["count"])
            rows.append(row)
            totals[row["conf"]] += row["count"]

    # Write output with normalized = count / total_count_for_conf
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["count", "conf", "journal", "normalized"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            total = totals[row["conf"]]
            normalized = R(row["count"] / total) if total else 0.0
            writer.writerow(
                {
                    "count": row["count"],
                    "conf": row["conf"],
                    "journal": row["journal"],
                    "normalized": normalized,
                }
            )


if __name__ == "__main__":
    main()
