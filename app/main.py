"""FastAPI application exposing the project management logic via a REST API."""

from typing import List

from fastapi import FastAPI, HTTPException

from .logic import ProjectManager
from .models import Material, Order, Project, Quote, Service, Supplier

app = FastAPI()

# In-memory data store using ProjectManager
manager = ProjectManager()

@app.get("/")
def read_root():
    return {"message": "Project materials API"}


@app.post("/projects", response_model=Project)
def create_project(project: Project) -> Project:
    """Add a new project."""
    manager.add_project(project)
    return project


@app.get("/projects", response_model=List[Project])
def list_projects() -> List[Project]:
    """Return all projects."""
    return list(manager.projects.values())


@app.post("/materials", response_model=Material)
def create_material(material: Material) -> Material:
    manager.add_material(material)
    return material


@app.get("/materials", response_model=List[Material])
def list_materials() -> List[Material]:
    return list(manager.materials.values())


@app.post("/services", response_model=Service)
def create_service(service: Service) -> Service:
    manager.add_service(service)
    return service


@app.get("/services", response_model=List[Service])
def list_services() -> List[Service]:
    return list(manager.services.values())


@app.post("/suppliers", response_model=Supplier)
def create_supplier(supplier: Supplier) -> Supplier:
    manager.add_supplier(supplier)
    return supplier


@app.get("/suppliers", response_model=List[Supplier])
def list_suppliers() -> List[Supplier]:
    return list(manager.suppliers.values())


@app.post("/quotes", response_model=Quote)
def create_quote(quote: Quote) -> Quote:
    manager.add_quote(quote)
    return quote


@app.get("/projects/{project_id}/quotes", response_model=List[Quote])
def project_quotes(project_id: int) -> List[Quote]:
    return manager.get_project_quotes(project_id)


@app.get("/projects/{project_id}/total")
def project_total(project_id: int) -> dict:
    return {"total": manager.get_project_total(project_id)}


@app.post("/orders", response_model=Order)
def create_order(quote_id: int) -> Order:
    try:
        return manager.place_order(quote_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/orders", response_model=List[Order])
def list_orders() -> List[Order]:
    return list(manager.orders.values())
