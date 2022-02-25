# DESCRIPTION
# This script will create an image of the 1st page (title page) of a pdf
#  
#
# INSTALLATION INSTRUCTIONS
# 1. Install Poppler https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
#    a) Download from https://github.com/oschwartz10612/poppler-windows/releases/
#    b) Unzip in C:\Python\Poppler (Bin directory should be c:\Python\Poppler\Library\bin. If not then update popplerPath parameter
# 2. Install pdf2image
#    a) From command line: python -m pip install pdf2image
# 
# Version   Date         Owner   Description 
# 1.0       25 Feb 2022  RJ      Release version
import argparse
from xml.dom.xmlbuilder import Options
from pdf2image import convert_from_path
import glob, os

class PDFTitlePageImager(object):

    def __init__(self, verbose=True, poppler_path='C:\\Python\\poppler\\Library\\bin'):
        self._verbose = verbose
        self._poppler_path = poppler_path
        self._errorList = []
        self._filecount = 0

    def image(self, directory='.', force=False, quality=20, recursive=False):
        dirList = self.getDirList(directory, recursive) 
        dirListCount = len(dirList)
        # self.print("DIRECTORIES TO PROCESS: " + str(dirListCount))
        for dirName in dirList:
            fileList  = self.getFileList(dirName, "pdf")
            imageList = self.getFileList(dirName, "jpg")
            processed = False
            fileListCount = len(fileList)
            imageListCount = len(imageList)
            if not fileList: # Just skip directories that are empty
                self.print("EMPTY      DIRECTORY #" + str(dirListCount) + " " + dirName)
            elif not force and ((fileList[fileListCount-1].replace("pdf","jpg") in imageList) 
                and (fileListCount <= imageListCount)): # If last PDF has an image then assume all PDFs have an image. But double check that there are at least as many images as PDFs
                self.print("SKIPPED    DIRECTORY #" + str(dirListCount) + " " + dirName)
            else:
                self.print("PROCESSING DIRECTORY #" + str(dirListCount) + " " + dirName)
                for fileName in fileList:
                    if fileName.replace("pdf","jpg") in imageList: # If there is an image for the PDF then it has already been processed
                        self.verbose_print(" Skipped   #" + str(fileListCount) + " " + os.path.basename(fileName) + " ALREADY PROCESSED")
                    else:
                        if not processed:
                            self.verbose_print("PROCESSING #" + str(dirListCount) + " " + dirName)
                            processed = True
                        self.verbose_print(" Processed #" + str(fileListCount) + " " + os.path.basename(fileName))
                        self.createImage(fileName, quality)
                    fileListCount -= 1
            dirListCount -= 1
        

    def getDirList(self, sourceDir, recursive):
        # Read all the PDF files in the directory and sort by name
        if recursive:
            fileList = [f for f in sorted(glob.glob(sourceDir + "/**/", recursive=recursive))]
        else:
            fileList = [sourceDir + "\\"]
        return fileList

    def getFileList(self, sourceDir, fileType):
        # Read all the PDF files in the directory and sort by name
        fileList = [f for f in sorted(glob.glob(sourceDir + "*." + fileType))]
        return fileList

    def createImage(self, fileName, quality):
        try:
            pages = convert_from_path(fileName, first_page=1, poppler_path=self._poppler_path, single_file=True)
            pages[0].save(fileName.replace(".pdf",".jpg"), quality=quality)
            self._filecount += 1
        except Exception as e:
            self._errorList += [fileName]
            self.verbose_print("ERROR " + str(e))

    def verbose_print(self, *args):
        if (self._verbose): 
            print(*args)

    def print(self, *args):
        print(*args)
            
    def close(self):
        self.print("Complete! " + str(self._filecount) + f" file{'s'[:self._filecount^1]} processed.")
        if self._errorList:
            self.verbose_print("FAILED TO PROCESS:")
            for fileName in self._errorList:
                self.verbose_print("..." + fileName)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PDF Title Page Imager')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='process subdirectories recursively')
    parser.add_argument('-f', '--force',    action='store_true',
                        help='force checking of directories already processed')
    parser.add_argument('-q', '--quality',  default=20,
                        help='image quality 1-100. 1 lowest to 100 highest level')
    parser.add_argument('-s', '--summary',  action='store_true',
                        help='print additional output')
    parser.add_argument('-d', '--directory', default='.',
                        help='parent directory containing PDFs')
    parser.add_argument('-p', '--poppler',  default='C:\\Python\\poppler\\Library\\bin',
                        help='Popplar bin directory')

    opts = parser.parse_args()
    imager = PDFTitlePageImager(verbose=not opts.summary, poppler_path=opts.poppler)
    imager.image(directory=opts.directory, force=opts.force, quality=int(opts.quality), recursive=opts.recursive)
    imager.close()
