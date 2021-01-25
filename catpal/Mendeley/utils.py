from datetime import datetime


def get_current_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    return dt_string


def parse_link_headers(link):
    link = link.replace(' ', '')
    links = link.split(',')
    parsed_links = {}
    for _link in links:
        _links = _link.split(';')
        key = _links[1][5:-1]
        value = _links[0][1:-1]
        parsed_links[key] = value

    return parsed_links

from cryptography.fernet import Fernet
if __name__== "__main__":
    #trying to generate the same key with the use
    key = Fernet.generate_key()
