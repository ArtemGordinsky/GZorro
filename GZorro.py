# -*- coding: utf-8 -*-
import os
import gzip
from distutils import dir_util
import argparse
import shutil
from Exceptions import ForbiddenFile

_allowedExt = ['.html', '.css', '.js']

class GZorro():
    def __init__(self, input_item):

        if os.path.isfile(input_item):
            try:
                self.f_gzip(input_item)
            except ForbiddenFile as e:
                print(str(e))
                return

        elif os.path.isdir(input_item):
            self.dir_gzip(input_item)


    def f_gzip(self, inputFile, showMessages = 1):

        fileExt = os.path.splitext(inputFile)[1]
        if fileExt not in _allowedExt:
            raise ForbiddenFile("There's usually no point in compressing such files.")

        outputFile = inputFile + '.gz'

        with open(inputFile, 'rb') as file_in:
            with gzip.open(outputFile, 'wb') as file_out:
                file_out.writelines(file_in)

        if showMessages == 1 :
            print('All done. Saved as ' + os.path.basename(outputFile.strip('/')))

        return outputFile


    def dir_gzip(self, input_dir):

        skippedFiles = []
        outputFolder = os.path.join(input_dir, 'Compressed')
        inputFolderSize = 0 # Bytes
        outputFolderSize = 0 # Bytes

        if os.path.isdir(outputFolder) :
            try:
                shutil.rmtree(outputFolder)
            except OSError as e:
                if e.errno == 13:
                    print("Permissions error. Try running as a root.")
                    return
                else:
                    raise

        dir_util.copy_tree(input_dir, outputFolder)

        for root, dirs, files in os.walk(outputFolder):

            for name in files:

                fileExt = os.path.splitext(name)[1]
                if fileExt not in _allowedExt:
                    skippedFiles.append(name)
                    continue

                inputFile = os.path.join(root, name)
                inputFolderSize = inputFolderSize + os.path.getsize(inputFile)

                try:
                    outputFile = self.f_gzip(inputFile, 0)
                except ForbiddenFile as e:
                    skippedFiles.append(name)
                    continue

                outputFolderSize = outputFolderSize + os.path.getsize(outputFile)
                os.rename(outputFile, inputFile)


        if (inputFolderSize == 0):
            print('Do you think giving me an empty folder is cool, huh?')
            return

        kbSaved = round( ((inputFolderSize - outputFolderSize) / 1024), 1)
        print('All done. Saved ' + str(kbSaved) + ' KB. Saved to …/' + os.path.basename(input_dir.strip('/')) + "/Compressed'.")

        if len(skippedFiles) > 0:
            print ('Skipped: ' + str(skippedFiles))


def main():
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = "GZorro compresses any file or folder using GZIP.\nPlease note, it will skip all but 'html', 'css' and 'js' files."
    )
    parser.add_argument(
        'input',
        metavar = '<input>',
        help = 'An input dir or file'
    )

    args = parser.parse_args()

    GZorro(args.input)

if __name__ == '__main__':
    main()