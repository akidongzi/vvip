# coding=utf-8

# print "config================",__name__

import logging, logging.handlers
import os


__LOG_FILE = './log/runlog.log'

logger = logging.getLogger()

def initLog():
    __DIR__ = "./log"
    if os.path.isdir(__DIR__) == False:
        os.makedirs(__DIR__)
    hdlr = logging.handlers.TimedRotatingFileHandler(__LOG_FILE, when='midnight', backupCount=30)
    formatter = logging.Formatter("[%(asctime)s]: %(module)s %(message)s ")
    # formatter = logging.Formatter("[%(asctime)s]: %(module)s %(levelname)s \n%(message)s \n")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    logger.info("initialization log handler success! FILE=[%s]" % __LOG_FILE)


if __name__ == '__main__':
    print 'main'
