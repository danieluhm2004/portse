import sys

import uvicorn
from API.v1 import router as _v1_router
from config import host, port

from MySQL import init_connection


class PortseCore:
    def __init__(self, app):
        self.terminating = False
        self.app = app

        # include API router
        self.app.include_router(_v1_router)

    @classmethod
    def show_banner(self, add_padding=False):
        ''' Show banner for XenXenXenSe Project '''
        from pyfiglet import Figlet
        figlet = Figlet()

        print(figlet.renderText('Portse'))
        print('Project Portse : a RESTful API implementation for iptable based port forwarding')
        print()
        print('Copyright (c) Daniel Uhm.')
        print('This software is distributed under Affero GNU Public License v3.')

        if add_padding:
            print()

    def run_api_server(self, development_mode=False):
        ''' Run API Server '''
        if development_mode:
            # development environment
            print('Running in development mode!')
            uvicorn.run('main:app', host=host, port=port, reload=True)

        else:
            # production environment
            uvicorn.run(self.app, host=host, port=port)

    def connect_db(self):

        # Temporary Solution, will refactor to OOP Python. - @zeroday0619 Plz help!
        init_connection()

    def start(self):
        self.show_banner(True)
        print()

        # Detect if server is executed with development mode
        development_mode = (('-d' in sys.argv) or ('--dev' in sys.argv))

        # Run DB Cache Service
        self.connect_db()

        # Run API Server
        self.run_api_server(development_mode)

        # Termination
        self.terminating = True
