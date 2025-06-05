# project-materials
Creates a comprehensive tool to manage building project materials and orders

## Development Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API root at `http://127.0.0.1:8000/` will return a simple JSON message.
