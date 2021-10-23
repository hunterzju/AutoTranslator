import sys
from Srt import SrtItem, SrtPage
from SrtTranslator import SrtTranslator

class FileLoader:
    def __init__(self):
        self.file_lines = None

    def readFromFile(self, path):
        with open(path) as f:
            self.file_lines = f.readlines()
        return self.file_lines

def main(path):
   f_loader = FileLoader()
   srt_trans = SrtTranslator(src_lang="English", dst_lang="Chinese")

   srt_lines = f_loader.readFromFile(path)
   srt_trans.getSrcPageFromLines(srt_lines)
   src_content = srt_trans.extractContentFromPage()
   print(src_content)
   

if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
