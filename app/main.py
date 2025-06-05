"""FastAPI application exposing the project management logic via a REST API."""

from typing import List

from datetime import date

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from io import StringIO, BytesIO
import csv
from fpdf import FPDF

from .logic import ProjectManager
from .models import (
    Material,
    Order,
    OrderStatus,
    Project,
    Quote,
    Service,
    Supplier,
)

app = FastAPI()

# In-memory data store using ProjectManager
manager = ProjectManager()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root():
    return {"message": "Project materials API"}


# ----- UI Routes -----

@app.get("/ui", response_class=HTMLResponse)
def ui_index(request: Request):
    """Render the home page for the HTML interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ui/projects", response_class=HTMLResponse)
def ui_projects(request: Request):
    return templates.TemplateResponse(
        "projects.html", {"request": request, "projects": list(manager.projects.values())}
    )


@app.post("/ui/projects")
def ui_create_project(
    id: int = Form(...),
    name: str = Form(...),
    address: str | None = Form(None),
    start_date: str | None = Form(None),
    end_date: str | None = Form(None),
):
    start = date.fromisoformat(start_date) if start_date else None
    end = date.fromisoformat(end_date) if end_date else None
    manager.add_project(
        Project(id=id, name=name, address=address, start_date=start, end_date=end)
    )
    return RedirectResponse("/ui/projects", status_code=303)


@app.get("/ui/materials", response_class=HTMLResponse)
def ui_materials(request: Request):
    return templates.TemplateResponse(
        "materials.html", {"request": request, "materials": list(manager.materials.values())}
    )


@app.post("/ui/materials")
def ui_create_material(
    id: int = Form(...),
    name: str = Form(...),
    unit: str = Form(...),
    notes: str | None = Form(None),
):
    manager.add_material(Material(id=id, name=name, unit=unit, notes=notes))
    return RedirectResponse("/ui/materials", status_code=303)


@app.get("/ui/services", response_class=HTMLResponse)
def ui_services(request: Request):
    return templates.TemplateResponse(
        "services.html", {"request": request, "services": list(manager.services.values())}
    )


@app.post("/ui/services")
def ui_create_service(
    id: int = Form(...),
    name: str = Form(...),
    unit_price: float = Form(...),
    notes: str | None = Form(None),
):
    manager.add_service(Service(id=id, name=name, unit_price=unit_price, notes=notes))
    return RedirectResponse("/ui/services", status_code=303)


@app.get("/ui/suppliers", response_class=HTMLResponse)
def ui_suppliers(request: Request):
    return templates.TemplateResponse(
        "suppliers.html", {"request": request, "suppliers": list(manager.suppliers.values())}
    )


@app.post("/ui/suppliers")
def ui_create_supplier(
    id: int = Form(...),
    name: str = Form(...),
    contact: str | None = Form(None),
    materials: str = Form(""),
):
    material_ids = [int(m) for m in materials.split(",") if m.strip()]
    manager.add_supplier(
        Supplier(id=id, name=name, contact=contact, materials=material_ids)
    )
    return RedirectResponse("/ui/suppliers", status_code=303)


@app.get("/ui/quotes", response_class=HTMLResponse)
def ui_quotes(request: Request):
    return templates.TemplateResponse(
        "quotes.html", {"request": request, "quotes": list(manager.quotes.values())}
    )


@app.post("/ui/quotes")
def ui_create_quote(
    id: int = Form(...),
    project_id: int = Form(...),
    supplier_id: int = Form(...),
    material_id: str = Form(""),
    service_id: str = Form(""),
    quantity: float = Form(...),
    price: float = Form(...),
):
    m_id = int(material_id) if material_id else None
    s_id = int(service_id) if service_id else None
    manager.add_quote(
        Quote(
            id=id,
            project_id=project_id,
            supplier_id=supplier_id,
            material_id=m_id,
            service_id=s_id,
            quantity=quantity,
            price=price,
        )
    )
    return RedirectResponse("/ui/quotes", status_code=303)


@app.get("/ui/orders", response_class=HTMLResponse)
def ui_orders(request: Request):
    return templates.TemplateResponse(
        "orders.html", {"request": request, "orders": list(manager.orders.values())}
    )


@app.post("/ui/orders")
def ui_create_order(quote_id: int = Form(...)):
    try:
        manager.place_order(quote_id)
    except ValueError:
        pass
    return RedirectResponse("/ui/orders", status_code=303)


@app.post("/ui/orders/update")
def ui_update_order(order_id: int = Form(...), final_price: float = Form(...)):
    try:
        manager.update_order(order_id, status=OrderStatus.completed, final_price=final_price)
    except ValueError:
        pass
    return RedirectResponse("/ui/orders", status_code=303)


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


@app.post("/projects/{project_id}/orders", response_model=List[Order])
def generate_project_orders(project_id: int) -> List[Order]:
    """Generate orders for all quotes in a project."""
    try:
        return manager.generate_orders(project_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.put("/orders/{order_id}", response_model=Order)
def update_order(
    order_id: int,
    status: OrderStatus | None = None,
    final_price: float | None = None,
) -> Order:
    try:
        return manager.update_order(order_id, status=status, final_price=final_price)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/projects/{project_id}/quotes/export")
def export_project_quotes(project_id: int, format: str = "csv"):
    quotes = manager.get_project_quotes(project_id)
    if format == "csv":
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow([
            "id",
            "project_id",
            "supplier_id",
            "material_id",
            "service_id",
            "quantity",
            "price",
        ])
        for q in quotes:
            writer.writerow([
                q.id,
                q.project_id,
                q.supplier_id,
                q.material_id or "",
                q.service_id or "",
                q.quantity,
                q.price,
            ])
        csv_file.seek(0)
        return StreamingResponse(
            iter([csv_file.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=quotes.csv"},
        )
    elif format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Project Quotes", ln=True)
        for q in quotes:
            line = f"{q.id} {q.project_id} {q.supplier_id} {q.quantity} @ {q.price}"
            pdf.cell(200, 10, txt=line, ln=True)
        pdf_output = pdf.output(dest="S").encode("latin-1")
        return StreamingResponse(
            BytesIO(pdf_output),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=quotes.pdf"},
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")


@app.get("/materials/export")
def export_materials(format: str = "csv"):
    materials = list(manager.materials.values())
    if format == "csv":
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(["id", "name", "unit", "notes"])
        for m in materials:
            writer.writerow([m.id, m.name, m.unit, m.notes or ""])
        csv_file.seek(0)
        return StreamingResponse(
            iter([csv_file.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=materials.csv"},
        )
    elif format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Materials", ln=True)
        for m in materials:
            pdf.cell(200, 10, txt=f"{m.id} {m.name} ({m.unit})", ln=True)
        pdf_output = pdf.output(dest="S").encode("latin-1")
        return StreamingResponse(
            BytesIO(pdf_output),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=materials.pdf"},
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

