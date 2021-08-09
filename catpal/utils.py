import uuid
import os, json
from cryptography.fernet import Fernet

config = None
# print(os.getcwd())
with open("./catpal/Mendeley/config.json", 'r') as fh:
    config = json.loads(fh.read())
#todo
key = config["ENC_KEY"].encode('utf-8')
fernet = Fernet(key)

def tree_to_list(root):
    """Recursively converts a tree into a list of idented strings."""
    list = []
    node_to_list(root, 0, list)

    return list


def node_to_list(node, depth, list):
    #identation = '_._._.'
    identation = '__'
    list.append({'str':(identation * depth)+ "\\" + node.name, 'category': node})
    # run for each child
    for child in node.childs():
        node_to_list(child, depth+1, list)


def generate_hash():
    return str(uuid.uuid4())

def decryption(element):
    return fernet.decrypt(element.lstrip("b'").rstrip("'").encode('utf-8'))

def encytption(element):
    return fernet.encrypt(element.encode('utf-8'))



