from datetime import datetime
import logging
# import TestResult

def driverPath():
    return r'C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe'

def baseUrl():
    return "http://10.58.122.201/"

# change time to str
def getCurrentTime():
    format = "%a %b %d %H:%M:%S %Y"
    return datetime.now().strftime(format)

# Get time diff
def timeDiff(starttime, endtime):
    format = "%a %b %d %H:%M:%S %Y"
    return datetime.strptime(endtime, format) - datetime.strptime(starttime, format)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def CreateLoggerFile(filename):
    try:
        fulllogname = ResultFolder.GetRunDirectory() + "\\" + filename + ".log"
        fh = logging.FileHandler(fulllogname)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [line:%(lineno)d] %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as err:
        logger.debug("Error when creating log file, error message: {}".format(str(err)))


def Log(message):
    logger.debug(message)