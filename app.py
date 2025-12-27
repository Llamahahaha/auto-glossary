import streamlit as st
import pymupdf
import re
import wordfreq
import requests

st.title("Auto Glossary")
uploaded = st.file_uploader("Choose pdf file", type="pdf")
if uploaded is not None:
    pdf_bytes = uploaded.read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    for i in range(doc.page_count):
        flag=0
        page = doc.load_page(i)
        text = page.get_text().strip()

        if text:
            words = re.findall(r"[a-zA-Z]+", text.lower())
        else:
            pix = page.get_pixmap()
            pdfbytes = pix.pdfocr_tobytes(language="eng")
            imgpdf = pymupdf.open("pdf", pdfbytes)
            res = imgpdf.load_page(0)
            words = re.findall(r"[a-zA-Z]+", res.get_text().lower())
        memo = []
        for word in words:
            value = wordfreq.zipf_frequency(word, 'en')
            if(value<=2.5) and (word not in memo):
                memo.append(word)
                url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

                response = requests.get(url)
                data = response.json()
                try:
                    for j in range(len(data[0]["meanings"][0]["definitions"])):
                        toPrint = data[0]["meanings"][0]["definitions"][j]["definition"]
                        if j==0:
                            if flag==0:
                                st.write(f"\nPage{i}:")
                                flag=1
                            st.write(f"{word}({j+1}):{toPrint}")
                        else:
                            st.write(f"({j+1}):{toPrint}")
                except KeyError:
                    continue