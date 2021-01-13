#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import waitress
from paste.translogger import TransLogger

import app
from option import App, Server, Log

if __name__ == "__main__":
    print(f"Starting '{App.name}' Project...")

    logger = logging.getLogger(
        name="wsgi"
    )

    logger.addHandler(
        hdlr=logging.FileHandler(
            filename=Log.file
        )
    )

    app = app.create_app()
    waitress.serve(
        app=TransLogger(
            application=app,
            setup_console_handler=True
        ),
        port=Server.port
    )
