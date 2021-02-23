import os
from configparser import ConfigParser

def get_db_params(filename='config.ini', section='postgresql'):
    '''parse the database parameters for connecting
    '''
    parser = ConfigParser()
    filepath = os.path.join(os.getcwd(), filename)
    parser.read(filepath)
    if parser.has_section(section):
        db_params = {param[0]:param[1] for param in parser.items(section)}
    else:
        raise Exception(f'Section {section} not found in the {filename}')
    return db_params
