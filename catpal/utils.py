import uuid

def tree_to_list(root):
    """Recursively converts a tree into a list of idented strings."""
    list = []
    node_to_list(root, 0, list)

    return list


def node_to_list(node, depth, list):
    identation = '_._._.'
    list.append({'str':(identation * depth) + node.name, 'category': node})
    # run for each child
    for child in node.childs():
        node_to_list(child, depth+1, list)


def generate_hash():
    return str(uuid.uuid4())

