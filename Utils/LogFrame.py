import os
from loguru import logger

class LoggerExt:
    # log config
    def __init__(self, logpath):
        # info log
        logger.add(
            os.path.join(logpath, "logs/Info-{time:YYYY-MM-DD}.log"),
            format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            filter = lambda x: True if x["level"].name == "INFO" else False,
            rotation = "10MB", retention=7, level="INFO", encoding='utf-8',
            compression = "zip"
        )
        # debug log
        logger.add(
            os.path.join(logpath, "logs/Debug-{time:YYYY-MM-DD}.log"),
            format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation = "10MB", retention=7, level="DEBUG", encoding='utf-8',
            compression = "zip"
        )
        # error log
        logger.add(
            os.path.join(logpath, "logs/Error-{time:YYYY-MM-DD}.log"),
            format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            filter = lambda x: True if x["level"].name == "ERROR" else False,
            rotation = "10MB", retention=7, level="ERROR", encoding='utf-8',
            compression = "zip"
        )

        self.logger = logger

    def get(self):
        return self.logger

def test():
    test_logger = LoggerExt("./").get()

    test_logger.info("This is a info log")
    test_logger.info("中文日志测试")
    test_logger.error("Test error log")
    test_logger.debug("Test debug log")

if __name__ == "__main__":
    test()
