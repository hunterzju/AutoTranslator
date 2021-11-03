import argparse
import os
from Utils.LogFrame import default_logger
from Utils.FileFunc import FileRW, PathManager
from AutoSrt.SrtTranslator import translateSrt
from marko import Markdown
from AutoRst.MdTranslator import TranslatorRender

def parsePrepare():
    parser = argparse.ArgumentParser(prog='Translator', usage="-m srt|rst -i inpath -o outpath")
    parser.add_argument('-m', '--mode', dest='mode', type=str, default="srt", help="translate mode: srt | rst")
    parser.add_argument('-i', '--input', dest='inpath', type=str, required=True, help="input file path.")
    parser.add_argument('-o', '--output', dest='outpath', type=str, required=True, help="output file path")
    parser.add_argument('-s', '--src', dest='src_lang', type=str, default="en", help="translate src language")
    parser.add_argument('-d', '--dst', dest='dst_lang', type=str, default="zh", help="translate dst language")

    return parser

def translateSrtFile(src_lang, dst_lang, src_files, dst_path):
    # TODO: srt translate file.
    freader = FileRW(mod="rt")
    fwriter = FileRW(mod="wt")

    for f in src_files:
        file_name = os.path.basename(f)
        dst_file = os.path.join(dst_path, dst_lang+"-"+file_name)

        default_logger.info(f"translate srt file: {f}")
        src_lines = freader.readLinesFromFile(f)
        trans_res = translateSrt(src_lines=src_lines, src_lang=src_lang, dst_lang=dst_lang, original=True)
        fwriter.dumpToFile(dst_file, trans_res)

def translateMarkdown(dst_lang, src_files, dst_path):
    freader = FileRW(mod="rt")
    fwriter = FileRW(mod="wt")
    md = Markdown(renderer=TranslatorRender)

    for f in src_files:
        file_name = os.path.basename(f)
        dst_file = os.path.join(dst_path, dst_lang+"-"+file_name)

        default_logger.info(f"translate markdown file: {f}")
        src_content = freader.readContentFromFile(f)
        trans_res = md.convert(src_content)
        fwriter.dumpToFile(dst_file ,trans_res)


def main():
    parser = parsePrepare()
    args = parser.parse_args()
    pm = PathManager()

    src_flist = list()
    if pm.isPathFile(args.inpath):
        src_flist.append(args.inpath)
    elif pm.isPathDir(args.inpath):
        src_flist = pm.getFileList(args.inpath)
    else:
        default_logger.error(f"input path error: {args.inpath}")

    dst_path = args.outpath
    if not pm.isPathExists(args.outpath):
        default_logger.warning(f"output path not exists: {args.outpath}")
        os.mkdir(dst_path)

    if args.mode == "srt":
        translateSrtFile(args.src_lang, args.dst_lang, src_flist, args.outpath)
    elif args.mode == "md":
        translateMarkdown(args.dst_lang, src_flist, args.outpath)
    elif args.mode == "rst":
        default_logger.error("Rst file translate not supported.")
        raise ValueError
    else:
        default_logger.error(f"Unknown translate mode {args.mode}")

if __name__ == "__main__":
    main()
