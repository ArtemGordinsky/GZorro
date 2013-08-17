import os
import gzip
from distutils import dir_util
import argparse
import shutil

_allowedExt = ['.html', '.css', '.js']

class GZorro():
    def __init__(self, input_item):

        if os.path.isfile(input_item):
            self.f_gzip(input_item)

        elif os.path.isdir(input_item):
            self.dir_gzip(input_item)


    def f_gzip(self, input, output=input):

        fileExt = os.path.splitext(input)[1]
        if fileExt not in _allowedExt:
            print("There's usually no point in compressing such files.")
            return

        with open(input, 'rb') as file_input:
            with gzip.open(output, 'wb') as file_output:
                file_output.writelines(file_input)


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
                inputFolderSize = inputFolderSize + os.path.getsize(inputFile);

                outputFile = os.path.join(root, name + '.gz');

                with open(inputFile, 'rb') as file_in:

                    with gzip.open(outputFile, 'wb') as file_out:
                        file_out.writelines(file_in)
                        outputFolderSize = outputFolderSize + os.path.getsize(outputFile)
                        os.rename(outputFile, inputFile)


        if (inputFolderSize == 0):
            print 'Do you think giving me an empty folder is cool, huh?'
            return


        print('All done. Saved ' + str(((inputFolderSize - outputFolderSize) / 1024)) + " KB. Look in '/" + os.path.basename(input_dir.strip('/')) + "/Compressed' for your files.")

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