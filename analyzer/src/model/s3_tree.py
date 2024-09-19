import boto3
import logging

from model.s3_folder import S3Folder


class S3Tree():
    """
    Represents a tree structure of objects in an S3 bucket.

    Args:
        bucket (str): The name of the S3 bucket.

    Attributes:
        logger (logging.Logger): The logger object for logging messages.
        bucket (boto3.resources.factory.s3.Bucket): The S3 bucket object.

    """

    def __init__(self, bucket: str):
        self.logger = logging.getLogger(__name__)
        self.bucket = bucket

    def tree(self, dir_path: str = '', tree_depth: int = None, margin: int = 1000000):
        """
        Generates a tree structure of objects in the S3 bucket.

        Args:
            dir_path (str, optional): The directory path to start the tree from. Defaults to ''.
            tree_depth (int, optional): The depth of the tree. Defaults to None.

        Returns:
            list: A list of S3Folder objects representing the tree structure.

        """
        if not dir_path:
            dir_path = ''

        s3_Bucket = boto3.resource('s3').Bucket(self.bucket)
        objects = s3_Bucket.objects.filter(Prefix=dir_path)

        info = []
        for idx, obj in enumerate(objects):
            info.append({
                "key": obj.key,
                "size": obj.size
            })
            if idx > margin:
                logging.warning("Too many files in the bucket")
                raise TooManyFilesException(n_files=len(info), margin=margin)

        logging.info(f"There are {len(info)} files in the bucket")

        tree = []
        for elem in info:
            if elem["size"] > 0:
                folders = "/".join(elem["key"].split('/')[:-1])
                item = S3Folder(folders, elem["size"], tree_depth=tree_depth)
                is_new = True
                for tree_item in tree:
                    if item == tree_item:
                        sum_folder = tree_item + item
                        tree.remove(tree_item)
                        tree.append(sum_folder)
                        is_new = False
                        break
                if is_new:
                    tree.append(item)
        return tree


class TooManyFilesException(Exception):

    def __init__(self, n_files, margin):
        self.n_files = n_files
        self.margin = margin
        super().__init__(
            "There are too many files in the bucket. Number of files: {n_files}, margin: {margin}")
