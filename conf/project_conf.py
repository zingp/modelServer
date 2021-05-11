'''
Author: liuyouyuan
Date: 2020-09-10 14:43:22
LastEditTime: 2020-09-10 15:38:08
LastEditors: liuyouyuan
Description: app config file
FilePath: prodir/conf/project_conf.py
'''
import os
# -- 基础配置 --
# 测试配置
APP_DIR = "./"
LOG_DIR = "./logs/"
DATABASE = APP_DIR

# 生产环境
# APP_DIR = "/project/"
# LOG_DIR = "/project/"
# DATABASE = "/data"

APP_PORT = 7483
PID_FILE = os.path.join(APP_DIR, "server.pid")

LOG = {
    "format": '"%(asctime)s [%(process)d] %(levelname)s %(pathname)s[line:%(lineno)d] - %(message)s"',
    "filename": LOG_DIR + "server.log",
    "level": "INFO"
}

# --BERT 配置--
MODEL_PATH = os.path.join(DATABASE, "data/bert_model/bert")
MODEL_NAME = "roberta.pt"

DEVICE = "cpu"
PAD_SIZE = 128
RATE = 0.5