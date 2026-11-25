# AI Resume Analyzer

A beginner-friendly Python + Streamlit project that compares a resume with a job description.

## Features

- Upload PDF, DOCX or TXT resumes.
- Paste a job description.
- Extract text from the uploaded resume.
- Calculate TF-IDF cosine similarity.
- Detect skills using a transparent built-in skill dictionary.
- Show matched skills and skills not found in the resume.
- Display suggestions and download a text report.
- Runs locally; no paid API key or external AI service is required.

> Note: This is an explainable baseline project, not a true LLM-powered system. Its score is an indicative keyword/text similarity score and must not be used as the sole basis for hiring decisions.

## 1. Requirements

- Python 3.10 or newer
- Visual Studio Code
- Internet connection for installing Python packages

Check Python:

```bash
python --version
```

## 2. Open in VS Code

1. Extract the downloaded ZIP file.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Choose the `AI_Resume_Analyzer` folder.
5. Open **Terminal → New Terminal**.

## 3. Create a virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

If PowerShell blocks activation, use Command Prompt terminal and run:

```cmd
venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Run the application

```bash
streamlit run app.py
```

Streamlit will open the app in your browser, usually at:

`http://localhost:8501`

## 6. Test the project

- Open `sample_data/sample_resume.txt`.
- Copy its contents into a `.txt` file and upload it, or use your own PDF/DOCX/TXT resume.
- Open `sample_data/sample_job_description.txt` and paste its contents into the job description box.
- Click **Analyze resume**.

## Project structure

```text
AI_Resume_Analyzer/
│
├── app.py
├── analyzer.py
├── requirements.txt
├── README.md
├── .gitignore
└── sample_data/
    ├── sample_resume.txt
    └── sample_job_description.txt
```

## How the matching works

1. Extract text from the uploaded resume.
2. Extract known skills from both resume and job description.
3. Calculate TF-IDF cosine similarity between the two texts.
4. Calculate job-description skill coverage.
5. Combine the scores:
   - 55% text similarity
   - 45% skill coverage (when skills are detected in the job description)
6. Display matched/missing skills and suggestions.

## Common issues

**`streamlit` is not recognized**

Activate the virtual environment and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**PDF text is empty**

Some PDFs are scanned images. This starter version extracts selectable text and does not include OCR. Use a text-based PDF or add OCR support.

**Module not found**

Make sure the virtual environment is activated and run:

```bash
pip install -r requirements.txt
```

## Possible future improvements

- Add an LLM API for grounded resume summaries.
- Add OCR for scanned resumes.
- Add a vector database and RAG for semantic matching.
- Add candidate consent, access control, secure storage and automatic deletion.
- Add evaluation tests and human review workflows.
