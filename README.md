---
title: AnyCoder
emoji: 🏆
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
disable_embedding: false
hf_oauth: true
hf_oauth_expiration_minutes: 43200
hf_oauth_scopes:
- manage-repos
- write-discussions
models:
  - MiniMaxAI/MiniMax-M2.5
  - zai-org/GLM-5
  - Qwen/Qwen3-Coder-Next
  - moonshotai/Kimi-K2.5
  - zai-org/GLM-4.7-Flash
  - zai-org/GLM-4.7
  - MiniMaxAI/MiniMax-M2.1
  - zai-org/GLM-4.6
  - zai-org/GLM-4.6V
  - deepseek-ai/DeepSeek-V3
  - deepseek-ai/DeepSeek-R1
  - MiniMaxAI/MiniMax-M2
  - moonshotai/Kimi-K2-Thinking
---


# AnyCoder - AI Code Generator with React Frontend

AnyCoder is a full-stack AI-powered code generator with a modern React/TypeScript frontend and FastAPI backend. Generate applications by describing them in plain English, with support for multiple AI models and one-click deployment to Hugging Face Spaces.

## 🎨 Features

- **Modern React UI**: Apple-inspired design with VS Code layout
- **Real-time Streaming**: Server-Sent Events for live code generation
- **Multi-Model Support**: Free coding models (GLM, DeepSeek, MiMo, Nemotron) via OpenCode Zen - zero cost, server-side API key
- **Multiple Languages**: HTML, Gradio, Streamlit, React, Transformers.js, ComfyUI
- **Authentication**: HuggingFace OAuth + Dev mode for local testing
- **One-Click Deployment**: Deploy generated apps directly to HF Spaces

## 🏗️ Architecture

```
anycoder/
├── backend_api.py           # FastAPI backend with streaming
├── frontend/                # Next.js React frontend
│   ├── src/
│   │   ├── app/            # Pages (page.tsx, layout.tsx, globals.css)
│   │   ├── components/     # React components
│   │   ├── lib/            # API client, auth utilities
│   │   └── types/          # TypeScript types
│   └── package.json
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker Space configuration
└── start_fullstack.sh      # Local development script
```

## 🚀 Quick Start

### Local Development

1. **Backend**:
```bash
export OPENCODE_ZEN_API_KEY="your_opencode_zen_api_key"
python backend_api.py
```

2. **Frontend** (new terminal):
```bash
cd frontend
npm install
npm run dev
```

3. Open `http://localhost:3000`

### Using start script:
```bash
export OPENCODE_ZEN_API_KEY="your_opencode_zen_api_key"
./start_fullstack.sh
```

## 🐳 Docker Space Deployment

This app runs as a Docker Space on HuggingFace. The Dockerfile:
- Builds the Next.js frontend
- Runs FastAPI backend on port 7860
- Uses proper user permissions (UID 1000)
- Handles environment variables securely

## 🔑 Authentication

- **Dev Mode** (localhost): Mock login for testing
- **Production**: HuggingFace OAuth with manage-repos scope

## 📝 Supported Languages

- `html` - Static HTML pages
- `gradio` - Python Gradio apps
- `streamlit` - Python Streamlit apps
- `react` - React/Next.js apps
- `transformers.js` - Browser ML apps
- `comfyui` - ComfyUI workflows

## 🤖 Available Models

The following models are currently supported and used by AnyCoder:

models:
  - MiniMaxAI/MiniMax-M2.5
  - zai-org/GLM-5
  - Qwen/Qwen3-Coder-Next
  - moonshotai/Kimi-K2.5
  - zai-org/GLM-4.7-Flash
  - zai-org/GLM-4.7
  - MiniMaxAI/MiniMax-M2.1
  - zai-org/GLM-4.6
  - zai-org/GLM-4.6V
  - deepseek-ai/DeepSeek-V3
  - deepseek-ai/DeepSeek-R1
  - MiniMaxAI/MiniMax-M2
  - moonshotai/Kimi-K2-Thinking

## 🎯 Usage

1. Sign in with HuggingFace (or use Dev Login locally)
2. Select a language and AI model
3. Describe your app in the chat
4. Watch code generate in real-time
5. Click **🚀 Deploy** to publish to HF Spaces

## 🛠️ Environment Variables

- `OPENCODE_ZEN_API_KEY` - OpenCode Zen API key (required for all AI model calls). Server-side only; never exposed to the frontend. Only verified free ($0) Zen models are reachable - the backend rejects any other model id.
- `HF_TOKEN` - HuggingFace API token (optional, only for importing/deploying to HF Spaces)
- `OAUTH_CLIENT_ID` / `OAUTH_CLIENT_SECRET` - HuggingFace OAuth app credentials (production sign-in)

## 📦 Tech Stack

**Frontend:**
- Next.js 14
- TypeScript
- Tailwind CSS
- Monaco Editor

**Backend:**
- FastAPI
- OpenCode Zen (free AI models)
- HuggingFace Hub (deploy/import)
- Server-Sent Events (SSE)

## 📄 License

MIT