import argparse
from aggregator import fetch_threat_data
from llm_analysis import analyze_with_llm
from output import save_output

def main():
    parser = argparse.ArgumentParser(description="Threat Intelligence Aggregator CLI")

    parser.add_argument(
        "--source",
        type=str,
        nargs='+',
        required=True,
        help="One or more threat intel sources (e.g., abuseipdb otx virustotal)"
    )
    parser.add_argument(
        "--llm",
        type=str,
        default="gpt-4",
        help="LLM model to use (e.g., gpt-3.5-turbo, gpt-4)"
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="json",
        help="Output format (json, csv, md)"
    )
    parser.add_argument(
        "--llm-off",
        action="store_true",
        help="Disable LLM enrichment"
    )

    args = parser.parse_args()
    all_data = []

    for source in args.source:
        data = fetch_threat_data(source)
        if data:
            all_data.extend(data)

    if not args.llm_off:
        enriched_data = analyze_with_llm(all_data, args.llm)
        save_output(enriched_data, args.output_format)
    else:
        save_output(all_data, args.output_format)

if __name__ == "__main__":
    main()
