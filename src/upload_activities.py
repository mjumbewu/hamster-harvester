#!/usr/bin/env python
#-*- coding:utf-8 -*-

import settings
import datetime as dt

def main():
    from utils import upload_hamster_facts
    from sys import argv

    if len(argv) > 2:
        start = dt.datetime.strptime(argv[1], '%Y-%m-%d').date()
        end = dt.datetime.strptime(argv[2], '%Y-%m-%d').date()
    else:
        start = end = None

    upload_hamster_facts(settings.HARVEST_HOST, 
                         settings.HARVEST_AUTH, 
                         start or dt.date.today(), 
                         end or dt.date.today())
    return 0

if __name__ == '__main__':
    from os.path import abspath, dirname, join as pathjoin
    import sys
    sys.path.insert(0, abspath(pathjoin(dirname(__file__), '..', 'libs')))

    sys.exit(main())
