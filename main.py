from fastapi import FastAPI

from core import PortSeCore

__author__ = 'danieluhm2004 <iam@dan.al>'
__copyright__ = 'Copyright 2020, Daniel Uhm'

app = FastAPI(
    title='PortSe v2',
    description='Iptable based port forwarding to REST API',
    debug=True
)

if __name__ == '__main__':
    core = PortSeCore(app)
    core.start()
