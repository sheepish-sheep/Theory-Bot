# 🔮 Theory Bot
> An AI-powered web application that generates wild, unhinged theories using a local Large Language Model.

## 🧠 Overview

Theory Bot is an AI-powered web application that generates wild, unhinged theories using a local Large Language Model (LLM) via LM Studio. It operates in two modes:

- **Unhinged Mode**: Takes user-provided text and creates absurd, bizarre theories by making unexpected connections.

- **Franchise Mode**: Takes the name of a franchise (e.g., Star Wars, Marvel) and generates wild fan theories about it.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI, Uvicorn |
| Frontend | HTML, TailwindCSS, Vanilla JavaScript |
| AI Integration | Local LLM via LM Studio API |
| Caching | JSON file storage |

## 🔧 Requirements

- Python 3.7+
- [LM Studio](https://lmstudio.ai/) with a compatible model (e.g., `hermes-2-llama-3.1-8b`)
- LM Studio running with local API endpoint: `http://127.0.0.1:1234/v1/completions`

## 📦 Installation

1. Clone the repository or download the files.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up LM Studio:
   - Download and install [LM Studio](https://lmstudio.ai/)
   - Download a compatible model (like `hermes-2-llama-3.1-8b`)
   - Start the model with API server enabled (port 1234)

## 🚀 Running the Application

1. Start LM Studio and ensure the API server is running on port 1234.

2. Run the Theory Bot server:
   ```bash
   python main.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

### Running in Mock Mode (No LM Studio Required)

You can run Theory Bot in mock mode, which doesn't require LM Studio to be running:

```bash
python main.py --mock
```

This mode uses predefined responses instead of calling the LLM API, which is useful for testing or when you don't have access to LM Studio.

### Changing the Port

If port 8000 is already in use, you can specify a different port:

```bash
python main.py --port 8001
```

## 🔌 API Endpoints

The application provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/generate-theory` | POST | Generate a theory in either unhinged or franchise mode |
| `/health` | GET | Check the health of the server and LLM API connection |

## 🧩 Theory Generation

The application uses a local LLM to generate theories based on user input:

1. **Unhinged Mode**: Provide any text and the system will create a bizarre theory.
2. **Franchise Mode**: Provide a franchise name (and optional additional text) to generate a fan theory.

## 📝 Caching

Generated theories are cached in `cached_theories.json` to improve performance and reduce redundant API calls.

## 📱 Browser Compatibility

The web interface is designed to work with modern browsers, with responsive design that works on both desktop and mobile devices.

## 🛠️ Project Structure

```
Theory Bot/
├── main.py                 # FastAPI application entry point
├── theory_generator.py     # Core theory generation logic
├── utils.py                # Utility functions for API calls and caching
├── cached_theories.json    # Cache for generated theories
├── templates/
│   └── index.html          # Web interface template
└── static/
    └── js/
        └── main.js         # Frontend interaction script
```

## 🔮 Future Enhancements

- Add support for multiple LLM endpoints
- Implement user authentication
- Add social sharing features
- Enhance the UI with animations
- Provide more theory generation modes