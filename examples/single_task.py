#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from pystorm.tasks import TaskObject

test_ftp = "ftp://ftp.cc.uoc.gr/mirrors/linux/lglive/win32diskimager.zip"

download_task = TaskObject(sys.argv[1], 
                           verbose=True
                           )

download_task.run()

