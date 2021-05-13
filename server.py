# -*- coding: utf-8 -*-
'''
Author: liuyouyuan
Date: 2020-09-02 11:36:41
LastEditTime: 2020-09-10 15:31:56
LastEditors: liuyouyuan
Description: app main
FilePath: ~/server.py
'''
import os
import time
import json
import logging
import logging.handlers

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify

from src import bert_run


app = Flask(__name__)
app.config.from_pyfile("conf/project_conf.py", silent=False)


# log config
def init_logger():
    log_config = app.config.get("LOG")
    print(log_config)
    logging.basicConfig(level=log_config['level'])
    logger = logging.getLogger()
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_config['filename'], when="MIDNIGHT")
    formatter = logging.Formatter(log_config['format'])
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# model加载层
def load_bert_model():
    return bert_run.Model(app.config)


@app.route('/server/predict', methods=['POST'])
def predict():
    try:
        req_data = request.get_json()
        logging.info('req_data:{}'.format(str(req_data)))
    except Exception as e:
        info = "requests json parse error, error {}, request:{}"
        logging.error(info.format(str(e), str(request)))
        return make_response(jsonify({}), 400)

    # 判断请求是否合法
    if not all(k in req_data for k in ["audio_id", "text", "from"]):
        logging.warning("bad request for search:{}".format(req_data))
        return make_response(jsonify({}), 400)

    ret = {"status": 200, "reason": "", "label": 1}
    log_result = {"label": 1}
    audio_id = req_data["audio_id"]
    text = req_data["text"]
    plat = req_data["from"]

    log_result["audio_id"] = audio_id
    log_result["plat"] = plat

    if not text.strip():
        ret["label"] = 0
        ret["reason"] = "text is empty"
        log_result["label"] = 0
        logging.info(str(json.dumps(log_result, ensure_ascii=False)))
        return make_response(jsonify(ret), 200)

    label_match, bert_prob = 0, 0
    #try:
    start = time.time()
    bert_prob = bert_model.predict(text)
    end = time.time()
    log_result["bert_pro"] = float(bert_prob)
    log_result["bert_duration"] = round(end-start, 6)
    # except Exception as e:
    #     info = "bert model error, error:{}, audio_id:{}, text:{}"
    #     logging.error(info.format(str(e), audio_id, str(text)))
    if bert_prob >= float(app.config.get("RATE")):
        logging.error(str(json.dumps(log_result, ensure_ascii=False)))
        return make_response(jsonify(ret), 200)
    
    ret["label"] = 0
    log_result["label"] = 0
    logging.info(str(json.dumps(log_result, ensure_ascii=False)))

    return make_response(jsonify(ret), 200)


init_logger()
logging.info('config load successful, params:{}'.format(str(app.config)))

bert_model = load_bert_model()
logging.info('bert_model load successful')


if __name__ != "__main__":
    port = app.config.get("APP_PORT")
    logging.info("server app is started")

if __name__ == '__main__':
    port = app.config.get("APP_PORT")
    logging.info("use port:{}".format(port))

    logging.info("server app is starting")
    app.run(threaded=True, host="0.0.0.0", port=port, debug=False)
