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
  | -f --force           | false     | Force processing of PDFs in directories assumed* to be processed|
  | -v --verbose         | false     | List each file processed |
  | -d --directory       | .\        | Specify the parent directory to process |
  | -q --quality         | 20        | Specify the JPG quality in % |
  | -p --poppler         | C:\\Python\\poppler\\Library\\bin | Specify the poppler bin folder path |
  
  **Additional Notes**
  
  \*For faster performance, and to reduce the list of PDF files reported, the PDF Title Imager assumes that a directory has already been processed if the last PDF has a title page JPG and there are at least as many JPGs as PDFs. However, in the case that a directory is full of unrelated JPGs and the last PDF is one of the only, or one of the few PDFs that has a JPG title page, the `-f` or `--force` parameter can be used to force processing of a directory. 
  
  In verbose mode, the directory and PDF counter are delibertly in reverse order so you can see the progress of the processing. 
 
 
  ### Examples
  
  **Default** 
 
  Only processes PDFs in the current directory. 
  
  `python pdftitleimager`
  
  Output
  ```
  READING DIRECTORIES...
   STATUS | PDF   | SKIP  | ERROR | DIRECTORY
  --------|-------|-------|-------|----------------------------------------------------------------------
   DONE   |     3 |     0 |     0 | #1 .\
  Complete! 3 files processed.
  ```
  
  
  **Process PDFs in all sub directories**
  
  Processes PDFs in the current directory and all subdirectories.
  
  `python pdftitleimager -r`
  
  Output
  ```
  READING DIRECTORIES...
   STATUS | PDF   | SKIP  | ERROR | DIRECTORY
  --------|-------|-------|-------|----------------------------------------------------------------------
   DONE   |     3 |     0 |     0 | #3 .\
   DONE   |     3 |     0 |     0 | #2 .\Test PDF Folder 1\
   DONE   |     2 |     0 |     0 | #1 .\Test PDF Folder 2\
  Complete! 8 files processed.
  ```

  **Reprocessing PDFs**

  The script can be rerun against the same directory. Any PDFs that already have a JPG title page will skipped. e.g. if the JPG title page for `Test PDF 2.1.pdf` was deleted after in our example above, only that PDF would be processed
  
  `python pdftitleimager -r`
  
  Output
  ```
  READING DIRECTORIES...
   STATUS | PDF   | SKIP  | ERROR | DIRECTORY
  --------|-------|-------|-------|----------------------------------------------------------------------
   DONE   |     0 |     3 |     0 | #3 .\
   DONE   |     0 |     3 |     0 | #2 .\Test PDF Folder 1\
   DONE   |     1 |     1 |     0 | #1 .\Test PDF Folder 2\
  Complete! 1 file processed.
  ```
  
  
  **Verbose Output**
  
  Display each file as it is processed. 
  
  `python pdftitleimager -r -v`
  
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
  


  **Force Reprocessing Directories** 
  
  The script skips directories where there is already a JPG title page for the last PDF AND there are at least as many JPGs as PDFs. In the (hopefully) unlikely event that additional PDFs have been added or JPG title pages have been deleted AND there are other unrelated JPGs in the directory, the force parameter can be used to force the script to check each PDF for a JPG title page individually
  
  `python pdftitleimager --recursive --vervose --force`
  
  Output
  ```
  PROCESSING DIRECTORY #3 .\
   Skipped   #3 Test PDF 0.1.pdf ALREADY PROCESSED
   Skipped   #2 Test PDF 0.2.pdf ALREADY PROCESSED
   Skipped   #1 Test PDF 0.3.pdf ALREADY PROCESSED
  PROCESSING DIRECTORY #2 .\Test PDF Folder 1\
   Skipped   #3 Test PDF 1.1.pdf ALREADY PROCESSED
   Skipped   #2 Test PDF 1.2.pdf ALREADY PROCESSED
   Skipped   #1 Test PDF 1.3.pdf ALREADY PROCESSED
  PROCESSING DIRECTORY #1 .\Test PDF Folder 2\
   Processed #2 Test PDF 2.1.pdf
   Skipped   #1 Test PDF 2.2.pdf ALREADY PROCESSED
  Complete! 1 file processed.
  ```
  

  **High Quality JPGs** 
  
  The quality of the JPG title pages can be increased, at the expense of larger file sizes.
  
  `python pdftitleimager --quality 80`
