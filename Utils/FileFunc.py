'''
Author: your name
Date: 2021-10-31 17:53:57
LastEditTime: 2021-10-31 19:13:41
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /AutoTranslator/Utils/FileFunc.py
'''
from Utils.LogFrame import default_logger

file_logger = default_logger

class FileRW:
    def __init__(self, encoding="UTF-8", mod="rt"):
        self.encoding = encoding
        self.mode = mod
    
    def setEncoding(self, encode_str):
        self.encoding = encode_str
    
    def setFileMode(self, mode_str):
        self.mod = mode_str
    
    def readFromFile(self, path):
        lines = None
        with open(path, mode=self.mode, encoding=self.encoding) as fr:
            lines = fr.readlines()
        return lines

    def dumpToFile(self, path, content):
        with open(path, mode=self.mode, encoding=self.encoding) as fw:
            fw.writelines(content)
        file_logger.info("Write content info file: {}".format(path))
