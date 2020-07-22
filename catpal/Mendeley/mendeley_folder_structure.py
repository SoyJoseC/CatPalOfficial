import mendeley_driver as md
import json
import utils


def get_folder_structure_as_json(group_id=None, group_name=None):
    root = md.folder_structure(group_id=group_id, group_name=group_name)

    def _get_folder_tree(node):
        if len(node.children) == 0:
            return {node.name: None}
        else:
            tree_dict = {}
            for child in node.children:
                child_tree = _get_folder_tree(child)
                tree_dict.update(child_tree)
            return {node.name: tree_dict}

    return _get_folder_tree(root)


def get_full_folder_structure():
    groups = md.get_groups()
    files = {}
    # tree = get_folder_structure_as_json()
    # files.update(tree)
    for group in groups:
        group_id = group.id
        group_name = group.name
        tree = get_folder_structure_as_json(group_id=group_id, group_name=group_name)
        files.update(tree)
    return files


def save_to_json(dict):
    with open('file_structure_%s_%s.json' % (md.config['USER_EMAIL'], utils.get_current_datetime()), 'w') as json_file:
        json.dump(dict, json_file)
    pass


def test1():
    """
    get_folder_structure_as_json with no parameters gets the folder structure of the local mendeley.
    :return:
    """
    tree = get_folder_structure_as_json()
    save_to_json(tree)
    pass


def test2():
    files = get_full_folder_structure()
    save_to_json(files)
    pass


def test3():
    folders = md.get_local_folders()
    pass


if __name__ == '__main__':
    test3()
