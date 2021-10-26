import sys

from Srt import SrtItem, SrtPage
from SrtTranslator import SrtTranslator
from Utils.LogFrame import default_logger

global_logger = default_logger

class FileLoader:
    def __init__(self):
        self.file_lines = None

    def readFromFile(self, path):
        with open(path) as fr:
            self.file_lines = fr.readlines()
        return self.file_lines

class FileDumper:
    def __init__(self) -> None:
        self.encoding = "UTF-8"
        self.mod = "wt"
    
    def setEncoding(self, encode_str):
        self.encoding = encode_str
    
    def setFileMode(self, mode_str):
        self.mod = mode_str

    def dumpToFile(self, path, content):
        with open(path, mode=self.mod, encoding=self.encoding) as fw:
            fw.writelines(content)
        global_logger.info("Write content info file: {}".format(path))
    
    def dumpToFileFromSrtPage(self, path, page):
        with open(path, mode=self.mod, encoding=self.encoding) as fw:
            for item in page.getSrtList():
                fw.write(str(item.getIdx()) + "\n")
                fw.write(item.getTimeline() + "\n")
                for _key in item.content.keys():
                    fw.write(item.content[_key] + "\n")
                fw.write('\n')

def main():
    src_path = sys.argv[1]
    dst_path = sys.argv[2]

    f_loader = FileLoader()

    srt_trans = SrtTranslator(src_lang="en", dst_lang="zh-CN")  
    srt_lines = f_loader.readFromFile(src_path)
    srt_trans.getSrcPageFromLines(srt_lines, src_lang="en")
    src_content = srt_trans.importContentFromPage()
    dst_page = srt_trans.constructDstPage(src_content)
    # res = srt_trans.translateContent(src_content, dst_lang="zh-CN")
    # dst_page = srt_trans.setDstPageFromContent(res, origin=True)
    # srt_trans.setDstPage(dst_page)
    # dst_lines = srt_trans.exportPageToLines()
    
    dst_page = srt_trans.translateContent(dst_lang="zh-CN")
    dst_lines = srt_trans.exportPageToLines(origin=True)
    
    f_dumper = FileDumper()
    f_dumper.dumpToFile(dst_path, dst_lines)
    # f_dumper.dumpToFileFromSrtPage(dst_path, dst_page)

if __name__ == "__main__":
    main()
