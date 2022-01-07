#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 14:28:15 2020

@author: leonard
"""
import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    print("Running as python executable")
    ROOT_DIR = os.path.dirname(sys.executable)
elif __file__:
    print("Running as python script")
    ROOT_DIR = os.path.dirname(__file__)

print("Application path: ", ROOT_DIR)

CONFIG_FOLDER = Path(os.path.join(ROOT_DIR, "config"))