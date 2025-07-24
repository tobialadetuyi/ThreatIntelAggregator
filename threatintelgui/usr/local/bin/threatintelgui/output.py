import json
import csv

def save_output(data, output_format):
    if output_format == "json":
        with open("output.json", "w") as f:
            json.dump(data, f, indent=2)
        print("[Output] Saved to output.json")
    elif output_format == "csv":
        keys = data[0].keys()
        with open("output.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print("[Output] Saved to output.csv")
    else:
        print("[Output] Unsupported format")
