import pdfplumber
with pdfplumber.open("Master.pdf") as pdf:
    page  = pdf.pages[0]
    text = page.chars[0]
    print(text)