# -*- coding: utf-8 -*-
'''
Author: liuyouyuan
Date: 2020-09-04 14:00:01
LastEditTime: 2020-09-10 15:39:49
LastEditors: liuyouyuan
Description: gunicorn config file
FilePath: prodir/conf/gunicorn_conf.py
'''
import os
import logging
import logging.handlers
import multiprocessing
from logging.handlers import WatchedFileHandler
from conf.project_conf import APP_DIR
from conf.project_conf import LOG_DIR
from conf.project_conf import APP_PORT
from conf.project_conf import PID_FILE

# 绑定ip端口
bind = '0.0.0.0:' + str(APP_PORT)

# 监听队列
backlog = 512

# gunicorn要切换到的目的工作目录
chdir = APP_DIR

# 超时时间
timeout = 30

# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
# worker_class = 'sync' 

# 进程数
workers = 1

# 指定每个进程开启的线程数
threads = 1

# pid 文件
pidfile = PID_FILE

# 错误日志的级别，访问日志的级别无法设置
loglevel = 'info' 

# 设置gunicorn访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"' 

accesslog = LOG_DIR + "gunicorn_access.log"      # 访问日志文件
errorlog = LOG_DIR + "gunicorn_error.log"        # 错误日志文件