#!/usr/bin/python
from mendeley import Mendeley
import pandas as pd
from catpal.Mendeley import logger, utils
import os
import json
import requests

config = None
# print(os.getcwd())
with open("./catpal/Mendeley/config.json", 'r') as fh:
    config = json.loads(fh.read())


# App Information
CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
CLIENT_NAME = config["CLIENT_NAME"]
REDIRECT_URI = "http://localhost:5000/oauth"

ACCESS_TOKEN = None

# Group Information
"""
groups = list(session.groups.iter())
group = groups[0]
print(group.__dict__)
"""


"""group_data = {
    'id': '316cff15-905a-3b4a-99e1-76e085570e8a',
    'name': 'COVID-19',
    'description': 'Papers related to the fight against COVID'
}"""

"""
group_data = {'name': 'TestMende',
              'description': 'For Testing',
              'id': '41b5c68e-eaff-3fc0-adf6-74444146428f'}
"""
# folder to synchronize with a nextcloud folder
# mendeley_folder = '/var/www/nextcloud/SMB/Mendeley2'
# temp_folder = '/var/www/nextcloud/SMB/MM'
mendeley_folder = 'C:/Users/EduardoFeria/Jupyter proyects/Mendeley2/Simple/MendeleyFolder'
temp_folder = 'C:/Users/EduardoFeria/Jupyter proyects/Mendeley2/Simple/TempFolder'

# Generated URL Information
dominio = 'https://cloud.cneuro.cu'

base_url = 'https://cloud.cneuro.cu/s/jS2gXc843y3WZ4e/download?path=%2F&files='
# base_url = 'This.is.a.test='

session = None


def authenticate(user_email, user_password):
    try:
        # These values should match the ones supplied when registering your application.
        mendeley = Mendeley(CLIENT_ID, redirect_uri=REDIRECT_URI)

        auth = mendeley.start_implicit_grant_flow()

        # The user needs to visit this URL, and log in to Mendeley2.
        login_url = auth.get_login_url()

        import requests

        res = requests.post(login_url, allow_redirects=False,
                            data={'username': user_email, 'password': user_password})

        auth_response = res.headers['Location']

        # After logging in, the user will be redirected to a URL, auth_response.
        global session
        session = auth.authenticate(auth_response)
        global ACCESS_TOKEN
        ACCESS_TOKEN = session.token['access_token']
    except Exception as exc:
        raise exc


def get_documents():
    """
    :return: Documents belonging to the logged user.
    """
    docs = list(session.documents.iter(view='all'))
    return docs


def get_documents_of_group(group_id):
    """
    :return: Documents belonging to the group.
    """
    docs = list(get_group(group_id).documents.iter(view='all'))
    return docs


def get_docs_from_group_api(group_id, access_token):
    """
    Retrieves the docs belonging to a group using Mendeleys API.
    :param group_id: the id of the group.
    :param access_token:
    :return: Documents, has a maximun of 500.
    """
    url = 'https://api.mendeley.com/documents'

    headers = {'Authorization': "Bearer '%s'" % access_token}
    params = {'group_id': group_id, 'view': 'all', 'limit': '500'}
    res = requests.get(url, headers=headers, params=params)
    return res


def get_documents_to_clasify():
    """
    retrieve new documents that has not been clasified yet
    :return:
    """
    unclasified_folder_name = config['UNCLASIFIED_FOLDER']
    folders = get_group_folders(group_data['id']).json()

    unclasified_folder = None
    for folder in folders:
        if 'parent_id' not in folder.keys() and folder['name'] == unclasified_folder_name:
            unclasified_folder = folder
            break

    if unclasified_folder is None:
        logger.log_error("Cannot find the %s folder in the group %s" % (unclasified_folder_name, group_data['name']))
        return

    docs = get_docs_from_folder(folder['id'])
    return docs


def add_doc_website(doc, website):
    """
    Adds a new Website to a Document.
    :param doc: Mendeley2 Document
    :param website: url where the document can be found
    :return:
    """
    websites = doc.websites
    if websites is None:
        websites = []
    for website_ in websites:
        if website_.startswith(dominio):
            websites.remove(website_)
    websites.append(website)
    doc.update(websites=websites)

    logger.log_info("Added website: %s to document %s" % (website, doc.title))


