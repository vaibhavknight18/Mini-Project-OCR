# 🧮 OCR Equation Solver Web App

This project is a web-based application that allows users to **upload or draw images of mathematical equations**, extract the text using **Google Cloud Vision OCR**, and solve them using **SymPy** in Python.

---

## 🚀 Features

- ✏️ Upload or draw equations on canvas
- 🔍 OCR using Google Cloud Vision API
- 🧠 Smart preprocessing for better equation recognition
- 🧮 Solves algebraic equations using SymPy
- 💡 Currently supports equations **only in variable `y`**
- 🖼️ Image binarization for enhanced accuracy
- 🔐 Secure `.env` based API key management

---

## 🖥️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **OCR:** Google Cloud Vision API
- **Math Solver:** SymPy
- **Image Processing:** OpenCV, PIL
- **API Key Management:** Python-dotenv

---

## 🛠️ Setup Instructions

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/vaibhavknight18/OCR-Mini-Project.git
cd OCR-Mini-Project

python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
pip install Flask opencv-python pillow numpy sympy google-cloud-vision python-dotenv

touch .env
GOOGLE_API_KEY=your_api_key_here
python app.py

OCR-Mini-Project/
│
├── app.py                    # Main Flask app
├── solve_equation_file.py   # Equation solver logic (only supports variable y)
├── templates/
│   ├── homepage.html
│   ├── uploadimage.html
│   └── canvasimage.html
├── static/
│   └── equation.png          # Uploaded/drawn image
├── .env                      # API key (excluded from Git)
├── requirements.txt
└── README.md

🙋‍♂️ Author
vaibhavknight18
GitHub: @vaibhavknight18
