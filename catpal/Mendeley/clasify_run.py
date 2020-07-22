from catpal.Mendeley import mendeley_driver as md
import pandas as pd
import numpy as np
from catpal.Mendeley import utils
import json

to_clasify_sumary = 'to_clasify'
HEADER_ROWS = 'HEADER_ROWS = '
DOC_COLUMNS = ['id', 'title', 'tags']

CATEGORIES = {
    'modelación': {
        'rebrote y meseta': None,
        'modelos': None,
        'pronósticos': None,
        'progresión': None
    },
    'equipos y dispositivos médicos': {
        'respiradores': None,
        'mascaras': None,
        'ventiladores': None
    },
    'diagnostico': {
        'Diagnóstico diferencial': None,
        'Kits': None,
        'Biomarcadores': None
        },
    'virología': None,
    'terapias no farmacológicas': {
        'terapias': None,
        'intervenciones': None
    },
    'patogenesis': None,
    'terapias farmacológicas': {
        'Vacunas': None,
        'Protocolos': None
    },
    'ensayos clínicos': {
        'Estudios de evaluación': None,
        'Resultados de las terapias': None
    },
    'inmunología': {
        'Inmunidad': {
            'Seroprevalencia': None,
            'Respuesta Inmune': None,
            'Tipos': None
        },
        'Inmunoterapia ': {
            'Eritropoyetina': None,
            'Inhibidores angiotensina (ACE 2)': None,
            'Plasma': None,
            'Antagonistas TNF o IL': None,
            'Antagonistas interleuquina-6': None
        },
        'Tormenta de citoquinas': {
            'Productos asociados': None
        }
    },
    'epidemiología': None,
    'revisiones y metanálisis': None
}


def headers(doc_columns, categories):
    """
    Creates the headers for the document data.
    :param doc_columns: columns about the document to show ex: ['id', 'title']
    :param categories: categories tree like ex: {'cat1': None, 'cat2': {'cat3': None, 'cat4': None},
    'cat5': {'cat6': {'cat7': None}}}
    :return: an array containing the headers:
    the columns of document data and the tree of categories.
    """

    nodes = {}
    jumps = []
    root = (0, 0)

    def create_tree(parent, childs, last):
        """
        recursively creates a tree by giving the positions of each node
        in a matrix.
        :param parent:
        :param childs:
        :param last: position for the new node.
        :return:
        """
        nodes[parent] = last
        # last = (last[0] + 1, last[1] + 1)
        if childs is None:
            # next sibling
            return last[0], last[1] + 1

        if childs is not None:
            child_last = (last[0] + 1, last[1] + 1)
            jumps.append((last[0] + 1, last[1]))
            for child in childs.keys():
                child_last = create_tree(child, childs[child], child_last)

            return last[0], child_last[1]

    # creates the headers for the categories
    create_tree('root', categories, (0, 0))
    # print(nodes)

    max_x = 0
    max_y = 0
    for node in nodes.values():
        max_x = max(max_x, node[1])
        max_y = max(max_y, node[0])
    max_x += 1
    max_y += 1

    arr = ['']*max_y
    for i in range(len(arr)):
        arr[i] = ['']*(max_x + len(doc_columns))

    for name, posic in nodes.items():
        arr[posic[0]][posic[1] + len(doc_columns)] = name

    for jump in jumps:
        arr[jump[0]][jump[1] + len(doc_columns)] = '↘'

    arr[-1][0:len(doc_columns)] = doc_columns

    # print('headers:\n', arr)

    return arr


def generate_excel_to_clasify():
    headers_ = headers(DOC_COLUMNS, CATEGORIES)
    headers_[0][0] = HEADER_ROWS + str(len(headers_))

    docs = md.get_documents_to_clasify()

    # update metadata
    for i, doc in enumerate(docs):
        docs[i] = md.update_metadata(doc)

    data_rows = []

    for doc in docs:
        row = [''] * len(headers_[-1])
        row[0] = doc.id
        row[1] = doc.title

        data_rows.append(row)
    headers_.extend(data_rows)

    data = pd.DataFrame(data=headers_, columns=None)
    data.to_excel(to_clasify_sumary + utils.get_current_datetime() + '.xls', na_rep='')


def load_excel_to_clasify():
    data = pd.read_excel('to_clasify09-07-2020_11-35-13.xls').values
    header_rows = data[0][1]
    header_rows = int(header_rows[len(HEADER_ROWS):])
    data = np.delete(data, 0, axis=1)

    headers = [''] * data.shape[1]
    headers[0:len(DOC_COLUMNS)] = DOC_COLUMNS

    for c in range(len(DOC_COLUMNS), data.shape[1]):
        for j in range(header_rows):
            val = data[j][c]
            if not pd.isna(val) and not val == '↘':
                data[header_rows-1][c] = data[j][c] + '*'
                headers[c] = data[j][c]
                break
    data = pd.DataFrame(data=data[header_rows:], columns=headers)

    # print(headers)

    for i in range(data.shape[0]):
        doc = data.iloc[i]
        clasif = [classe for classe in headers[len(DOC_COLUMNS):] if data[classe][i] == 'X']
        print(doc['title'])
        print(clasif)
        print()


def generate_documents_json():
    docs = md.get_documents_to_clasify()
    _docs = []
    for doc in docs:
        _docs.append({
            'id': doc.id,
            'title': doc.title,
            'abstract': doc.abstract,
        })
    with open('%s_%s.json' % (to_clasify_sumary, utils.get_current_datetime()), 'w') as fp:
        json.dump(_docs, fp)


def generate_categories_visualization_values():

    def gen_node_values(node, depth, children, list_nodes):
        node_val = (node, depth)
        list_nodes.append(node_val)
        if children is not None:
            for child in children.keys():
                list_nodes = gen_node_values(child, depth + 1, children[child], list_nodes)
        return list_nodes

    list_nodes = gen_node_values('categories', 0, CATEGORIES, [])
    return list_nodes


def print_categories_visualization(list_nodes):
    for node in list_nodes:
        print("     " * node[1], node[0])


def test():
    categories = {'cat1': None, 'cat2': {'cat3': None, 'cat4': None}, 'cat5': {'cat6': {'cat7': None}}}
    doc_columns = ['id', 'title']
    headers(doc_columns, categories)


def test2():
    load_excel_to_clasify()


def test3():
    list_nodes = generate_categories_visualization_values()
    print_categories_visualization(list_nodes)
    pass


if __name__ == '__main__':
    # generate_excel_to_clasify()
    # test()
    # test2()
    test3()
    pass





