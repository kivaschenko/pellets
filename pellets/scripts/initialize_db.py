import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models
from .seed_data import GOODS

def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    # insert data into goods table
    for item in GOODS:
        model = models.offer.Goods(name=item[0], body=item[1])
        dbsession.add(model)

    # create couple users: 'teodor' and 'civa'
    teodor = models.user.User(nickname='teodor', email='teodorathome@yahoo.com',
           role='editor')
    teodor.set_password('Teodorathome11')
    dbsession.add(teodor)

    civa = models.User(nickname='civa', email='civaschenko@yahoo.com',
         role='base')
    civa.set_password('Ki150797')
    dbsession.add(civa)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
