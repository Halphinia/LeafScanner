'''
Commandline Version of LeafScanner
'''

import argparse, os
from backend import scanner, renamer

def main():
    parser = argparse.ArgumentParser(
                    prog='LeafScanner',
                    description='Finds the area of leaves and renames the pictures accordingly',
                    epilog='')
    #group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--file', type=str, help="Input path to a single file")
    parser.add_argument('--folder', type=str, help="Input path to a folder")
    args = parser.parse_args()
    if args.folder:
        imgs = folderInput(args.folder)
        for img in imgs:
            print(img)
    elif args.file:
        filePipeline(args.file)

def filePipeline(file):
    print("Single file pipeline")

def folderPipeline(folder):
    folderIn = folderInput(folder)
    scanner.folderLoad(folderIn)

def folderInput(folderPath):
    return [os.path.join(folderPath, f) for f in os.listdir(folderPath) if f.endswith(".jpg") or f.endswith(".hmic") or f.endswith(".png")]

if __name__ == '__main__':
    main()