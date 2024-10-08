import os
import logging
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from src.model.s3_tree import tree, TooManyFilesException


class Analyzer():
    """
    This class provides methods for analyzing S3 buckets and generating reports.

        output_folder (str): The path to the output folder where the reports will be saved.

    Attributes:
        output_folder (str): The path to the output folder where the reports will be saved.

    Methods:
        all_buckets(): Retrieves the names of all S3 buckets.
        analyze(bucket: str, overwrite: bool = False): Analyzes the specified S3 bucket and generates a JSON report.
    """

    def __init__(self, output_folder: str):
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def all_buckets(self):
        """
        Retrieves the names of all S3 buckets.

        Returns:
            list: A list of bucket names.

        """
        s3 = boto3.resource('s3')
        bucket_names = [bucket.name for bucket in s3.buckets.all()]
        return bucket_names

    def analyze(self, bucket: str, overwrite: bool = False):
        """
        Analyzes the specified S3 bucket and generates a JSON report.

        Args:
            bucket (str): The name of the S3 bucket to analyze.
            overwrite (bool): If True, overwrites the existing report for the bucket.

        Returns:
            int: The total size of the files in the S3 bucket.

        Raises:
            ClientError: If there is an error while processing the S3 bucket.
        """
        output_file = f"{self.output_folder}/{bucket}.json"

        if not overwrite and os.path.exists(output_file):
            with open(output_file, encoding='utf-8') as f:
                data = json.load(f)
            raise AlreadyAnalyzedException(bucket, data["size"])
        try:
            logging.info("Processing bucket: %s", bucket)
            s3_folders = tree(
                bucket=bucket,
                tree_depth=os.environ.get("TREE_DEPTH", 4)
            )

            data = {
                "bucket_name": bucket,
                "size": sum(f.size for f in s3_folders),
                "datetime": f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                "folders": [f.json_encoder() for f in s3_folders]
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, indent=4))

            return data["size"]
        except (ClientError, TooManyFilesException) as ex:
            logging.error(ex)
            raise AnalyzerException(str(ex), bucket) from ex


class AnalyzerException(Exception):
    """
    Custom exception class for the Analyzer module.

    This exception is raised for errors specific to the Analyzer's operations.

    Attributes:
        None

    Methods:
        None
    """

    def __init__(self, message, bucket):
        self.message = message
        self.bucket = bucket
        super().__init__(self.message)


class AlreadyAnalyzedException(Exception):
    """
    Exception raised when an attempt is made to analyze an already analyzed S3 bucket.

    Attributes:
        bucket (str): The name of the S3 bucket.
        size (int): The size of the S3 bucket.
        message (str): Explanation of the error.
    """

    def __init__(self, bucket, size):
        self.bucket = bucket
        self.size = size
        self.message = f"Bucket {bucket} already analyzed. Skipping."
        super().__init__(self.message)
