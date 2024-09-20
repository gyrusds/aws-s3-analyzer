import json
import logging
import argparse
from dotenv import load_dotenv
from src.methods.analyzer import Analyzer, AnalyzerException, AlreadyAnalyzedException

OUTPUT_FOLDER = "../backend/output"


def main(include_buckets: str = "", exclude_buckets: str = ""):
    """
    Main function to analyze AWS S3 buckets.

    This function initializes the Analyzer, loads the current summary from a JSON file,
    and processes the list of all buckets. It filters the buckets based on the include
    and exclude lists, performs analysis on each bucket, and updates the summary.

    Args:
        include_buckets (str): Comma-separated list of bucket names to include in the analysis.
        exclude_buckets (str): Comma-separated list of bucket names to exclude from the analysis.

    Raises:
        FileNotFoundError: If the summary JSON file is not found.
        AlreadyAnalyzedException: If a bucket has already been analyzed.
        AnalyzerException: If an error occurs during the analysis of a bucket.

    Returns:
        None
    """
    analyzer = Analyzer(OUTPUT_FOLDER)
    all_buckets = analyzer.all_buckets()

    in_buckets = include_buckets.split(",") if include_buckets else []
    ex_buckets = exclude_buckets.split(",") if exclude_buckets else []

    try:
        with open(f"{OUTPUT_FOLDER}/summary.json", encoding="utf-8") as f:
            current_summary = json.load(f)
        logging.info(
            "Loaded summary from %s/summary.json. There are %i buckets", OUTPUT_FOLDER, len(current_summary))
    except FileNotFoundError:
        current_summary = []

    if in_buckets:
        all_buckets = [
            bucket for bucket in all_buckets if bucket in in_buckets]

    summary = []
    logging.info("Starting analysis for %i buckets", len(all_buckets))
    for bucket in all_buckets:
        if bucket in ex_buckets:
            summary.append({
                "bucket_name": bucket,
                "size": 0,
                "status": "excluded"
            })
        elif bucket in [b["bucket_name"] for b in current_summary]:
            logging.info("Skipping %s as it has already been analyzed", bucket)
            summary.extend(
                [b for b in current_summary if b["bucket_name"] == bucket])
        else:
            try:
                size = analyzer.analyze(bucket)
                logging.info(
                    "Analysis for %s completed. Size: %i", bucket, size)
                summary.append({
                    "bucket_name": bucket,
                    "size": size,
                    "status": "done"
                })
            except AlreadyAnalyzedException as ex:
                logging.info(str(ex))
                summary.append({
                    "bucket_name": bucket,
                    "size": ex.size,
                    "status": "done"
                })
            except AnalyzerException as ex:
                logging.error("Analysis for %s failed: %s", bucket, ex)
                summary.append({
                    "bucket_name": bucket,
                    "size": 0,
                    "status": "failed",
                    "error": str(ex)
                })
        with open(f"{OUTPUT_FOLDER}/summary.json", 'w', encoding="utf-8") as f:
            f.write(json.dumps(summary, indent=4))


if __name__ == '__main__':

    load_dotenv()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        )
    parser = argparse.ArgumentParser(description='AWS S3 Analyzer')
    parser.add_argument('--include-buckets', type=str, default='',
                        help='Comma-separated list of buckets to include')
    parser.add_argument('--exclude-buckets', type=str, default='',
                        help='Comma-separated list of buckets to exclude')
    args = parser.parse_args()

    main(args.include_buckets, args.exclude_buckets)
    main()
