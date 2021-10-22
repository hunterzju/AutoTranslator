import sys
from Srt import SrtItem, SrtPage
from SrtTranslator import Translator

class FileLoader:
    def __init__(self):
        self.fp = None

def main():
   origin_page = SrtPage()
   new_page = SrtPage()

if __name__ == "__main__":
    path = sys.argv[1]
    print(path)
