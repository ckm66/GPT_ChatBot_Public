from PyPDF2 import PdfReader

reader = PdfReader("Homework1.pdf")

print(type(reader))
for page in reader.pages:
    print(page.extract_text())