def update_metadata(doc):
    """
    Updates the Keywords and the Identifiers of a document by searching the catalogs
    :return:
    """
    keys = ['doi', 'arxiv', 'isbn', 'issn', 'pmid', 'scopus']
    visited = {key: False for key in keys}

    def review(doc):

        if doc.identifiers is None:
            doc.identifiers = {}

        identifier_changed = False

        # doc_keywords = doc.keywords

        for key in keys:
            if not visited[key]:

                cat = None

                if key in doc.identifiers.keys():
                    if key == 'doi':
                        try:
                            cat = session.catalog.by_identifier(doi=doc.identifiers['doi'], view='all')
                        except Exception:
                            print('catalog Error')
                        visited[key] = True
                    elif key == 'arxiv':
                        try:
                            cat = session.catalog.by_identifier(arxiv=doc.identifiers['arxiv'], view='all')
                        except Exception:
                            print('catalog Error')
                        visited[key] = True
                    elif key == 'isbn':
                        try:
                            cat = session.catalog.by_identifier(isbn=doc.identifiers['isbn'], view='all')
                        except Exception:
                            print('catalog Error')
                        visited[key] = True
                    elif key == 'issn':
                        try:
                            cat = session.catalog.by_identifier(issn=doc.identifiers['issn'], view='all')
                        except Exception:
                            print('catalog Error')
                        visited[key] = True
                    elif key == 'pmid':
                        try:
                            cat = session.catalog.by_identifier(pmid=doc.identifiers['pmid'], view='all')
                        except Exception:
                            print('catalog Error')
                        visited[key] = True
                    elif key == 'scopus':
                        try:
                            cat = session.catalog.by_identifier(scopus=doc.identifiers['scopus'], view='all')
                        except Exception:
                            print('catalog Error')
                        visited[key] = True

                    # Modifying the Identifiers
                    # print(key, 'catalog:', cat.identifiers)
                    if cat is None:
                        continue

                    # looking for a new indentifier
                    for catkey in cat.identifiers.keys():
                        if catkey in cat.identifiers.keys() and catkey not in doc.identifiers.keys():
                            doc.identifiers[catkey] = cat.identifiers[catkey]
                            identifier_changed = True

                    # modifying the Keywords
                    if cat.keywords is not None:
                        # print(cat.keywords)
                        if doc.keywords is None:
                            doc.keywords = []
                        doc.keywords = list(set(doc.keywords + cat.keywords))

                    # modifying abstract
                    if doc.abstract is None and cat.abstract is not None:
                        doc.abstract = cat.abstract
                        pass

                    # modifying source
                    # In Mendeley2 source => Journal
                    if doc.source is None and cat.source is not None:
                        doc.source = cat.source
                        pass

                    # modifying year
                    if doc.year is None and cat.year is not None:
                        doc.year = cat.year
                        pass

                    # modifying volume
                    if doc.volume is None and cat.volume is not None:
                        doc.volume = cat.volume
                        pass

                    # modifying issue
                    if doc.issue is None and cat.issue is not None:
                        doc.issue = cat.issue
                        pass

                    # modifying pages
                    if doc.pages is None and cat.pages is not None:
                        doc.pages = cat.pages
                        pass

        if identifier_changed:
            return review(doc)
        else:
            # if there is no new information to review then save the data
            doc.update(identifiers=doc.identifiers, keywords=doc.keywords, abstract=doc.abstract, source=doc.source,
                       year=doc.year, volume=doc.volume, issue=doc.issue, pages=doc.pages)
            return doc

    return review(doc)


def get_file_of_document(doc):
    doc_files = list(doc.files.iter())  # this is a mendeley resource
    return doc_files


