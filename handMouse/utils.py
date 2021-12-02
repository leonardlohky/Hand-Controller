#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:34:11 2020
@author: leonard
"""
import configparser
from definitions import CONFIG_FOLDER
    
def get_config_param(section, field):
    config = configparser.ConfigParser()
    config.read(CONFIG_FOLDER / "settings.ini")
    param = config.get(section, field)
    
    return param