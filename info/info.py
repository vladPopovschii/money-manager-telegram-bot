from os import path

markup = open(path.join(path.dirname(__file__), 'info.html'), 'r').read()

def get_info_markup() -> str:
    return markup