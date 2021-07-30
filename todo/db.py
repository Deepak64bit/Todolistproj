import datetime
import random
import sqlite3

import click 
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g: 
        dbname = current_app.config['DATABASE'] 
        g.db = sqlite3.connect(dbname)
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    #tables are created
    f = current_app.open_resource("sql/create.sql")
    sql_codes = f.read().decode("ascii")
    cur = db.cursor()
    cur.executescript(sql_codes)
    cur.close()
    db.commit()
    close_db()


@click.command('initdb', help="initialise the database")
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialised') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
