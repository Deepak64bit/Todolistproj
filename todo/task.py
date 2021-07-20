import datetime
from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g
from . import db

bp = Blueprint("task", "task", url_prefix="")

def format_date(d):
    if d:
        v = d.strftime('%Y-%m-%d %H:%M:%S')
        return v
    else:
        return None

        
    



