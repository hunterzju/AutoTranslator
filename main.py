import argparse
from logging import ERROR
from Utils.LogFrame import default_logger
from AutoSrt import SrtTranslator

def parsePrepare():
    parser = argparse.ArgumentParser(prog='Translator', usage="-m srt|rst -i inpath -o outpath")
    parser.add_argument('-m', '--mode', dest='mode', type=str, default="srt", help="translate mode: srt | rst")
    parser.add_argument('-i', '--input', dest='inpath', type=str, required=True, help="input file path.")
    parser.add_argument('-o', '--output', dest='outpath', type=str, required=True, help="output file path")
    parser.add_argument('-s', '--src', dest='src_lang', type=str, default="en", help="translate src language")
    parser.add_argument('-d', '--dst', dest='dst_lang', type=str, default="zh", help="translate dst language")

    return parser

def translateSrtFile():
    # TODO: srt translate by file.
    pass

def translateSrtDir():
    # TODO: srt translate by folder
    pass

def main():
    parser = parsePrepare()
    args = parser.parse_args()

    translator = None
    if args.mode == "srt":
        translator = SrtTranslator(args.src_lang, args.dst_lang)
    elif args.mode == "rst":
        default_logger.error("Rst file translate not supported.")
        raise ValueError


if __name__ == "__main__":
    main()
