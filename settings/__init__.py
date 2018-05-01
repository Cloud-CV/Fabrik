# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

# TODO: Add support for test and production environment settings

try:
    from .dev import *  
    print("Using Dev settings")
except ImportError:
    pass
