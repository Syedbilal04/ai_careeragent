# AI Career Agent

> Tell it what you're interested in, and it suggests **3 career options**, the **key skills and expected salary range (INR)** for each, and a **free learning resource** per career. Built with FastAPI and LangChain on OpenAI models.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white)

## ✨ Features

- **Three-step LangChain pipeline** (`app/agents/career_agent.py`):
  1. **Interest chain:** interests → 3 numbered career suggestions
  2. **Skill chain:** careers → top 3 skills + expected salary range in INR
  3. **Resource chain:** careers → one free course/platform per career, with a URL
- Web UI (Jinja2 template + CSS) served at `/`
- JSON API for integrations, including a structured `/career` endpoint that returns 3 careers as JSON (title, skills, INR salary, resources) using the OpenAI Python SDK directly
- CORS enabled

## 🛠️ Tech Stack

| Layer | Tech |
| --- | --- |
| API / server | FastAPI, Uvicorn |
| LLM orchestration | LangChain 0.3 (`langchain-core` prompt templates, `langchain-openai` `ChatOpenAI`); OpenAI Python SDK for `/career` |
| Model | OpenAI `gpt-4o` (temperature 0.3) for the chains, set in `app/utils/llm_config.py`; `/career` uses `OPENAI_MODEL` (default `gpt-4o-mini`) |
| UI | Jinja2 templates, static CSS |
| Config | python-dotenv, Pydantic |
| Runtime | `runtime.txt` pins Python 3.11.9 (the format Render and Heroku-style hosts read) |

## 🚀 Getting Started

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root from the template and add your key:

```bash
cp .env.example .env    # then set OPENAI_API_KEY (and optionally OPENAI_MODEL)
```

The app needs `OPENAI_API_KEY` at startup, because the LangChain chains create their `ChatOpenAI` clients when the module is imported.

Run it:

```bash
uvicorn app.main:app --reload
# UI:   http://127.0.0.1:8000/
# Docs: http://127.0.0.1:8000/docs
```

To deploy (e.g. on Render), use a start command like `uvicorn app.main:app --host 0.0.0.0 --port $PORT` and set `OPENAI_API_KEY` in the environment.

## 🔌 API

| Method | Path | Body | Returns |
| --- | --- | --- | --- |
| `GET` | `/` | – | Web UI |
| `GET` | `/status` | – | `{"message": "AI Career Agent is running"}` |
| `POST` | `/suggest` | `{"interests": "robotics, maths"}` | `{"careers", "skill_and_salary", "resources"}` |
| `POST` | `/career` | `{"prompt": "..."}` | `{"careers": [{"title", "skills": [...], "salary", "resources": [...]}]}`. Errors: `503` if no API key, `502` if the OpenAI call fails or the reply can't be parsed |

Example:

```bash
curl -X POST http://127.0.0.1:8000/suggest \
  -H "Content-Type: application/json" \
  -d '{"interests": "I like biology and computers"}'
```

## 📁 Project Structure

```
app/
  main.py                 # FastAPI app, UI route, /status, /suggest
  config.py               # loads env vars
  agents/career_agent.py  # runs the three chains
  chains/
    interest_chain.py
    skill_chain.py
    resouce_chian.py      # resource chain (filename typo kept for compatibility)
  routes/career_routes.py # /career endpoint (structured JSON via the OpenAI SDK)
  schemas/request.py      # CareerQuery model
  utils/llm_config.py     # ChatOpenAI factory
  templates/index.html
  static/style.css
requirements.txt
runtime.txt
.env.example
```

## ⚠️ Known Limitations

- The web UI uses `/suggest` (free-text answers); `/career` is JSON-only and has no UI yet.
- `HUMBUGGING_API_TOKEN` is read in `config.py` but not used.
- No automated tests yet.

## 📄 License

No licence file has been added yet, so all rights are reserved by default.
