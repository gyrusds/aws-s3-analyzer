import logging
import random


class S3Folder():
    """
    Represents a folder in an S3 bucket.

    Attributes:
    - name (str): The name of the folder.
    - size (int): The size of the folder in bytes.
    - children (list): The list of child folders or files contained within the folder.
    - tree_depth (int): The depth of the tree. Default is None.

    Methods:
    - __init__(name: str, size: int = 0, children: list = []): Initializes a new instance of the S3Folder class.
    - add_child(child): Adds a child folder or file to the folder.
    - __str__(indent: str = ''): Returns a string representation of the folder and its children.
    - __repr__(): Returns a string representation of the folder.
    - __add__(other): Adds another S3Folder to the current folder.
    - __eq__(other): Checks if the folder is equal to another folder or a string.
    - __ne__(other): Checks if the folder is not equal to another folder.
    - __hash__(): Returns the hash value of the folder.
    - __iter__(): Returns an iterator that iterates over the folder and its children.
    """

    def __init__(self, name: str, size: int = 0, children: list = None, tree_depth: int = None):
        self.logger = logging.getLogger(__name__)
        path = name.split('/')
        self.name = path[0]
        self.size = size
        if children:
            self.children = children.copy()
        else:
            self.children = []
        if len(path) > 1:
            # No limit on tree depth
            if tree_depth is None:
                self.children.append(S3Folder('/'.join(path[1:]), size))
            # Limit tree depth
            elif tree_depth > 0:
                self.children.append(
                    S3Folder('/'.join(path[1:]), size, tree_depth=tree_depth - 1))

    def add_child(self, child):
        """
        Adds a child node to the current S3 folder.

        Args:
            child: The child node to be added to the current folder.
        """
        self.children.append(child)

    def __str__(self, indent: str = ''):
        if len(self.children) > 0:
            children = []
            for child in self.children:
                children.append(indent + child.__str__(indent + '  '))
            str_children = '\n'.join(children)
        else:
            str_children = ''
        return f"{indent}{self.name} - {self.size} bytes \n{str_children}"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, S3Folder):
            for child in other.children:
                is_new = True
                for self_child in self.children:
                    if child == self_child:
                        sum_child = self_child + child
                        self.children.remove(self_child)
                        self.children.append(sum_child)
                        is_new = False
                        break
                if is_new:
                    self.children.append(child)
            return S3Folder(self.name, self.size + other.size, self.children)
        return self

    def __eq__(self, other):
        if isinstance(other, S3Folder):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    def __ne__(self, other):
        return self.name != other.name

    def __hash__(self):
        return hash(self.name)

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child

    def json_encoder(self):
        """
        Encodes the S3Folder object into a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing the following keys:
                - 'id' (int): A randomly generated integer between 1 and 100000000.
                - 'name' (str): The name of the S3 folder.
                - 'size' (int): The size of the S3 folder.
                - 'children' (list): A list of dictionaries, each representing a child S3Folder object, 
                  encoded using the same json_encoder method.
        """
        return {
            'id': random.randint(1, 100000000),
            'name': self.name,
            'size': self.size,
            'children': [child.json_encoder() for child in self.children]
        }
