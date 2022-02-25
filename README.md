# DESCRIPTION
 This script will create an image of the 1st page (title page) of a pdf. The script will process all files in the current
 directory and all files in the subdirectories if -recursive argument is included

 PDFs that already have an title page image will always be skipped. To reprocess these PDFs, just delete the related JPG file
 Directories where a JPG exists for the last PDF (and there are at least as many JPGs as PDFs) will be skipped unless the -force argument is used
 For details on all the files skipped, use the -verbose argument
  

 INSTALLATION INSTRUCTIONS
 1. Install Poppler - conda install -c conda-forge poppler, or 
    a) Download from https://github.com/oschwartz10612/poppler-windows/releases/
    b) Unzip in C:\Python\Poppler (Bin directory should be c:\Python\Poppler\Library\bin. If not then update popplerPath parameter
 2. Install pdf2image - pip install pdf2image
