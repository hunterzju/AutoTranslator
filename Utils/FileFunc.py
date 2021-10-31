'''
Author: your name
Date: 2021-10-31 17:53:57
LastEditTime: 2021-10-31 20:40:35
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /AutoTranslator/Utils/FileFunc.py
'''
import os
from typing import List
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

class PathManager:
    def __init__(self) -> None:
        pass

    def isPathFile(self, path) -> bool:
        return os.path.isfile(path)

    def isPathDir(self, path) -> bool:
        return os.path.isdir(path)

    def isPathExists(self, path) -> bool:
        return os.path.exists(path)

    def getFileList(self, dirpath) -> List:
        for root, ds, fs in os.walk(dirpath):
            for f in fs:
                yield os.path.join(root, f)
