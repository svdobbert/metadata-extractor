# metadata-extractor
A python-script to extract location-based metadata from crossref-papers.

## How does it work?
The [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) is used to extract metadata from DOIs (including title, year, authors, url and abstract). Then [Selenium](https://www.browserstack.com/selenium) is used to open the URLs in a testing environment and extract the chapter describing the Study environment (by chapter title containing "study"), as well as the keywords (by chapter title containing "keywords"). In this input (chapters, title abstract), the script looks for specific keywords and writes the to a new file.
The keywords.csv file contains the location-based keywords for which the script looks. Keywords can be added to the file but the structure (column names) must be kept.

## Input
When the script is run you are asked to entern the following data:
* Input File: Path to a list (.csv) containing the DOIs of the papers to process. The file has to contain a column labeled "DOI". Default is "./complete_list.csv".
* Output File: Path to an output file (.csv) to which the results are saved. Default is "./results.csv".
* First Row: Row in the input file at which to start processing. Default is 1.
* Last Row: Row in the input file at which to stop processing. Default is the last row in the document.

## Output
* DOI: DOIs of the processed paper.
* Title: Titles of the processed papers (from CrossRef-Metadata).
* Year: Year in which the paper was published (from CrossRef-Metadata).
* Authors: Authors of the paper (first and last name) (from CrossRef-Metadata).
* URL: URL with which the paper can be accessed (from CrossRef-Metadata).
* Keywords: Keywords found in the paper by looking for the word "keyword" in the paper headings (extracted using Selenium).
* Species: List  of focal species, found by looking for italics in the title and abstract.
* Area: Study Area, found by looking for keywords in the Study Area chapter, title and abstract.
* Country:  List  of Countries, found by looking for defined country terms in the Study Area chapter, title and abstract.
* Mountain Range': List  of Mountain Ranges, found by looking for defined country terms in the Study Area chapter, title and abstract.

## Warning
A long list of input DOIs may result in errors. We recommend to break it into parts.