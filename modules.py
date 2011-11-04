from flask import Flask, jsonify, render_template, request
from database import db_session
import hashlib, json, jsonrpclib, urllib

from htpcfrontend import app
from settings import *
from tools import *

from database import *
from models import Module

AVAILABLE_MODULES = [
    {
        'name': 'applications',
        'label': 'Applications',
        'description': 'Allows you to link to whatever applications you want (SABnzbd, SickBeard, etc.)',
        'mandatory_static': False,
        'static': True,
        'poll': None,
        'delay': 0,
    },
    {
        'name': 'recently_added',
        'label': 'Recently added',
        'description': 'Shows you episodes recently added to your library.',
        'mandatory_static': False,
        'static': False,
        'poll': 350,
        'delay': 0,
    },
]

@app.route('/xhr/add_module_dialog')
@requires_auth
def add_module_dialog():
    return render_template('add_module_dialog.html',
        available_modules = AVAILABLE_MODULES,
    )

@app.route('/xhr/add_module', methods=['POST'])
@requires_auth
def add_module():
    try:
        module_id = request.form['module_id']
        column = request.form['column']
        position = request.form['position']

        module_info = None

        for available_module in AVAILABLE_MODULES:
            if module_id == available_module['name']:
                module_info = available_module
                break

        if not module_info:
            return jsonify({ 'status': 'error' })

    except:
        return jsonify({ 'status': 'error' })

    module = Module(
        module_info['name'],
        module_info['static'],
        column,
        position,
        module_info['poll'],
        module_info['delay'],
    )

    db_session.add(module)
    db_session.commit()

    module_info['template'] = '%s.html' % (module_info['name'])

    return render_template('placeholder_template.html',
        module = module_info,
    )