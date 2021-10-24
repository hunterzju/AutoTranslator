import re
import sys
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_PATH)

class SrtItem:
    __slots__ = ['index', 'timeline', 'content']
    def __init__(self, idx=None, timeline=None, content=""):
        self.index = idx
        self.timeline = timeline
        self.content = content

    def setIdx(self, idx):
        self.index = idx
    
    def getIdx(self):
        return self.index

    def setTimeline(self, timeline):
        self.timeline = timeline
    
    def getTimeline(self):
        return self.timeline

    def addContent(self, content):
        self.content += content
    
    def getContent(self):
        return self.content

class SrtPage:
    def __init__(self, lang=None, srt_list=[]):
        self.language = lang
        self.srt_list = srt_list

    def getSrtList(self):
        return self.srt_list

    def appendSrt(self, srt_item):
        # FIXME: checkif self.srt_list is 'list' type
        self.srt_list.append(srt_item)

class StringOPs:
    def __init__(self):
        self.split_symbols = r"[.|!|?]"        # use 'r' as regex expression

    def Spliter(self, content, split_sbls=None):
        if split_sbls == None:
            split_sbls = self.split_symbols
        res_list = re.split(split_sbls, content)
        return res_list
