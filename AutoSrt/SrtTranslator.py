import sys
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_PATH)

import time
from AutoSrt.Srt import SrtItem, SrtPage, StringOPs
from Translator.TxyTranslator import TencentTranslate
# from pygoogletranslation import Translator        # call times limited.
from Utils.LogFrame import default_logger
from AutoSrt import DEBUG

trans_logger = default_logger
g_str_ops = StringOPs()


'''
description: Translate Srt file from source language to destination language.
param {*}
return {*}
'''
class SrtTranslator():
    def __init__(self, src_lang=None, dst_lang=None, src_page=None, dst_page=None):
        self.src_lang = src_lang
        self.dst_lang = dst_lang
        self.src_page = src_page
        self.dst_page = dst_page
        self.trans_client = TencentTranslate()

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

    '''
    description: load SrtPage from lines in file.
    param {*} self - class object
    param {*} lines - srt lines from a file.
    param {*} src_lang - source srt file language.
    return {*}
    '''
    def constructSrcPageFromLines(self, lines, src_lang=None):
        # TODO: check if src_lang == self.src_lang
        if src_lang is None:
            self.logger.warning("src lange is not set, use {} instead.".format(self.src_lang))
            src_lang = self.src_lang
        srt_page = SrtPage(lang=src_lang, srt_list=[])

        srt_item = None
        for idx, line in enumerate(lines):
            line = line.strip('\n')
            if idx % 4 == 0:
                srt_item = SrtItem(idx=int(line), content=dict())
            elif idx % 4 == 1:
                srt_item.setTimeline(line)
            elif idx % 4 == 2:
                srt_item.addContent(self.src_lang, line)
                srt_page.appendSrt(srt_item)
            else:
                continue

        self.setSrcPage(srt_page)
        return srt_page

    '''
    description: extract content from src page items.
    param {*} self
    return {*} content - raw text in src language.
    '''
    def extractContentFromPage(self, srt_page=None):
        content = ""

        if srt_page == None and self.src_page == None:
            trans_logger.error("translator src page is None")
            return None
        elif srt_page == None:
            srt_page = self.src_page

        for item in srt_page.getSrtList():
            content += item.getContent(self.src_lang).strip()

        if DEBUG:
            trans_logger.debug(content)

        return content

    '''
    description: split origin text by sentence and construct dst page
    param {*} self
    param {*} content - origin content
    return {*} dst_page
    '''
    def constructDstPage(self, content):
        new_page = SrtPage(lang=self.dst_lang ,srt_list=[])
        if self.dst_page == None:
            self.setDstPage(new_page)

        origin_text_list = g_str_ops.Spliter(content, split_sbls=r"[.|!|?]")
        origin_len = len(origin_text_list)

        src_list = self.src_page.getSrtList()
        src_len = len(src_list)

        write_idx = 0
        for idx in range(src_len):
            dst_item = SrtItem(idx=src_list[idx].getIdx(), timeline=src_list[idx].getTimeline(), content=dict())
            if idx < origin_len:
                dst_item.addContent(self.src_lang, origin_text_list[idx].strip())

            if DEBUG:
                trans_logger.debug(str(idx)+":"+str(dst_item.content))

            new_page.appendSrt(dst_item)
            write_idx = idx

        # if split origin item is more than src srt item, create new item with last timeline in src.
        if write_idx < origin_len:
            for idx in range(write_idx, origin_len):
                dst_item = SrtItem(idx=idx, timeline=src_list[-1].getTimeline())
                dst_item.addContent(self.src_lang, origin_text_list[idx].strip())

                if DEBUG:
                    trans_logger.debug(str(idx) + str(dst_item.content))

                new_page.appendSrt(dst_item)
                write_idx = idx

        return new_page

    '''
    description: translate from Src content to Dst content by item.
    param {} dst_lang - dst lanuage
    return {*} dst_page - dst page
    res - Translated object in pygoogletranslation, origin for src language, text for dst language.
    reflink:https://github.com/Saravananslb/py-googletranslation
    '''
    def translatePage(self, dst_lang=None, srt_page=None):
        if self.trans_client == None:
            trans_logger.error("No translator Found.")
            sys.exit(-1)
        if srt_page == None:
            srt_page = self.src_page

        if dst_lang == None:
            trans_logger.warning("Translator dst language not set. Use default language {}".format(self.dst_lang))
            dst_lang = self.dst_lang

        for idx, item in enumerate(srt_page.getSrtList()):
            # jump empty item
            if self.src_lang not in item.content.keys():
                continue
            if item.getContent(self.src_lang) in ['' or None]:
                continue
            # res = self.trans_client.translate(item.getContent(self.src_lang), dest=self.dst_lang)
            if DEBUG:
                trans_logger.debug(item.getContent(self.src_lang))
            res = TencentTranslate().translate(text=item.getContent(self.src_lang), target=self.dst_lang)
            if DEBUG:
                trans_logger.debug(str(idx) + ":" + str(res))
            srt_page.srt_list[idx].addContent(self.dst_lang, res)

            # tencent translate api limit to 5/1s.
            if idx % 5 == 0:
                time.sleep(1)
        self.setDstPage(srt_page)

        return srt_page

    '''
    description: export dst page into content.
    param {*} self
    param {*} origin
    return {*}
    '''
    def exportPageToLines(self, srt_page, origin=False):
        content = ""

        for item in srt_page.getSrtList():
            content += str(item.getIdx()) + "\n"
            content += item.getTimeline() + "\n"
            if origin:
                if self.src_lang not in item.content.keys():
                    pass
                else:
                    content += item.getContent(self.src_lang) + "\n"
            if self.dst_lang in item.content.keys():
                content += item.getContent(self.dst_lang) + "\n"
            content += "\n"

        if DEBUG:
            trans_logger.debug(content)

        return content

'''
description: translate srt lines into dst language content.
param {*} src_lang - src language
param {*} dst_lang - dst language
param {*} src_lines - src lines by file.readlines()
param {*} split - split src content by sentence or not, some srt item may not be well organized.
param {*} original - if translate result contains origin text.
return {*} res - text strings, can use file.write() into a file.
'''
def translateSrt(src_lines, src_lang="en", dst_lang="zh", split=False, original=False):
    res_content = None

    srt_trans = SrtTranslator(src_lang=src_lang, dst_lang=dst_lang)  
    src_page = srt_trans.constructSrcPageFromLines(src_lines, src_lang=src_lang)
    dst_page = src_page
    if split:
        src_content = srt_trans.extractContentFromPage(src_page)
        dst_page = srt_trans.constructDstPage(src_content)
    
    dst_page = srt_trans.translatePage(dst_lang=dst_lang, srt_page=dst_page)
    res = srt_trans.exportPageToLines(dst_page, origin=original)

    return res

def test():
    # TODO: add test function. Split Unit Test to a folder.
    from Utils.FileFunc import FileRW

    f_reader = FileRW(mod="rt")
    f_writer = FileRW(mod="wt")

    src_path = sys.argv[1]
    dst_path = sys.argv[2]

    srt_lines = f_reader.readFromFile(src_path)
    dst_lines = translateSrt(srt_lines, src_lang="en", dst_lang="zh", split=False, original=True)
    
    f_writer.dumpToFile(dst_path, dst_lines)

if __name__ == "__main__":
    test()


