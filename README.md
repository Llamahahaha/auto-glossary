# Auto Glossary

A Streamlit app that scans an uploaded PDF for uncommon/advanced English words and looks up their definitions using the [Free Dictionary API](https://dictionaryapi.dev/).

## What it does

- Upload a PDF through the browser.
- The app extracts text from each page.
- Words are scored by frequency using `wordfreq` (Zipf scale). Words with a frequency score of 2.5 or below (i.e. less common words) are treated as "glossary-worthy."
- Each qualifying word is looked up via the Free Dictionary API, and its definition(s) are displayed under the page number where it appears.

Known limitation: no working OCR

The code contains a fallback path intended to run OCR (via PyMuPDF's `pdfocr_tobytes`) on pages with no extractable text — e.g. scanned or image-only PDFs. **This does not work out of the box.**

- It requires **Tesseract OCR** to be installed separately on the system (it is *not* a Python package and is not covered by `requirements.txt`).
- Even with Tesseract installed, this path is unverified/untested in this project.

**In practice: only text-based PDFs (PDFs with a real, selectable text layer) are supported.** Scanned documents or image-only pages will likely fail or be skipped.

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`:
  - `streamlit`
  - `pymupdf`
  - `wordfreq`
  - `requests`
- An internet connection (for dictionary API lookups)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

This opens the app in your browser (default: `http://localhost:8501`). Upload a PDF and the glossary will be generated page by page.

## Notes / possible improvements

- No caching of dictionary lookups — the same word appearing across multiple documents/runs will always re-query the API.
- No rate-limiting or retry logic for the dictionary API beyond basic error handling.
- The word-frequency threshold (`2.5`) is hardcoded and not configurable via the UI.
- OCR support would need to be properly implemented and documented (including a system dependency on Tesseract) before it can be relied on.
