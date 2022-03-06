import argparse
from xml.dom.xmlbuilder import Options
from pdf2image import convert_from_path
import glob, os

class PDFTitlePageImager(object):

    def __init__(self, summary=False, poppler_path='C:\\Python\\poppler\\Library\\bin'):
        self._summary = summary
        self._poppler_path = poppler_path
        self._errorList = []
        self._filecount = 0 

    def image(self, directory='.', force=False, quality=20, recursive=False):
        self.print("READING DIRECTORIES..." )
        dirList = self.getDirList(directory, recursive) 
        dirListCount = len(dirList)
        dirListWidth = len(str(dirListCount))
        
        self.summary_print(" STATUS | PDF   | SKIP  | ERROR | DIRECTORY ")
        self.summary_print(f"--------|-------|-------|-------|---------------------------------------------------------------------------")
        for dirName in dirList:
            fileList  = self.getFileList(dirName, "pdf")
            imageList = self.getFileList(dirName, "jpg")
            fileListCount = len(fileList)
            imageListCount = len(imageList)
            filesPDF = 0
            filesSkipped = 0
            filesError = 0

            self.summary_overwrite(f"        |       |       |       | {' ':<76s}")
            self.summary_overwrite(f"        |       |       |       | #{dirListCount:<{dirListWidth}d} {dirName[:69]}")
            if not fileList: # Just skip directories that are empty
                self.verbose_print(f"EMPTY    DIRECTORY #{dirListCount:03d} {dirName}")
                self.summary_overwrite(f" EMPTY ")
            elif not force and ((fileList[fileListCount-1].replace(".pdf",".jpg").upper() in (image.upper() for image in imageList)) and (fileListCount <= imageListCount)): # If last PDF has an image then assume all PDFs have an image. But double check that there are at least as many images as PDFs
                self.verbose_print(f"SKIPPED  DIRECTORY #{dirListCount:03d} {dirName}")
                self.summary_overwrite(f" SKIP  ")
            else:
                self.verbose_print(f"PROCESS  DIRECTORY #{dirListCount:03d} {dirName}")
                complete = 0.0
                for fileName in fileList:
                    self.summary_overwrite(f"        |       |       |       | {' ':<76s}")
                    self.summary_overwrite(f" {complete:4.0%}   | {filesPDF:>5d} | {filesSkipped:>5d} | {filesError:>5d} | #{dirListCount:<{dirListWidth}d} {dirName[:69]}" )
                    if fileName.replace("pdf","jpg").upper() in (image.upper() for image in imageList): # If there is an image for the PDF then it has already been filesPDF
                        self.verbose_print(f"         Skipped   #{fileListCount:03d}  {os.path.basename(fileName)} ALREADY PROCESSED")
                        filesSkipped += 1
                    else:
                        self.verbose_print(f"         Process   #{fileListCount:03d}  {os.path.basename(fileName)}")
                        processed = self.createImage(fileName, quality)
                        if processed:
                            filesPDF += 1
                        else:
                            filesError += 1                            
                            self.verbose_print("ERROR " + self._errorList[len(self._errorList)-1])
                    fileListCount -= 1
                    complete = (filesPDF+filesSkipped+filesError)/len(fileList)
                    
                self.summary_print(f" DONE   | {filesPDF:>5d} | {filesSkipped:>5d} | {filesError:>5d} | #{dirListCount:<{dirListWidth}d} {dirName[:69]}")
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
            pages = convert_from_path(fileName, first_page=1, poppler_path=self._poppler_path, single_file=True, thread_count=4)
            pages[0].save(fileName.replace(".pdf",".jpg"), quality=quality)
            self._filecount += 1
            return True
        except Exception as e:
            self._errorList += [fileName + ' ' + str(e)] 
            return False

    def verbose_print(self, *args):
        if not self._summary: 
            print(*args)

    def summary_overwrite(self,  *args):
        if self._summary: 
            print(*args, end="\r", flush=True)

    def summary_print(self, *args):
        if self._summary: 
            print(*args, flush=True)

    def print(self, *args):
        print(*args)
            
    def close(self):
        self.print(f"Complete! {self._filecount} file{'s'[:self._filecount^1]} processed. {' ':<80s}")
        if self._errorList:
            self.print("")
            self.print("FAILED TO PROCESS:")
            for fileName in self._errorList:
                self.print(fileName)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PDF Title Page Imager')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='process subdirectories recursively')
    parser.add_argument('-f', '--force',    action='store_true',
                        help='force checking of directories already processed')
    parser.add_argument('-q', '--quality',  default=20,
                        help='image quality 1-100. 1 lowest to 100 highest level')
    parser.add_argument('-v', '--verbose',  action='store_true',
                        help='print additional output')
    parser.add_argument('-d', '--directory', default='.',
                        help='parent directory containing PDFs')
    parser.add_argument('-p', '--poppler',  default='C:\\Python\\poppler\\Library\\bin',
                        help='Popplar bin directory')

    opts = parser.parse_args()
    imager = PDFTitlePageImager(summary=not opts.verbose, poppler_path=opts.poppler)
    imager.image(directory=opts.directory, force=opts.force, quality=int(opts.quality), recursive=opts.recursive)
    imager.close()
