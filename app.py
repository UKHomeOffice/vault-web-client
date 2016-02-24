"""API to inteface Vault.

Little web app to interface with Vault.
"""
import os
import hvac

from flask import Flask, jsonify, request
app = Flask(__name__)
VERSION = '0.0.1'


@app.route("/")
def hello():
    """Base entrypoint."""
    return jsonify(
        {
            'message': 'Well, Hello! I am  vaultweb',
            'version': VERSION})


@app.route("/read")
def read():
    """Read KVs from Vault."""
    key = request.args.get('key')
    client = hvac.Client(
        url=os.environ['VAULT_SERVER'],
        token=os.environ['VAULT_TOKEN'],
        verify=False)
    try:
        val = client.read(key, )
        return jsonify(key=val)
    except Exception as e:
        print (e)
        return jsonify(key=str(e))


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
