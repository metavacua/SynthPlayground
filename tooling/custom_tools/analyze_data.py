import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Analyze raw data.")
    parser.add_argument("--raw_data", required=True, help="The raw data to analyze.")
    args = parser.parse_args()

    analysis_report = f"Analysis of the data: {args.raw_data.upper()}"
    print(json.dumps({"analysis_report": analysis_report}))


if __name__ == "__main__":
    main()
