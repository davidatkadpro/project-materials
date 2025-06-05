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

### Available API Endpoints

`app.main` exposes a small REST interface for managing projects. The most
useful routes are:

- `POST /projects` and `GET /projects` - create and list projects
- `POST /materials` and `GET /materials` - manage material catalog entries
- `POST /services` and `GET /services` - manage available services
- `POST /suppliers` and `GET /suppliers` - register suppliers
- `POST /quotes` - attach a quote for a material or service
- `GET /projects/{project_id}/quotes` - list quotes for a project
- `GET /projects/{project_id}/total` - return the total cost of a project
- `POST /orders` - create an order from a quote
- `GET /orders` - list orders that have been created
- `POST /projects/{project_id}/orders` - generate orders for all quotes in a project
- `PUT /orders/{order_id}` - update an order's status or final price
- `GET /projects/{project_id}/quotes/export?format=csv|pdf` - export quotes
- `GET /materials/export?format=csv|pdf` - export the material catalog

## Core Data Models

Pydantic models in `app/models.py` define the basic project entities:
- `Project` with optional address and schedule fields
- `Material` including a unit of measure
- `Supplier` with contact information and available materials
- `Service` for tasks like electrical or plumbing
- `Quote` representing supplier pricing for materials or services
- `Order` tracking the status of a quote and its final price


## Business Logic

`app/logic.py` contains helper functions and a `ProjectManager` class providing an in-memory
implementation of the core operations:

- `calculate_quantity(base_measure, multiplier)` returns a quantity using a simple multiplier
- `ProjectManager` stores projects, materials, suppliers, quotes, and orders
- `place_order()` creates an order from a quote
- `get_project_total()` calculates the total cost for a project
- `best_quote()` finds the cheapest quote for a material or service
- `generate_orders()` creates orders for all quotes tied to a project
- `update_order()` modifies an order's status or final price

## Workflow Features

The API supports generating purchase orders straight from a project and
exporting data for reporting:

- Generate all project orders with `POST /projects/{project_id}/orders`.
- Update an order's status or final price via `PUT /orders/{order_id}`.
- Export project quotes or the material catalog to CSV or PDF using the
  `/projects/{project_id}/quotes/export` and `/materials/export` endpoints.

## Web User Interface

FastAPI also serves a simple HTML front end under the `/ui` path. It uses Jinja2 templates located in `app/templates` to render pages for viewing and creating data. Each section lists existing items and includes a form for adding new ones.

Start the development server and open `http://127.0.0.1:8000/ui` in your browser to interact with projects, materials, services, suppliers, quotes, and orders through a basic web interface.

