"""Business logic layer for managing projects, materials, quotes and orders."""

from typing import Dict, List, Optional

from .models import (
    Material,
    Order,
    OrderStatus,
    Project,
    Quote,
    Service,
    Supplier,
)


def calculate_quantity(base_measure: float, multiplier: float) -> float:
    """Return calculated quantity using a simple multiplier."""
    return base_measure * multiplier


class ProjectManager:
    """In-memory management of projects, quotes and orders."""

    def __init__(self) -> None:
        self.projects: Dict[int, Project] = {}
        self.materials: Dict[int, Material] = {}
        self.services: Dict[int, Service] = {}
        self.suppliers: Dict[int, Supplier] = {}
        self.quotes: Dict[int, Quote] = {}
        self.orders: Dict[int, Order] = {}

    # Basic CRUD helpers
    def add_project(self, project: Project) -> None:
        self.projects[project.id] = project

    def add_material(self, material: Material) -> None:
        self.materials[material.id] = material

    def add_service(self, service: Service) -> None:
        self.services[service.id] = service

    def add_supplier(self, supplier: Supplier) -> None:
        self.suppliers[supplier.id] = supplier

    def add_quote(self, quote: Quote) -> None:
        self.quotes[quote.id] = quote

    # Business operations
    def place_order(self, quote_id: int) -> Order:
        if quote_id not in self.quotes:
            raise ValueError("Quote does not exist")
        order_id = len(self.orders) + 1
        order = Order(id=order_id, quote_id=quote_id, status=OrderStatus.ordered)
        self.orders[order_id] = order
        return order


    def generate_orders(self, project_id: int) -> List[Order]:
        """Create orders for all quotes attached to a project."""
        orders = []
        for quote in self.get_project_quotes(project_id):
            orders.append(self.place_order(quote.id))
        return orders

    def update_order(
        self,
        order_id: int,
        *,
        status: Optional[OrderStatus] = None,
        final_price: Optional[float] = None,
    ) -> Order:
        """Update order status or final price."""
        if order_id not in self.orders:
            raise ValueError("Order does not exist")
        order = self.orders[order_id]
        if status is not None:
            order.status = status
        if final_price is not None:
            order.final_price = final_price
            # update quote price when order finalized
            if order.quote_id in self.quotes:
                self.quotes[order.quote_id].price = final_price
        return order

    def get_project_quotes(self, project_id: int) -> List[Quote]:
        return [q for q in self.quotes.values() if q.project_id == project_id]

    def get_project_total(self, project_id: int) -> float:
        return sum(q.price * q.quantity for q in self.get_project_quotes(project_id))

    def best_quote(
        self, project_id: int, *, material_id: Optional[int] = None, service_id: Optional[int] = None
    ) -> Optional[Quote]:
        """Return the cheapest quote for the given material or service within a project."""
        candidates = [
            q
            for q in self.get_project_quotes(project_id)
            if q.material_id == material_id and q.service_id == service_id
        ]
        if not candidates:
            return None
        return min(candidates, key=lambda q: q.price)
