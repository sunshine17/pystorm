#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pystorm.services import FetchService
from pystorm.tasks import TaskObject
from pystorm.report import parse_bytes, parse_time
import md5

# Start fetch services 
fetch_service = FetchService(2)
fetch_service.start()

url_list = [
#    'http://zhangmenshiting.baidu.com/data2/music/35419687/2658981364835661192.mp3?xcode=0498c120d84ad3b9a2238d4578ab66ec',
    'http://zhangmenshiting.baidu.com/data2/music/1462458/1028646194400192.mp3?xcode=2028c51708f6206c30b0581eb794ca53',
    'http://zhangmenshiting.baidu.com/data2/music/3454'

#    'http://mr4.douban.com/201304031029/778eea11cb0f8b58bc8fa12a92f0a456/view/musicianmp3/mp3/x14363243.mp3', 
#    'http://mr3.douban.com/201304031029/9f7f58cd47e2cf6fd0f43e3db35edad5/view/musicianmp3/mp3/x14329077.mp3',
#    'http://mr3.douban.com/201304031029/78a6437fe22124b10ef079f86ce0665f/view/musicianmp3/mp3/x14320126.mp3'
            ]

def gen_out_fname(url):
    m = md5.new()
    m.update(url)
    return m.hexdigest() + '.mp3'

task_list = [ TaskObject(url, output_file=gen_out_fname(url)) for url in url_list]

def update_state(task, data):
    progress = "%d%%" % data.progress
    speed = parse_bytes(data.speed)
    remaining = parse_time(data.remaining)
    filesize = parse_bytes(data.filesize)
    downloaded = parse_bytes(data.downloaded)
    
    print "%s: %s/s - %s, progress: %s, total: %s, remaining time: %s" % (task.output_file, speed, 
                                                                          downloaded, progress, 
                                                                          filesize, remaining)
    print "-----------------------------------------------------------"
    
curr_num = 0;
def on_finish(task, data):
    global curr_num
    curr_num += 1
    print '===Task FIN: ' + task.output_file

def on_start(task, data):
    print '===Task STARTED: ' + task.output_file

def on_err(task, err):
    print '===ERR task url: '  + task.url
#    print err

for task in task_list:
#    task.connect("update", update_state)
    task.connect("finish", on_finish)
    task.connect("start", on_start)
    task.connect("error", on_err)
    
fetch_service.add_missions(task_list)    

while curr_num < len(task_list):
    try:
        fetch_service.join(5.0)
    except KeyboardInterrupt:    
        sys.exit(0)
        raise SystemExit
