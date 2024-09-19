import json
import logging
import argparse
from dotenv import load_dotenv
from methods.analyzer import Analyzer, AnalyzerException, AlreadyAnalyzedException

OUTPUT_FOLDER = "../backend/output"


def main(include_buckets: str = "", exclude_buckets: str = ""):
    analyzer = Analyzer(OUTPUT_FOLDER)
    all_buckets = analyzer.all_buckets()

    in_buckets = include_buckets.split(",") if include_buckets else []
    ex_buckets = exclude_buckets.split(",") if exclude_buckets else []

    try:
        with open(f"{OUTPUT_FOLDER}/summary.json") as f:
            current_summary = json.load(f)
        logging.info(
            f"Loaded summary from {OUTPUT_FOLDER}/summary.json. There are {len(current_summary)} buckets")
    except FileNotFoundError:
        current_summary = []

    if in_buckets:
        all_buckets = [
            bucket for bucket in all_buckets if bucket in in_buckets]

    summary = []
    logging.info(f"Starting analysis for {len(all_buckets)} buckets")
    for bucket in all_buckets:
        if bucket in ex_buckets:
            summary.append({
                "bucket_name": bucket,
                "size": 0,
                "status": "excluded"
            })
        elif bucket in [b["bucket_name"] for b in current_summary]:
            logging.info(f"Skipping {bucket} as it has already been analyzed")
            summary.extend(
                [b for b in current_summary if b["bucket_name"] == bucket])
        else:
            try:
                size = analyzer.analyze(bucket)
                logging.info(f"Analysis for {bucket} completed. Size: {size}")
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
                logging.error(f"Analysis for {bucket} failed: {ex}")
                summary.append({
                    "bucket_name": bucket,
                    "size": 0,
                    "status": "failed",
                    "error": str(ex)
                })
        with open(f"{OUTPUT_FOLDER}/summary.json", 'w') as f:
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
