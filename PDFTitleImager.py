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
        self.print("READING DIRECTORIES..." )
        dirList = self.getDirList(directory, recursive) 
        dirListCount = len(dirList)
        for dirName in dirList:
            fileList  = self.getFileList(dirName, "pdf")
            imageList = self.getFileList(dirName, "jpg")
            fileListCount = len(fileList)
            imageListCount = len(imageList)
            processed = 0

            if not fileList: # Just skip directories that are empty
                self.print("EMPTY    DIRECTORY #" + str(dirListCount) + " " + dirName)
            elif not force and ((fileList[fileListCount-1].replace("pdf","jpg") in imageList) 
                and (fileListCount <= imageListCount)): # If last PDF has an image then assume all PDFs have an image. But double check that there are at least as many images as PDFs
                self.print("SKIPPED  DIRECTORY #" + str(dirListCount) + " " + dirName)
            else:
                self.verbose_print("PROCESSING DIRECTORY #" + str(dirListCount) + " " + dirName)
                self.summary_print("     PROCESSING DIRECTORY #" + str(dirListCount) + " " + dirName)
                for fileName in fileList:
                    if fileName.replace("pdf","jpg") in imageList: # If there is an image for the PDF then it has already been processed
                        self.verbose_print(" Skipped   #" + str(fileListCount) + " " + os.path.basename(fileName) + " ALREADY PROCESSED")
                    else:
                        self.verbose_print(" Processed #" + str(fileListCount) + " " + os.path.basename(fileName))
                        self.createImage(fileName, quality)
                        processed += 1
                    self.summary_print(f"{fileListCount: >4d}")
                    fileListCount -= 1
                if not self._verbose:
                    self.print(f"{processed: >4d}-PROCESSED ")
            dirListCount -= 1
        

    def getDirList(self, sourceDir, recursive):
        # Read all the PDF files in the directory and sort by name
        if recursive:
            fileList = [f for f in sorted(glob.glob(sourceDir + "/**/", recursive=recursive))]
        else:
            fileList = [sourceDir + "\\"]
        return fileList

    def getFileList(self, sourceDir, fileType):
        try:
            # Read all the PDF files in the directory and sort by name
            fileList = [f for f in sorted(glob.glob(sourceDir + "*." + fileType))]
            return fileList
        except:
            # Added due to crash error in glob.glob; directories with brackets https://bugs.python.org/issue738361
            return []

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

    def summary_print(self, *args):
        if (not self._verbose): 
            print(*args, end="\r", flush=True)

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
