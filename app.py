"""API to inteface Vault.

Little web app to interface with Vault.
"""
import os
import hvac
import ast

from flask import Flask, jsonify, request, abort

app = Flask(__name__)
VERSION = '0.0.4'

client = hvac.Client()


@app.route("/")
def hello():
    """Base entrypoint."""
    return jsonify(
        {
            'message': 'Well, Hello! I am  vaultweb',
            'version': VERSION})


@app.route("/login/token", methods=['POST'])
def login_token():
    """Login to Vault using a token."""
    host = request.form['host']
    token = request.form['token']
    client = hvac.Client(
        url=host,
        token=token,
        verify=ast.literal_eval(os.environ['VERIFY']))

    if client.is_authenticated():
        return 200
    else:
        return 401


@app.route("/readValue")
def read_value():
    """Read KVs from Vault inside a value attr."""
    key = request.args.get('key')
    try:
        resp = read_key(key)
        val = resp['val']
        data = val['data']
        value = data['value']
        entries = value.split()
        list_val = []
        for entry in entries:
            list_val.append(entry)
        return jsonify(resp)
    except Exception as e:
        return jsonify(key=str(e))


@app.route("/read")
def read():
    """Read KVs from Vault."""
    key = request.args.get('key')
    try:
        resp = read_key(key)
        return jsonify(resp)
    except Exception as e:
        return jsonify(key=str(e))


def read_key(key):
    """Read key from Vault."""
    client = hvac.Client(
        url=os.environ['VAULT_SERVER'],
        token=os.environ['VAULT_TOKEN'],
        verify=ast.literal_eval(os.environ['VERIFY']))
    val = client.read(key)
    app.logger.debug(val)

    obj = {'key': key, 'val': val}
    return obj


@app.route("/write", methods=['POST'])
def write():
    """Write KVs to Vault."""
    key = request.form['key']
    pair_key = request.form['pair_key']
    pair_value = request.form['pair_value']
    lease = request.form["lease"]

    client = hvac.Client(
        url=os.environ['VAULT_SERVER'],
        token=os.environ['VAULT_TOKEN'],
        verify=ast.literal_eval(os.environ['VERIFY']))
    obj = {pair_key: pair_value, "lease": lease}
    client.write(key, **obj)
    return jsonify(obj)


@app.route("/healthcheck")
def health():
    """Healthcheck that verifies if the service can talk to Vault."""
    client = hvac.Client(
        url=os.environ['VAULT_SERVER'],
        token=os.environ['VAULT_TOKEN'],
        verify=ast.literal_eval(os.environ['VERIFY']))
    if client:
        return "ok", 200
    else:
        abort(409)


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
