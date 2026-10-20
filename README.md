# AI Text Summarizer 📝

A simple AI-powered web application that creates shorter summaries from longer English text. It uses Streamlit for the interface and a pretrained DistilBART model through Hugging Face Transformers.

## Features

- Generate short, medium, or long summaries
- Show original and summary word counts
- Estimate the percentage of word reduction
- Download the summary as a `.txt` file
- Simple interactive web interface
- Reuses the loaded model with Streamlit caching

## Tech Stack

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- `sshleifer/distilbart-cnn-12-6`

## Project structure

```text
AI-Text-Summarizer/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## Run locally

### 1. Install Python

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/).

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the app

```bash
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`.

The pretrained model is downloaded automatically on the first run. This needs an internet connection and can take several minutes.

## Upload to GitHub

1. Create a new repository named `AI-Text-Summarizer` at [github.com/new](https://github.com/new).
2. Open a terminal inside this project folder.
3. Run:

```bash
git init
git add .
git commit -m "Add AI text summarizer project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the HTTPS URL of your own GitHub repository.

## Optional: Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create an app and select your repository, `main` branch, and `app.py`.

Large AI dependencies and model downloads can take time, and the hosting environment must have enough memory.

## Limitations

- The selected model is primarily designed for English news-style summarization.
- AI-generated summaries may miss details or contain inaccuracies. Check important information against the original text.
- Very long text is processed in chunks, so the summary may not preserve every relationship across sections.
- This project is a demo and is not a substitute for checking the original source.

## Model information

Model: [`sshleifer/distilbart-cnn-12-6`](https://huggingface.co/sshleifer/distilbart-cnn-12-6)

Review the model card and license/usage conditions before redistribution or public deployment.
