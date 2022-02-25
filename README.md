#PDF Title Imager
Having problems finding the exact PDF file that you are looking for. PDF Title Imager creates a JPG of the title page of all your PDFs allowing you to view your folders with one of the icon views in Windows Explorer.     

By default, PDF Title Imager will process all the PDFs in the current directory and ignore any PDFS that already have PDF title page JPG. This can be overridden with the following arguments:
'-r --recursive'  Process all subdirectories as well
'-f --force'      Force processing of folders already processed. PDF Title Imager assumes that a directory is already processed if there is a PDF title page for the last PDF in the directory and there are at least as many JPGs and PDFs
'-v --verbose'    Explicitly lists the PDFs that have been skipped
'-d --directory'  Explicitly specify the parent directory to process rather than using the current directory by default
'-q --quality'    Specify the JPG quality. The default is 20(%)
'-p --poppler'    Override the poppler bin folder path. The default is 'C:\\Python\\poppler\\Library\\bin'
  

##INSTALLATION INSTRUCTIONS
 1. Install Poppler 'conda install -c conda-forge poppler', or
    - Download poppler from https://github.com/oschwartz10612/poppler-windows/releases/
    - Unzip in C:\Python\Poppler
 2. Install pdf2image 'pip install pdf2image'
