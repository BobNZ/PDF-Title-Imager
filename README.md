# PDF Title Imager
  Having problems finding the exact PDF file that you are looking for. PDF Title Imager creates a JPG of the title page of all your PDFs allowing you to view your folders with one of the icon views in Windows Explorer.     
  

## INSTALLATION INSTRUCTIONS
 1. Install Poppler 
    ```
    conda install -c conda-forge poppler
    
    or, for Windows users
    
    - Download poppler from https://github.com/oschwartz10612/poppler-windows/releases/
    - Unzip in C:\Python\Poppler
    
 2. Install pdf2image `pip install pdf2image`

## Usage
  By default, PDF Title Imager will process all the PDFs in the current directory and ignore any PDFS that already have PDF title page JPG. This can be overridden with the following optional arguments:
  
  | Parameter            | Default   |  Description |
  | :------------------- | :-------- | :----------- |
  | -r --recursive       | false     | Process all subdirectories as well |
  | -f --force           | false     | Force processing of folders are assumed as already processed  |
  | -v --verbose         | false     | Explicitly lists the PDFs that have been skipped |
  | -d --directory       | .\        | Explicitly specify the parent directory to process rather than using the current directory by default |
  | -q --quality         | 20        | Specify the JPG quality in % |
  | -p --poppler         | C:\\Python\\poppler\\Library\\bin | Override the poppler bin folder path. The default is |
  
 
  ## To Do
  1. Print 1 file and not 1 files processed
  2. When Versose is not on. Just print the directory processed and number of files
  
 
  ## Example
  
  ** Default ** 
  Process the current directory and all subdirectories, ignore files that have a PDF title page JPG
  `python pdftitleimager -r`
  Output
  ```
  DIRECTORIES: 1
  PROCESSING #1 .\
  Processed #3 Test PDF 0.1.pdf
  Processed #2 Test PDF 0.2.pdf
  Processed #1 Test PDF 0.3.pdf
  3 files processed. Complete!

  ** Recursive **
  ```
  DIRECTORIES: 3
  PROCESSING DIRECTORY #3 .\ 3 files processed
  PROCESSING DIRECTORY #2 .\Test PDF Folder 1\ 3 files processed
  PROCESSING DIRECTORY #1 .\Test PDF Folder 2\ 2 files processed
  8 files processed. Complete!
 
  ** Reprocessing Recursive Verbose** 
  ```
  DIRECTORIES: 3
  SKIPPED    DIRECTORY #3 .\
  SKIPPED    DIRECTORY #2 .\Test PDF Folder 1\
  PROCESSING DIRECTORY #1 .\Test PDF Folder 2\
  Processed #2 Test PDF 2.1.pdf
  Skipped   #1 Test PDF 2.2.pdf ALREADY PROCESSED
  1 files processed. Complete!
  
