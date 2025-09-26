# EPFL URL to PDF Converter (bêta)

Unofficial tool for extracting text from a page or news item on the EPFL website and exporting it to PDF format.
Should/could also work on other WordPress-based sites.

## Install

To run this tool, you'll need Python 3.x and the following libraries:

```bash
pip install flask beautifulsoup4 requests reportlab
```

And then...
* Create a directory
* Place the app.py file in your project directory
* Add the index.html into a "templates" directory

## Run Locally
```bash
python3 app.py
```
* Open your web browser and go to http://localhost:5000 (default port)
* Enter one or more URLs (each on a new line) in the form
* Click "Generate" to create a PDF

## Usage
* The tool extracts text from the main content area of a webpage (using the main class)
* It supports extracting from EPFL websites and WordPress-based sites
* The output PDF will be saved as output.pdf and automatically downloaded

## Limitations
Still have to find how to:
* display elements in bold in the text
* underline links
* for sure a lot of other things, but well.. that's a start
