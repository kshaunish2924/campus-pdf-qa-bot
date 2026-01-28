\# Campus PDF Q\&A Bot (Emerging Tools \& Technologies)



A FastAPI backend for uploading campus PDFs, extracting text, and preparing for a RAG-based Q\&A system.



---



\## Tech Stack

\- Python

\- FastAPI

\- Uvicorn (development server)

\- pypdf (PDF text extraction)



---



\## Project Structure

backend/

&nbsp; app/

&nbsp;   core/          # config

&nbsp;   services/      # pdf extraction + storage helpers

&nbsp;   schemas/       # Pydantic response models

&nbsp;   data/

&nbsp;     uploads/     # uploaded PDFs (ignored by git, folder kept)

&nbsp;     texts/       # extracted text files (ignored by git, folder kept)

&nbsp;     metadata.json

&nbsp;   main.py        # FastAPI app

requirements.txt



---



\## Setup (Windows / PowerShell)



1\) Create \& activate virtual environment



python -m venv .venv  

.\\.venv\\Scripts\\Activate.ps1  



2\) Install dependencies



pip install -r requirements.txt  



3\) Run the server



python -m uvicorn backend.app.main:app --reload --port 8010  



Open in browser:



http://127.0.0.1:8010/docs



---



\## API Endpoints (Week 2)



Health Check  

GET /  

Returns service status



Upload PDF (extract + store)  

POST /pdf/upload  

multipart/form-data  

Returns: pdf\_id, extracted text stats, preview



Get PDF by ID  

GET /pdf/{pdf\_id}  

Returns metadata record + text preview



List PDFs  

GET /pdfs  

Returns list of all stored PDF records from metadata.json



---



\## Notes

\- Uploaded PDFs and extracted text files are ignored by git via .gitignore

\- metadata.json remains tracked and stores PDF records



