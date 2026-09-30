# Jobaround — Open-Source AI Resume Tailoring

This version does NOT require an OpenAI API key.

It uses:
- Flask for the website
- Ollama for local/open-model AI
- PDF/DOCX/TXT resume extraction
- DOCX/PDF output
- Country-specific resume instructions
- A fallback mode if Ollama is unavailable

## 1. Install Python dependencies

```bash
python3 -m pip install -r requirements.txt
```

## 2. Install Ollama

Install Ollama on the machine that will run the AI model.

Then download a model, for example:

```bash
ollama pull qwen2.5:3b
```

Start Ollama if it is not already running:

```bash
ollama serve
```

Ollama's API is normally available at:

```text
http://127.0.0.1:11434
```

## 3. Start Jobaround

```bash
python3 app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 4. Production

For Linux/VPS:

```bash
python3 -m gunicorn --bind 127.0.0.1:5000 app:app
```

Important: Ollama must also be running on a machine accessible to the Flask application. Shared hosting generally cannot run the Ollama model itself.

For a GoDaddy VPS, you can run both Flask/Gunicorn and Ollama on the VPS if its RAM/CPU is sufficient. For GoDaddy shared/cPanel hosting, keep Ollama on another Linux machine/VPS and set:

```bash
export OLLAMA_URL=http://YOUR_AI_SERVER:11434
```

Do NOT expose Ollama publicly without authentication/network controls.

## 5. Optional model change

Create `.env`/environment variables or export:

```bash
export OLLAMA_MODEL=qwen2.5:3b
```

You can replace it with another Ollama model you have installed.

## 6. What the website does

1. User uploads PDF/DOCX/TXT resume.
2. Website extracts text.
3. User selects country and job title.
4. Optional job description can be pasted.
5. Ollama rewrites the resume using country-specific instructions.
6. Website generates PDF and DOCX downloads.
7. If Ollama is unavailable, fallback mode still processes the resume without inventing credentials.

## Security before public launch

Add authentication/rate limiting, file scanning, automatic output cleanup, HTTPS, CSRF protection and privacy/consent controls before accepting sensitive resumes from the public.
