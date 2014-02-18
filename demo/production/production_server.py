# -*- coding: utf-8 -*-

from flask import Flask, jsonify


app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/available/<int:i>')
def from_production(i):
    return jsonify({'message': 'I am from production server.'})


def main():
    app.run('localhost', 9000)


if __name__ == '__main__':
    main()
