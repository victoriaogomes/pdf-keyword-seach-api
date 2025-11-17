# 📄 PDF Keyword Search API
![Python](https://img.shields.io/badge/python-3.13-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)



This application helps researchers automatically filter and analyze keywords in conference and journal papers. It searches 
for specified keywords inside PDF files through an API request and generates enhanced versions of the PDFs with all matched 
terms highlighted. In addition, it builds a Table of Contents (TOC) section that groups every keyword found and summarizes 
the total number of occurrences for each one.

---

## 🚀 Features

- 🔍 Search for keywords in PDF folders 
  - Scan entire PDF folders to find occurrences of specified keywords, allowing the user to customize if subfolders
  should also be considered in the search
- 📚 Generate enhanced PDFs 
  - Save a new PDF for each processed file in a specified output folder with all matched keywords highlighted
  - Adds a Table of Contents (TOC) to each PDF grouping each keyword occurrence
- 📝 Generate a detailed summary file 
  - Save a file summarizing all processed PDFs, including:
    - Title 
    - File name 
    - Number of pages 
    - Total keywords found 
    - Detailed count of each keyword by page 
- 📦 Supports multiple output formats 
  - Export the summary in JSON or Excel (.xlsx) formats for easy analysis 
- ⚡ API-driven processing 
  - Perform keyword searches programmatically through an API request, allowing automation and integration in larger workflows.
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