def download_document(doc, dir):
    """

    :param doc:
    :param dir:
    :return:
    """
    if not (os.path.exists(dir) and os.path.isdir(dir)):
        logger.log_error("The specified directory %s is not valid." % dir)
        return

    files = get_file_of_document(doc)
    if len(files) > 0:
        file = files[0]
        file.download(dir)
        logger.log_info("The document %s was succesfully downloaded to %s." % (doc.title, dir))
    else:
        logger.log_warning("Could not find a source file for the document %s" % doc.title)


def get_groups():
    """
    Retrieves the groups in Mendeley2.
    :return:
    """
    return list(session.groups.iter())


def get_group(id):
    """
    :return: The Group that has the id.
    """
    return session.groups.get(id)


def get_local_folders(access_token=ACCESS_TOKEN):
    url = 'https://api.mendeley.com/folders'

    headers = {'Authorization': "Bearer '%s'" % access_token}
    params = {'limit': '200'}
    res = requests.get(url, headers=headers, params=params)
    folders = res.json()
    res_header = res.headers
    mendeley_count = int(res_header['Mendeley2-Count'])
    while mendeley_count > len(folders):
        link = res_header['link']
        next = utils.parse_link_headers(link)['next']
        res = requests.get(next, headers=headers)
        res_header = res.headers
        folders2 = res.json()
        folders.extend(folders2)
    return folders


def get_group_folders(group_id, access_token=ACCESS_TOKEN):
    """
    Retrieves folders belonging to a group.
    :param gropu_id: Group from where the folders will be retrieved
    :param access_token:
    :return: a list of dictionaries each containing the metadata of a folder.
    {'id', 'name', 'created', 'modified', 'group_id', 'parent_id': 'if it is not in root folder'}

    """
    url = 'https://api.mendeley.com/folders'

    headers = {'Authorization': "Bearer '%s'" % access_token}
    params = {'group_id': group_id, 'limit': '200'}
    res = requests.get(url, headers=headers, params=params)
    # number_of_folders
    return res


class Node:
    """
    Utility class for representing the file tree
    """
    def __init__(self, id, name, data, parent=None):
        self.id = id
        self.name = name
        self.data = data
        self.parent = parent
        self.children = []
        self.linked_parent = False


def folder_structure(group_id, group_name=None):
    """
    Builds a file tree given a list of folders and its parents.
    :param json_folder: list of dictionaries representing folders
    :return: A root Node containing the whole file structure
    """

    if group_name is None:
        groups = get_groups()
        for group in groups:
            if group_id == group.id:
                group_name = group.name

    json_folder = None
    if group_id is not None:
        json_folder = get_group_folders(group_id).json()
    else:
        json_folder = get_local_folders()
        group_id = 0
        group_name = 'Local'

    created = {fol['id']: False for fol in json_folder}
    # root = Node(id=group_data['id'], name=group_data['name'], data=None)
    root = Node(id=group_id, name=group_name, data=None)
    nodes_id = {fol['id']: Node(fol['id'], fol['name'], fol) for fol in json_folder}

    nodes_id[root.id] = root
    for node in nodes_id.values():
        if node.id != root.id:
            data = node.data
            if 'parent_id' in data.keys():
                node.parent = data['parent_id']
            else:
                node.parent = root.id

    def find_parent(node):
        """
        finds the parent of a node in a tree given by the root node.
        :param node:
        :return: the parent of the node
        """
        parents = []
        while node.id != root.id:
            parents.append(node.parent)
            node = nodes_id[node.parent]

        parents.reverse()
        node = nodes_id[parents.pop(0)]

        def find_node(node):
            if len(parents) == 0:
                return node
            children = node.children
            for child in children:
                if child.id == parents[0]:
                    parents.pop(0)
                    return find_node(child)

        return find_node(node)

    def create_node(fol):
        """
        Given a folder creates a node and link that node to its parent in the file tree
        :param fol:
        :return:
        """
        if created[fol['id']]:
            return

        if 'parent_id' in fol.keys():
            if created[fol['parent_id']]:
                node = Node(fol['id'], fol['name'], fol, fol['parent_id'])
                # nodes_id[fol['parent_id']].children.append(node)
                # print(find_parent(node))
                find_parent(node).children.append(node)
                created[node.id] = True
            # print('created "%s" child of "%s"' % (nodes_id[fol['id']].name, nodes_id[fol['parent_id']].name, ))

            else:
                # print('will create "%s"' % (nodes_id[fol['parent_id']].name, ))
                create_node(nodes_id[fol['parent_id']].data)
                node = Node(fol['id'], fol['name'], fol, fol['parent_id'])
                find_parent(node).children.append(node)
                created[node.id] = True
        else:
            # child of Root node
            root.children.append(Node(fol['id'], fol['name'], fol, parent=root.id))
            created[fol['id']] = True

    for fol in json_folder:
        create_node(fol)

    return root


