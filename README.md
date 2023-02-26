# RESolution
Projects were created and tested using Visual Studiy 2022 Community Edition. All build, run, test instructions are intended for use in VS Studio 2022 Comm Edition. 

## PdfREParser
PdfREParser is a python project that reads a PDF file and converts it into JSON.

### Highlights
1. Performs binary read on pdf files and parses into JSON format.
2. Decompresses compressed object streams in order adds the streamed objects to the generated JSON.
3. Detects embedded files and extracts them during parsing.
4. Attempts to decode data streams into readable ascii or Unicode.  
5. All data streams are converted to char64 encoding for later analysis.
6. All data streams have an MD5 hash generated which is included in the JSON file.
7. Takes advantage of the PDF XREF convention which allows the program to "fast foward" across large data streams.
8. Retrains original raw meta data and data streams for further analysis.
9. Attempts to translate proprietary character tables using embedded Unicode font directives for text/string searches.  This functionality is still experimental.

#### Run instructions
PdfREParser.py is the primary controller of the project. The script takes one argument, which is the relative file path of the PDF file to be parsed.

#### Test intructions
Some unit tests are included in the /tests folder, but these need to be expanded upon.  VS Studio has issues with debuging python in test mode.  Many PDF examples that
were used for initial testing are included in the /examples folder.

## REAnalyzer
The purpose of the python based REAnalyzer is to take the tokenzied source artifacts and analyze them by running configurable rules against the JSON.  The project currently only 
is designed to process PDF files, but any file format could be incorporated as long as it is feasible to be represented in JSON.

### Highlights
1. Reads JSON file output from parser (PdfREParser). Other types of source artifacts could be input in the future. 
2. Uses recursive tree processing to parse object relationship and identifies orphan objects.
3. Executes rules against input file, and generates a rules execution summary file.

#### Run instructions
analyzer.py is the main controller of REAnalyzer. The file should be an output of the Parser program like PdfREParser.  The JSOn file should indicate what type analyzer
should be used for the input file. Currently only PDF is supported.

#### Test instructions
Unit tests need to be created for this project as they were not initially created during prototyping.  Output files from PdfREParser can be used for testing purposes.

## Reviewer
Reviewer is a ReactJS web based application that gives the analyst a graphical user interface in order to inspect the rules execution summary from REAnalyzer.  In 
addtion, the application can be used to further inspect the tokenized PDF (or other source) file. The current project uses nodejs to build and run the project on a local
http server.  You must install NodeJS to run this project.

### Highlights
1. Uses the Palantir open source web GUI component library blueprintjs.
2. Provides three basic views:  rules excecution summary, object tree view, and object pool.
3. Objects can be "drilled into" in order to browse and perform reverse engineering activities. 

#### Run intsructions
First install npm (npm install)
From command line, npm run start.  Application will attempt to start at http://localhost:3000

Output from REAnalyzer must copied into the /public folder.  The files.json file must edited to include copied files.  Copied files will included rules execution summary
and object pool, all in JSON format. Existing examples are included in the files.json file.

