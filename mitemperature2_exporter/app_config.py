# -*- coding: utf-8 -*-

import toml


def app_config():
    return toml.load("config/app.toml")
