# Personal Blog

A modular, full-stack blog application using FastAPI (Python) for the backend and React (Vite + TypeScript + Tailwind CSS) for the frontend. Blog posts are stored in a GitHub Gist for easy, serverless persistence.

---

## Features
- Create and view blog posts
- Posts stored in a GitHub Gist (no database required)
- Modern React frontend with Tailwind CSS
- Modular, extensible backend and frontend codebases
- API-first design (FastAPI auto-generates docs)

---

## Tech Stack
- **Backend:** FastAPI, Pydantic, httpx, python-dotenv
- **Frontend:** React, Vite, TypeScript, Tailwind CSS
- **Storage:** GitHub Gist (via GitHub API)

---

## Directory Structure
```
personal-blog/
  backend/
    app/
      api/routes/         # FastAPI routes
      core/               # Config, exceptions
      models/             # Pydantic models
      schemas/            # Request/response schemas
      services/blog/      # Gist service logic
    requirements.txt
    run.py
  frontend/
    src/                 # React components
    public/
    package.json
    tailwind.config.js
    ...
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd personal-blog
```

### 2. Backend Setup
```bash
cd backend
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Environment Variables
Create a `.env` file in `backend/` with:
```
GITHUB_TOKEN=your_github_token
GIST_ID=your_gist_id
FRONTEND_URL=http://localhost:5173
PORT=8000
```
- `GITHUB_TOKEN` must have access to read/write the Gist.
- `GIST_ID` is the ID of your Gist (must contain `blog_data.json`).

#### Run the Backend
```bash
python run.py
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

---

## Usage
- Open [http://localhost:5173](http://localhost:5173) in your browser.
- Create and view blog posts.
- Posts are persisted to your GitHub Gist.

---

## API Endpoints
- `GET /api/blog-posts/` — List all blog posts
- `POST /api/blog-posts/` — Create a new blog post
- `GET /api/blog-posts/{id}` — Get a single blog post
- `GET /health` — Health check

---

## Customization & Extensibility
- Swap out the Gist service for a real database by implementing the service interface.
- Add authentication, comments, or other features as needed.
- Use Tailwind CSS to easily customize the frontend design.