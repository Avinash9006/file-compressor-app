# 📂 File Compressor & Converter App

A full-stack web app built with **React** and **FastAPI** that allows users to:
- Upload images or PDF files.
- Preview the file (image or embedded PDF).
- Compress images based on government form specs (SSC, Passport, Aadhaar).
- Convert and download processed files.

---

## 🚀 Features

- ✅ Drag & Drop file upload with preview
- 📷 Image preview (JPG, PNG)
- 📄 PDF viewer in browser
- 🔧 Backend compression logic via FastAPI
- 💾 Output in base64 or downloadable format
- 🔍 Face detection & photo validation (coming soon)
- 🧾 Tailored to Indian government form specifications

---

## 🖥️ Tech Stack

### Frontend
- React
- Tailwind CSS
- React Dropzone

### Backend
- FastAPI
- Pillow (image processing)
- PyMuPDF or pdf2image (PDF support)

---

## 📁 Project Structure

project-root/
├── frontend/ # React frontend
│ ├── public/
│ ├── src/
│ └── ...
│
├── backend/ # FastAPI backend
│ ├── main.py
│ └── utils/
│ └── compress.py
│
├── .gitignore
├── README.md
└── ...

---

## 🛠️ Setup Instructions

### ⚙️ Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (React)
cd frontend/sizemaster
npm install
npm start

**This will launch the app at http://localhost:3000 (or another port if 3000 is already in use).**

npm run build
**To build the app for production, run:**



Built with ❤️ by Avinash Singh
[GitHub Profile](https://github.com/Avinash9006)