def runNode(root, root_folder=None, show_files=False):
    """
    Walks over the file tree. Shows the folder tree
    :param root: root Node of the tree.
    :param root_folder: Folder for mirror the files.
    :param show_files:  Will show the files or not
    :return:
    """

    def _runNode(root, depth, root_folder=None, show_files=False):
        print("    " * depth, root.name)

        # show the files in folder or/and copy them to a folder
        if root.id != group_data['id']:
            if root_folder is not None or show_files is True:
                docs = get_docs_from_folder(root.id, ACCESS_TOKEN)
                if show_files is True and root_folder is not None:
                    for doc in docs:
                        print("    " * depth, '**', doc)
                        # Download the file

        elif root_folder is not None:
            root_folder = os.path.join(root_folder, root.name)

        for node in root.children:
            if root_folder is None:
                _runNode(node, depth + 1, show_files=show_files)
            else:
                _runNode(node, depth + 1, root_folder=os.path.join(root_folder, node.name), show_files=show_files)

    return _runNode(root, 0, root_folder=root_folder, show_files=show_files)


def get_file_hierarchy():
    # https: // dev.mendeley.com / code / core_quick_start_guides.html
    """
    List the child folders of a folder
    It is not possible to list the child folders of a folder directly using the python API. Your application should construct a tree model of folders by parsing the results of /folders and using the value of the parent_id member to establish a parent relationship.
    """
    group_id = get_group().id
    res = get_group_folders(group_id, ACCESS_TOKEN)
    root = folder_structure(res.json())
    # Show the file tree
    runNode(root, show_files=True)
    return root


def get_docs_from_folder(folder_id, access_token=ACCESS_TOKEN):
    """
    :param folder_id:
    :param access_token:
    :return: A paginated collection of IDs of the documents in the folder.
    """
    url = 'https://api.mendeley.com/folders/%s/documents' % folder_id

    headers = {'Authorization': "Bearer '%s'" % access_token}
    params = {'id': '%s' % folder_id, 'limit': '100'}
    res = requests.get(url, headers=headers, params=params).json()
    docs = []
    for doc_id in res:
        id = doc_id['id']
        doc = session.documents.get(id, view='all')
        docs.append(doc)
    return docs


