#!/usr/bin/env python
#-*- coding:utf-8 -*-

import settings

def main():
    from utils import download_harvest_project_names
    download_harvest_project_names(settings.HARVEST_HOST, settings.HARVEST_AUTH)
    return 0

if __name__ == '__main__':
    from os.path import abspath, dirname, join as pathjoin
    import sys
    sys.path.insert(0, abspath(pathjoin(dirname(__file__), '..', 'libs')))

    sys.exit(main())
