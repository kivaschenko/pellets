import psycopg2
import click
from flask import current_app
from flask.cli import with_appcontext
from . import config


def create_tables():
    '''Create all tables in the current database'''
    with current_app.open_resource('schema.sql') as f:
        commands = f.read().decode('utf8')

    with psycopg2.connect(**config.db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(commands)

@click.command('init_db')
@with_appcontext
def init_db_command():
    '''Clear the existing data and create new table'''
    create_tables()
    click.echo('Initialized the new database.')

def init_app(app):
    app.cli.add_command(init_db_command)