def synchronize_mendeley():
    # docs = get_documents_of_group()
    docs = get_documents()

    # creating a CSV for file hyper-params
    csv_columns = ['title', 'id', 'tags', 'file_name', 'keywords', 'identifiers']
    csv_data = [] # np.array((len(docs), len(csv_columns)), dtype=np.str)
    json_data = []

    for idx, doc in enumerate(docs):
        # Updating the metadata
        doc = update_metadata(doc)

        # printProgressBar(idx + 1, len(docs))

        new_file_name = doc.id + doc.title
        # remove bad characters from file name
        for i in '<>:"/\\|?*':
            new_file_name = new_file_name.replace(i, '')
        new_file_name = new_file_name.replace('\n', '_')
        new_file_name = new_file_name.replace('\r', '_')
        new_file_name = new_file_name.replace(' ', '_')

        file = None
        files = get_file_of_document(doc)

        if len(files) > 0:
            file = files[0]
            extension = os.path.splitext(file.file_name)[1]
            if len(mendeley_folder) + len(new_file_name) + len(extension) > 250:
                new_file_name = new_file_name[0:250 - len(mendeley_folder) - len(extension)]
            new_file_name = new_file_name + extension
        else:
            logger.log_warning("Could not find a source file for the document %s in Mendeley2's Database." % doc.title)
            continue

        if new_file_name not in os.listdir(mendeley_folder):
            # clear temp folder
            for file in os.listdir(temp_folder):
                os.remove(os.path.join(temp_folder, file))
            # copy the doc to the folder
            files[0].download(temp_folder)
            logger.log_info("The document %s was succesfully downloaded to %s." % (doc.title, dir))
            c = os.listdir(temp_folder)
            if len(c) == 0:
                logger.log_error("There is no file in %s" % temp_folder)
                continue
            # get the file
            file_name = os.path.join(temp_folder, c[0])
            try:
                os.rename(file_name, os.path.join(mendeley_folder, new_file_name))
                logger.log_info("Saved file %s." % os.path.join(mendeley_folder, new_file_name))
                doc_url = base_url + new_file_name
                # print(doc_url)
                add_doc_website(doc, doc_url)
            except OSError:
                logger.log_error("OS Error. Could not copy the file %s." % new_file_name)
                continue
            except:
                logger.log_error("Error copying the file %s." % new_file_name)
                continue
        else:
            doc_url = base_url + new_file_name
            add_doc_website(doc, doc_url)
            
        # add the data to CSV
        # csv_data[idx][:] = np.array([doc.title, doc.id, doc.tags, new_file_name])
        csv_data.append([doc.title, doc.id, doc.tags, new_file_name, str(doc.keywords), str(doc.identifiers)])
        json_data.append({'title': doc.title, 'id': doc.id, 'tags': doc.tags, 'file_name': new_file_name,
                          'keywords': doc.keywords, 'identifiers': doc.identifiers})

    csv_ = pd.DataFrame(data=csv_data, columns=csv_columns)
    csv_.to_csv(path_or_buf=os.path.join(mendeley_folder, '_data.csv'))
    with open(os.path.join(mendeley_folder, '_data.json'), 'w') as outfile:
        json.dump(json_data, outfile)


def create_folder(access_token=ACCESS_TOKEN):
    url = 'https://api.mendeley.com/folders/'

    headers = {
        'Authorization': "Bearer '%s'" % access_token,
        'Accept': 'application/vnd.mendeley-folder.1+json',
        'Content-Type': 'application/vnd.mendeley-folder.1+json',
    }
    params = {
        'name': 'newfolderapicreated',
        "group_id": group_data['id']
    }

    res = requests.post(url, headers=headers, data=params)
    return res.json()


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = 'O', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    iteration_label = "%d/%d" % (iteration, total)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    # print('\r%s |%s| %s %s%% %s' % (prefix, bar, iteration_label, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def test():
    sess = authenticate()
    docs = get_documents_of_group()
    doc = docs[0]
    files = get_file_of_document(doc)

    download_document(doc, mendeley_folder)


def test2():
    """
    Testing retrive metadata from catalog and update the document.
    :return:
    """
    sess = authenticate()
    docs = get_documents_of_group()
    for doc in docs:
        update_metadata(doc)


def test3():
    """
    testing moving docs to a specific folder.
    :return:
    """
    folder_res = get_group_folders(group_data['id'], ACCESS_TOKEN).json()
    name_id = {fol['name']: fol['id'] for fol in folder_res}

    folder_id = name_id['Ian Googfellow']
    doc_id = get_documents_of_group()[3].id
    url = 'https://api.mendeley.com/folders/%s/documents' % folder_id

    headers = {'Authorization': "Bearer '%s'" % ACCESS_TOKEN}
    params = {'id': '%s' % doc_id}
    # params = '${"id": "%s"}' % doc_id
    access_token2 = session.token['access_token']
    # params2 = {'id': '%s' % doc_id, 'Authorization': "Bearer '%s'" % access_token}
    res = requests.post(url, headers=headers, data=params)
    print(res)
    return res.json()
    pass


def test4():
    create_folder()
    pass


def test5():
    get_documents_to_clasify()


def test6():
    res = get_local_folders().json()
    pass


if __name__ == '__main__':
    # synchronize_mendeley()
    # get_file_hierarchy()
    # test2()
    # test3()
    test4()
    # test5()
    # test6()
    pass
