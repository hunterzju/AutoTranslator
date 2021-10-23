from Srt import SrtItem, SrtPage

'''
description: Translate Srt file from source language to destination language.
param {*}
return {*}
'''
class SrtTranslator:
    def __init__(self, src_lang=None, dst_lang=None, src_page=None, dst_page=None):
        self.src_lang = src_lang
        self.dst_lang = dst_lang
        self.src_page = src_page
        self.dst_page = dst_page
        self.src_content = None
        self.dst_content = None
    
    def setSrcLanguage(self, language):
        self.src_lang = language            # TODO: assert language Enum
    
    def getSrcLanguage(self):
        return self.src_lang
    
    def setDstLanguage(self, language):
        self.dst_lang = language
    
    def getDstLanguage(self, language):
        return self.dst_lang
    
    def setSrcPage(self, srt_page):
        self.src_page = srt_page
    
    def setDstPage(self, dst_page):
        self.dst_page = dst_page
    
    def setSrcContent(self, content):
        self.src_content = content
    
    def getSrcContent(self):
        return self.src_content
    
    def setDstContent(self, content):
        self.dst_content = content
    
    def getDstContent(self):
        return self.dst_content

    '''
    description: load SrtPage from lines in file.
    param {*} self - class object
    param {*} lines - srt lines from a file.
    param {*} src_lang - source srt file language.
    return {*}
    '''
    def getSrcPageFromLines(self, lines, src_lang=None):
        # TODO: check if src_lang == self.src_lang
        if src_lang is None:
            src_lang = self.src_lang
        srt_page = SrtPage(src_lang)

        srt_item = None
        for idx, line in enumerate(lines):
            line = line.strip('\n')
            if idx % 4 == 0:
                srt_item = SrtItem(idx=int(line))
            elif idx % 4 == 1:
                srt_item.setTimeline(line)
            elif idx % 4 == 2:
                srt_item.setContent(line)
                srt_page.appendSrt(srt_item)
            else:
                continue
        
        self.src_page = srt_page
    
    # TODO: extract content from Src Page
    def extractContentFromPage(self):
        content = ""
        for item in self.src_page.srt_list:
            content += item.content
        return content

    # TODO: translate from Src content to Dst content

    # TODO: split translate result and set into Dst srt page
    def setDstPageFromContent(self):
        pass

def test(path):
    # TODO: add test function.
    pass

if __name__ == "main":
    import sys

    path = sys.argv[1]
    test(path)
    

