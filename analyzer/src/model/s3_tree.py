import logging
import boto3

from src.model.s3_folder import S3Folder


def tree(bucket, dir_path: str = '', tree_depth: int = None, margin: int = 1000000):
    """
    Generates a tree structure of objects in the S3 bucket.

    Args:
        bucket (str): The name of the S3 bucket.
        dir_path (str, optional): The directory path to start the tree from. Defaults to ''.
        tree_depth (int, optional): The depth of the tree. Defaults to None.
        margin (int, optional): The maximum number of files to process. Defaults to 1000000.

    Returns:
        list: A list of S3Folder objects representing the tree structure.

    """
    if not dir_path:
        dir_path = ''

    objects = boto3.resource('s3').Bucket(
        bucket).objects.filter(Prefix=dir_path)

    info = []
    for idx, obj in enumerate(objects):
        info.append({
            "key": obj.key,
            "size": obj.size
        })
        if idx > margin:
            logging.warning("Too many files in the bucket")
            raise TooManyFilesException(n_files=len(info), margin=margin)

    logging.info("There are %i files in the bucket", len(info))

    output_tree = []
    for elem in info:
        if elem["size"] > 0:
            folders = "/".join(elem["key"].split('/')[:-1])
            item = S3Folder(folders, elem["size"], tree_depth=tree_depth)
            is_new = True
            for tree_item in output_tree:
                if item == tree_item:
                    sum_folder = tree_item + item
                    output_tree.remove(tree_item)
                    output_tree.append(sum_folder)
                    is_new = False
                    break
            if is_new:
                output_tree.append(item)
    return output_tree


class TooManyFilesException(Exception):
    """
    Exception raised when the number of files in an S3 bucket exceeds a specified margin.

    Attributes:
        n_files (int): The number of files in the S3 bucket.
        margin (int): The maximum allowed number of files before the exception is raised.
    """

    def __init__(self, n_files, margin):
        self.n_files = n_files
        self.margin = margin
        super().__init__(
            "There are too many files in the bucket. Number of files: {n_files}, margin: {margin}")
