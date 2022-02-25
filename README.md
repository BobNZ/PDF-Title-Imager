# PDF Title Imager
  Do you have a large (or small) collection of PDFs and would like to see the title page of all the PDFs without having to open them one by one? PDF Title Imager quickly creates a JPG image of the PDFs title page for all your PDFs allowing you to view the cover page of all your PDFs using, for example,  the icon view in Windows Explorer `CTRL + ALT + 1` or `ALT-V` and select your preferred icon view 
  

### INSTALLATION INSTRUCTIONS
 1. Install Poppler 
    ```
    conda install -c conda-forge poppler
    
    or, for Windows users
    
    - Download poppler from https://github.com/oschwartz10612/poppler-windows/releases/
    - Unzip poppler in C:\Python\Poppler
    
 2. Install pdf2image `pip install pdf2image`

### Usage
  By default, PDF Title Imager will process all the PDFs in the current directory and ignore any PDFS that already have PDF title page JPG. This can be overridden with the following optional arguments:
  
  | Parameter            | Default   |  Description |
  | :------------------- | :-------- | :----------- |
  | -r --recursive       | false     | Process all subdirectories |
  | -f --force           | false     | Force processing of all folders PDF Title Imager thinks are already processed |
  | -s --summary         | false     | Only list directories |
  | -d --directory       | .\        | Specify the parent directory to process |
  | -q --quality         | 20        | Specify the JPG quality in % |
  | -p --poppler         | C:\\Python\\poppler\\Library\\bin | Override the poppler bin folder path |
  
  **Additional Notes**
  For faster performance, and to reduce the list of PDF files skipped, the PDF Title Imager assumes that a directory has already been processed if the last PDF has a title page JPG and there are at least as many JPGs as PDFs. However, in the case that a directory is full of unrelated JPGs and the last PDF is one of the only, or few, PDFs that has a JPG title page, the `-f` or `--force` parameter can be used to force the processing of each PDF in the directory. 
  
 
 
  ### Examples
  
  **Default** 
 
  Process the current directory and all subdirectories, ignore files that have a PDF title page JPG.
  
  `python pdftitleimager`
  
  Output
  ```
  DIRECTORIES To PROCESS: 1
  PROCESSING DIRECTORY #1 .\
  Processed #3 Test PDF 0.1.pdf
  Processed #2 Test PDF 0.2.pdf
  Processed #1 Test PDF 0.3.pdf
  Complete! 3 files processed.
  ```
  
  
  **Process PDFs in all sub directories**
  
  PDFs in the current directory and all subdirectories are processed
  
  `python pdftitleimager -r`
  
  Output
  ```
  PROCESSING DIRECTORY #3 .\
  Processed #3 Test PDF 0.1.pdf
  Processed #2 Test PDF 0.2.pdf
  Processed #1 Test PDF 0.3.pdf
  PROCESSING DIRECTORY #2 .\Test PDF Folder 1\
  Processed #3 Test PDF 1.1.pdf
  Processed #2 Test PDF 1.2.pdf
  Processed #1 Test PDF 1.3.pdf
  PROCESSING DIRECTORY #1 .\Test PDF Folder 2\
  Processed #2 Test PDF 2.1.pdf
  Processed #1 Test PDF 2.2.pdf
  Complete! 8 files processed. 
  ```
  
  
  **Summary Output**
  
  Only the directories are displayed when they are processed
  
  `python pdftitleimager -r -s`
  
  Output
  ```
  PROCESSING DIRECTORY #3 .\
  PROCESSING DIRECTORY #2 .\Test PDF Folder 1\
  PROCESSING DIRECTORY #1 .\Test PDF Folder 2\
  Complete! 8 files processed.
  ```
  
  
  **Reprocessing PDFs** 
  
  After processing all sub directories, Title Page JPG for `Test PDF 2.1.pdf` is deleted.
  
  `python pdftitleimager -recursive`
  
  Output
  ```
  SKIPPED    DIRECTORY #3 .\
  SKIPPED    DIRECTORY #2 .\Test PDF Folder 1\
  PROCESSING DIRECTORY #1 .\Test PDF Folder 2\
   Processed #2 Test PDF 2.1.pdf
   Skipped   #1 Test PDF 2.2.pdf ALREADY PROCESSED
  Complete! 1 file processed.
  ```
