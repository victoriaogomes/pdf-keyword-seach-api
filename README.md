# 📄 PDF Keyword Search API
This is an application designed to **search for keywords inside PDF files** through an API request, and save the PDFs with
the searched words highlighted.

---

## 🚀 Features

- 🔍 Keyword search in PDF folders
- 📚 Save a new PDF file in a specified folder with the searched keywords highlighted 
- 📝 Save a file with the information regarding the all the processed PDF files, containing:
  - Title
  - File name
  - Amount of pages
  - Total amount of keywords found
  - Amount of keywords detailed by keyword
- 📦 Supports multiple output formats (i.e., json and xlsx)

---

## 📂 Project Overview

### ▶️ Execution guide
To run this project, you need to install:
1. [Python 3.13](https://www.python.org/downloads/release/python-3130/) or over
2. An IDE (we recommend [IntelliJ](https://www.jetbrains.com/idea/download/?section=windows) or [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows))

After setting up everything, and installing the libraries required by the API, you just have to run the **main.py** file.

### 👩🏻‍💻 Technologies used
This project was developed using:
- [Python 3.13](https://www.python.org/downloads/release/python-3130/) 
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- [FastAPI Framework](https://fastapi.tiangolo.com/)
- [OpenpyXl](https://openpyxl.readthedocs.io/en/stable/)

### 🏛️ Architecture: Netflix Hexagonal Pattern

This project follows the **Netflix Hexagonal Architecture**, a modern evolution of the classic Hexagonal / Ports & Adapters approach.  
The goal is to create a highly modular, testable, and maintainable system where **business logic is fully isolated** from frameworks, UI layers, and external services.

To learn more about it: [Ready for changes with Hexagonal Architecture - by Netflix Technology Blog | Netflix TechBlog](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749)


## 🛠️ Endpoints

---

## 1. 🔍 POST `/search_keywords`

Searches for keywords inside PDF files stored in a given folder.

### Request body parameters
This endpoint expects the following three parameters in the request body:
- **keywords**: a list containing all the keywords that the application must search for in the PDF files
- **pdf_folder_path**: a path to a folder where all PDF files that must be processed are stored
- **output_path**: a path to a folder in which the application must save all PDFs that have at least one of the keywords

Moreover, there are three optional parameters:
- **include_subfolders**: specifies if the application must also look for PDF files in the subfolders of the folder received in the "pdf_folder_path parameter", and has a default value of `True`
- **ignore_reference_section**: specifies if the application must ignore the references section when looking for the received keywords, or if it must search in this section as well, and has a default value of `True`
- **output_format**: selects if the output of the PDF processing should be saved in `xlsx` or in a `json` file, and has a default value of of `xlsx`

### **Curl example**
```bash
    curl --location 'http://127.0.0.1:8000/search' \
    --header 'Content-Type: application/json' \
    --data '{
        "keywords": ["Generative AI", "Large Language Models", "LLM", "LLMs", "Gemini", "Copilot", "ChatGPT", "LLaMA", "Prompt"],
        "pdfFolderPath": "C:/Users/example/OneDrive/Documents",
        "outputPath": "C:/Users/Processed papers",
        "include_subfolders": true,
        "ignore_reference_section": true
    }'
```
