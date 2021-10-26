import sys
import os
from AutoSrt import DEBUG
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_PATH)

import time
import random
from Srt import SrtItem, SrtPage, StringOPs
# from google.cloud import translate_v2 as Translator
from pygoogletranslation import Translator
from Utils.LogFrame import default_logger, LoggerExt

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
        self.trans_client = Translator()
    
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
    def getSrcPageFromLines(self, lines, src_lang=None):
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
    
    '''
    description: extract content from src page items.
    param {*} self
    return {*} content - raw text in src language.
    '''
    def importContentFromPage(self):
        content = ""

        if self.src_page == None:
            trans_logger.error("translator src page is None")
            return None

        for item in self.src_page.getSrtList():
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

            self.dst_page.appendSrt(dst_item)
            write_idx = idx
        
        # if split origin item is more than src srt item, create new item with last timeline in src.
        if write_idx < origin_len:
            for idx in range(write_idx, origin_len):
                dst_item = SrtItem(idx=idx, timeline=src_list[-1].getTimeline())
                dst_item.addContent(self.src_lang, origin_text_list[idx].strip())

                if DEBUG:
                    trans_logger.debug(str(idx) + str(dst_item.content))

                self.dst_page.appendSrt(dst_item)
                write_idx = idx
        
        return self.dst_page

    '''
    description: translate from Src content to Dst content by item.
    param {} dst_lang - dst lanuage
    return {*} dst_page - dst page
    res - Translated object in pygoogletranslation, origin for src language, text for dst language.
    reflink:https://github.com/Saravananslb/py-googletranslation
    '''
    def translateContent(self, dst_lang=None):
        if self.trans_client == None:
            trans_logger.error("No translator Found.")
            sys.exit(-1)
        if dst_lang == None:
            trans_logger.warning("Translator dst language not set. Use default language {}".format(self.dst_lang))
            dst_lang = self.dst_lang

        for idx, item in enumerate(self.dst_page.getSrtList()):
            if item.getContent(self.src_lang) in ['' or None]:
                continue
            res = self.trans_client.translate(item.getContent(self.src_lang), dest=self.dst_lang)
            if DEBUG:
                trans_logger.debug(str(idx) + ":" + str(res))
            self.dst_page.srt_list[idx].addContent(self.dst_lang, res.text)

            # avoid ip banned by google, FIXME: use proxy instead.
            if idx % 5 == 0:
                time.sleep(random.randrange(10,20))
        
        return self.dst_page

    # TODO: split translate result and set into Dst srt page
    '''
    description: convert translate result to Dst srt page form.
    param {*} self - class object
    param {*} translated_res - Translated object from pygoogletranslation.
    param {*} origin - if res contains origin language.
    return {*}  res_pag - dst srt page.
    '''
    def setDstPageFromContent(self, translated_res, origin=False):
        if translated_res is None:
            trans_logger.error("translate result is None object.")
            return None
        
        if self.dst_page is None:
            trans_logger.warning("translator dst page is None. Creat a new page.")
            new_page = SrtPage(srt_list=[])
            self.setDstPage(new_page)

        dst_text = translated_res.text
        # if DEBUG:
        #     trans_logger.debug(dst_text)
        if origin:
            origin_text = translated_res.origin
            if DEBUG:
                trans_logger.debug(origin_text)
        
        src_list = self.src_page.getSrtList()
        src_len = len(src_list)


        trans_text_list = g_str_ops.Spliter(content=dst_text, split_sbls=r"[。|！|？]")
        trans_len = len(trans_text_list)
        if origin:
            origin_text_list = g_str_ops.Spliter(content=origin_text, split_sbls=r"[.|!|?]")
            origin_len = len(origin_text_list)
        
        write_idx = 0
        for idx in range(src_len):
            dst_item = SrtItem(idx=src_list[idx].getIdx(), timeline=src_list[idx].getTimeline())
            if idx < trans_len:
                dst_item.addContent(trans_text_list[idx].strip() + "\n")
            if origin and idx < origin_len:
                dst_item.addContent(origin_text_list[idx].strip() + "\n")
            dst_item.addContent("\n")

            if DEBUG:
                trans_logger.debug(str(idx) + ":" + str(dst_item.content))

            self.dst_page.appendSrt(dst_item)
            write_idx = idx
        
        # if translate srt item is more than origin srt item, create new item with last timeline in origin.
        if write_idx < trans_len:
            for idx in range(write_idx, trans_len):
                dst_item = SrtItem(idx=idx, timeline=src_list[-1].getTimeline())
                dst_item.addContent(trans_text_list[idx].strip() + "\n")
                if origin and idx < origin_len:
                    dst_item.addContent(origin_text_list[idx].strip() + "\n")
                dst_item.addContent("\n")

                if DEBUG:
                    trans_logger.debug(dst_item.content)

                self.dst_page.appendSrt(dst_item)
                write_idx = idx
        
        if origin and write_idx < origin_len:
            for idx in range(write_idx, origin_len):
                dst_item = SrtItem(idx=idx, timeline=src_list[-1].getTimeline())
                dst_item.addContent(origin_text_list[idx].strip() + "\n")

                if DEBUG:
                    trans_logger.debug(dst_item.content)

                self.dst_page.appendSrt(dst_item)
        
        return self.dst_page

    # TODO: convert dst page struct into lines to write to file.
    '''
    description: export dst page into content.
    param {*} self
    param {*} origin
    return {*}
    '''
    def exportPageToLines(self, origin=False):
        content = ""

        for item in self.dst_page.getSrtList():
            content += str(item.getIdx()) + "\n"
            content += item.getTimeline() + "\n"
            if origin:
                content += item.getContent(self.src_lang) + "\n"
            content += item.getContent(self.dst_lang) + "\n"
        
            if DEBUG:
                trans_logger.debug(content)
        
        return content

def test(path):
    # TODO: add test function. Split Unit Test to a folder.
    pass

if __name__ == "main":
    path = sys.argv[1]
    test(path)
    

