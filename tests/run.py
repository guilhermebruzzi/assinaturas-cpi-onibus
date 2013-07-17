#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import traceback
import nose
from optparse import OptionParser

def add_path():
    global project_root
    file_path = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath("%s/../" % file_path)
    sys.path.insert(0, project_root)
    return project_root

project_root = add_path()

os.environ["MONGODB_DB"] = "assinatura_cpi_test"
os.environ["TESTING"] = "True"
os.environ["SECRET_KEY"] = "test key"

from config import get_app
import app

def run_tests():
    result = None
    try:
        parser = OptionParser()
        parser.add_option("-f", "--file", dest="filename", help="Nome dos arquivos para rodar", default=None)
        (parsed, args) = parser.parse_args()
        params = ["nosetests", "--with-xcoverage", "--with-xunit", "-w", "tests", "--cover-package", "assinaturas_cpi_onibus.*", "--match", "(?:^|[\b_\./-])[Tt]est"]
        if parsed.filename:
            params.insert(0, "--tests=")
            params.insert(0, parsed.filename)
        result = nose.run(argv=params)

    except Exception as e:
        print ""
        print e
        print ""

        traceback.print_last()
    finally:
        if result:
            exit(0)
        exit(1)

if __name__ == '__main__':
    run_tests()