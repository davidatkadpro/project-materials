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

## Core Data Models

Pydantic models in `app/models.py` define the basic project entities:
- `Project` with optional address and schedule fields
- `Material` including a unit of measure
- `Supplier` with contact information and available materials
- `Service` for tasks like electrical or plumbing
- `Quote` representing supplier pricing for materials or services
- `Order` tracking the status of a quote

## Business Logic

`app/logic.py` contains helper functions and a `ProjectManager` class providing an in-memory
implementation of the core operations:

- `calculate_quantity(base_measure, multiplier)` returns a quantity using a simple multiplier
- `ProjectManager` stores projects, materials, suppliers, quotes, and orders
- `place_order()` creates an order from a quote
- `get_project_total()` calculates the total cost for a project
- `best_quote()` finds the cheapest quote for a material or service

