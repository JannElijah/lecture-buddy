# 🧠 Lecture Buddy AI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%202.0-8E75B2)

Lecture Buddy is an AI-powered study assistant designed to help students digest complex lecture slides instantly. By uploading a PDF, the application uses Google's Gemini 2.0 model to generate concise summaries and interactive quizzes, transforming passive reading into active learning.

![App Screenshot](https://via.placeholder.com/1200x600?text=Please+Upload+A+Screenshot+of+Your+App+Here)
-> Note: Replace the image link above with a screenshot of your running application!-

 🚀 Key Features

- -🤖 Instant Analysis: Uses Google Gemini 2.0 Flash for lightning-fast text processing.
- 📄 PDF Support: specific handling for lecture slide decks via `PyPDF2`.
- 📝 Smart Summaries: Generates structured, bullet-point notes using Markdown formatting.
- ❓ Dynamic Quizzes: Creates custom multiple-choice questions with adjustable difficulty (Easy/Medium/Hard).
- 👁️ Anti-Spoiler Mode: Interactive "Hidden Answer Key" prevents spoilers during self-testing.
- 🎨 Modern UI: A custom-styled interface featuring Dark Mode, Glassmorphism, and Gradient Accents.

 🛠️ Tech Stack

-   Frontend: Streamlit (Custom CSS styling)
-   Backend: Python 3.x
-   AI Model: Google Generative AI (Gemini 2.0 Flash)
-   Data Processing: PyPDF2

 📦 How to Run Locally

1.  Clone the repository:
    bash
    git clone https://github.com/yourusername/lecture-buddy.git
    cd lecture-buddy
    

2.  Create a Virtual Environment (Optional but recommended):
    bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    

3.  Install dependencies:
    bash
    pip install -r requirements.txt
    

4.  Run the application:
    bash
    streamlit run app.py
    

 🔑 Configuration

To use the AI features, you need a Google Gemini API Key.
1.  Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Enter the key in the app's sidebar (it is not saved permanently for security).

 👨‍💻 Author

Jann Elijah B. Limpiado
-3rd Year IT Student-
-   [LinkedIn Profile](www.linkedin.com/in/jannlimpiado)
-   [GitHub Profile](https://github.com/JannElijah)


-Created for Portfolio 2025-
