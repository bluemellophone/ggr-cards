import argparse
from datetime import date
import logging
import socket

import flask
from flask import make_response, redirect, request, url_for  # NOQA
import tornado.httpserver
import tornado.wsgi

# TYPE 1
CAR_COLORS = ['white', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black']
CAR_NUMBER = list(map(str, range(1, 25)))  # 50
PERSON_LETTERS = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
]  # , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']

# TYPE 2
CAR_COLORS = ['white']
CAR_NUMBER = list(map(str, range(1, 253)))  # 250
PERSON_LETTERS = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
]  # , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']


# Application
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024 * 1024  # 256 Megabytes
app.config['TEMPLATES_AUTO_RELOAD'] = True


class NavbarClass:
    def __init__(nav):
        nav.item_list = [
            ('', 'Home'),
            ('overview', 'Overview'),
            ('images/form', 'Images'),
            ('gps/form', 'GPS'),
            ('map/form', 'Map'),
            ('cards', 'Cards'),
        ]

    def __iter__(nav):
        _link = request.path.strip('/').split('/')
        for link, nice in nav.item_list:
            yield link == _link[0], link, nice


def template(template_name=None, **kwargs):
    if template_name is None:
        template_name = 'index'
    template_ = template_name + '.html'
    # Update global args with the template's args
    global_args = {
        'NAVBAR': NavbarClass(),
        'YEAR': date.today().year,
    }
    _global_args = dict(global_args)
    _global_args.update(kwargs)
    print(template_)
    return flask.render_template(template_, **_global_args)


@app.route('/')
def cards(type=4):
    if type == 1:
        page_list = [
            [
                [
                    (1, 'red', 'a'),
                    (24, 'blue', 'f'),
                    (3, 'orange', 'd'),
                ],
                [
                    (18, 'purple', 'c'),
                    (4, 'white', 'd'),
                    (2, 'black', 'b'),
                ],
                [
                    (9, 'green', 'a'),
                    (11, 'yellow', 'e'),
                    (19, 'red', 'c'),
                ],
                [
                    (4, 'orange', 'b'),
                    (3, 'blue', 'f'),
                    (21, 'purple', 'a'),
                ],
            ]
        ]
    else:
        page_list = []

    i = 1
    page = []
    row = []
    for car_color in CAR_COLORS:
        for batch in range(1, len(CAR_NUMBER) + 1, 12):
            limit = min(batch + 12, len(CAR_NUMBER) + 1)
            for person_letter in PERSON_LETTERS:
                for car_number in range(batch, limit):
                    row.append((car_number, car_color, person_letter))
                    if i % 3 == 0:
                        page.append(row)
                        row = []
                    if i % 12 == 0:
                        page_list.append(page)
                        page = []
                    i += 1

    return template('cards', page_list=page_list, type=type)


def start_tornado(app, port=5000):
    def _start_tornado():
        http_server = tornado.httpserver.HTTPServer(tornado.wsgi.WSGIContainer(app))
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()

    # Initialize the web server
    logging.getLogger().setLevel(logging.INFO)
    try:
        app.server_ip_address = socket.gethostbyname(socket.gethostname())
        app.port = port
    except Exception:
        app.server_ip_address = '127.0.0.1'
        app.port = port
    url = f'http://{app.server_ip_address}:{app.port}'
    print(f'[web] Tornado server starting at {url}')
    # Blocking
    _start_tornado()


def start_from_terminal():
    # Parse command line arduments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', help='which port to serve content on', type=int, default=4000
    )
    # Start tornado
    args = parser.parse_args()
    start_tornado(app, args.port)


if __name__ == '__main__':
    start_from_terminal()
