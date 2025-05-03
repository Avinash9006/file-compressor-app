# 📂 File Compressor & Converter App

A full-stack web app built with **React** and **FastAPI** that allows users to:
- Upload image or PDF files
- Preview files (image or embedded PDF)
- Compress images based on government form specs (SSC, Passport, Aadhaar)
- Convert and download processed files

---

## 🚀 Features

- ✅ Drag & drop file upload with preview  
- 📷 Image preview (JPG, PNG)  
- 📄 PDF viewer in browser  
- 🔧 Backend image compression with FastAPI  
- 💾 Downloadable or base64-encoded output  
- 🔍 Face detection & photo validation *(coming soon)*  
- 🧾 Tailored for Indian government form requirements  

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

```
project-root/
├── frontend/           # React frontend
│   ├── public/
│   ├── src/
│   └── ...
│
├── backend/            # FastAPI backend
│   ├── main.py
│   └── utils/
│       └── compress.py
│
├── .gitignore
├── README.md
└── ...
```

---

## 🛠️ Setup Instructions

### ⚙️ Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### ⚙️ Frontend (React)

```bash
cd frontend/sizemaster
npm install
npm start
```

➡️ This will launch the app at [http://localhost:3000](http://localhost:3000) (or another available port).

To build the app for production:

```bash
npm run build
```

---

## 👨‍💻 Author

Built with ❤️ by **Avinash Singh**  
[GitHub Profile](https://github.com/Avinash9006)
