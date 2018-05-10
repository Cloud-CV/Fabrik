# -*- coding: utf-8 -*-
from __future__ import absolute_import

# TODO: Add support for production environment settings

import sys

TEST = [arg for arg in sys.argv if 'test' in arg]
if TEST:
    print("Using Test settings")
    from .test import * # noqa
else:
    try:
        from .dev import *  # noqa
        print("Using Dev settings")
    except ImportError:
        pass
