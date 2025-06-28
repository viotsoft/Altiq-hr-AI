from typing import List, Dict, Optional
from datetime import datetime, date
from HRMS.schemas import BusinessTripCreate, BusinessTripStatusUpdate, BusinessTripExpense


class BusinessTripManager:
    def __init__(self):
        self.trips: List[Dict] = []
        self.expenses: List[Dict] = []
        self._next_trip_id: int = 1
        self._next_expense_id: int = 1

    def create_trip(self, req: BusinessTripCreate) -> str:
        """
        Create a new business trip request.
        """
        if req.start_date >= req.end_date:
            raise ValueError("Start date must be before end date.")
        
        trip_id = f"TR{self._next_trip_id:03d}"
        trip = {
            "trip_id": trip_id,
            "emp_id": req.emp_id,
            "destination": req.destination,
            "purpose": req.purpose,
            "start_date": req.start_date.isoformat(),
            "end_date": req.end_date.isoformat(),
            "estimated_cost": req.estimated_cost,
            "manager_id": req.manager_id,
            "status": "Pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "approved_by": None,
            "approved_at": None
        }
        self.trips.append(trip)
        self._next_trip_id += 1
        return f"Business trip {trip_id} created for {req.emp_id} to {req.destination}."

    def update_trip_status(self, req: BusinessTripStatusUpdate, trip_id: str) -> str:
        """
        Update the status of a business trip (approve, reject, etc.).
        """
        for trip in self.trips:
            if trip["trip_id"] == trip_id:
                old_status = trip["status"]
                trip["status"] = req.status
                trip["updated_at"] = datetime.utcnow().isoformat()
                
                if req.status in ["Approved", "Rejected"] and req.approved_by:
                    trip["approved_by"] = req.approved_by
                    trip["approved_at"] = datetime.utcnow().isoformat()
                
                return f"Trip {trip_id} status updated from {old_status} to {req.status}."
        
        raise ValueError(f"Trip '{trip_id}' not found.")

    def get_trip_details(self, trip_id: str) -> Dict:
        """
        Get detailed information about a specific trip.
        """
        for trip in self.trips:
            if trip["trip_id"] == trip_id:
                return trip
        raise ValueError(f"Trip '{trip_id}' not found.")

    def list_trips(
        self,
        employee_id: Optional[str] = None,
        status: Optional[str] = None,
        manager_id: Optional[str] = None
    ) -> List[Dict]:
        """
        List trips with optional filters.
        """
        results = self.trips
        
        if employee_id:
            results = [t for t in results if t["emp_id"] == employee_id]
        if status:
            results = [t for t in results if t["status"].lower() == status.lower()]
        if manager_id:
            results = [t for t in results if t["manager_id"] == manager_id]
        
        return sorted(results, key=lambda x: x["created_at"], reverse=True)

    def get_pending_approvals(self, manager_id: str) -> List[Dict]:
        """
        Get all pending trip requests for a manager to approve.
        """
        return [
            trip for trip in self.trips 
            if trip["manager_id"] == manager_id and trip["status"] == "Pending"
        ]

    def add_expense(self, req: BusinessTripExpense) -> str:
        """
        Add an expense to a business trip.
        """
        # Verify trip exists
        trip_exists = any(trip["trip_id"] == req.trip_id for trip in self.trips)
        if not trip_exists:
            raise ValueError(f"Trip '{req.trip_id}' not found.")
        
        expense_id = f"EXP{self._next_expense_id:04d}"
        expense = {
            "expense_id": expense_id,
            "trip_id": req.trip_id,
            "expense_type": req.expense_type,
            "amount": req.amount,
            "description": req.description,
            "expense_date": req.expense_date.isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
        self.expenses.append(expense)
        self._next_expense_id += 1
        return f"Expense {expense_id} added to trip {req.trip_id}."

    def get_trip_expenses(self, trip_id: str) -> List[Dict]:
        """
        Get all expenses for a specific trip.
        """
        return [exp for exp in self.expenses if exp["trip_id"] == trip_id]

    def get_trip_summary(self, trip_id: str) -> Dict:
        """
        Get a summary of trip details and total expenses.
        """
        trip = self.get_trip_details(trip_id)
        expenses = self.get_trip_expenses(trip_id)
        
        total_expenses = sum(exp["amount"] for exp in expenses)
        estimated_cost = trip["estimated_cost"]
        
        return {
            "trip": trip,
            "expenses": expenses,
            "total_expenses": total_expenses,
            "estimated_cost": estimated_cost,
            "variance": total_expenses - estimated_cost,
            "expense_count": len(expenses)
        }

    def cancel_trip(self, trip_id: str, reason: str = "Cancelled by employee") -> str:
        """
        Cancel a business trip.
        """
        for trip in self.trips:
            if trip["trip_id"] == trip_id:
                if trip["status"] in ["Completed", "Cancelled"]:
                    raise ValueError(f"Cannot cancel trip in {trip['status']} status.")
                
                trip["status"] = "Cancelled"
                trip["updated_at"] = datetime.utcnow().isoformat()
                return f"Trip {trip_id} cancelled. Reason: {reason}"
        
        raise ValueError(f"Trip '{trip_id}' not found.")


if __name__ == "__main__":
    # Test the business trip manager
    btm = BusinessTripManager()
    
    # Create a test trip
    from datetime import date
    trip_req = BusinessTripCreate(
        emp_id="E001",
        destination="New York",
        purpose="Client Meeting",
        start_date=date(2024, 2, 15),
        end_date=date(2024, 2, 18),
        estimated_cost=2500.0,
        manager_id="E002"
    )
    
    print(btm.create_trip(trip_req))
    print(btm.list_trips()) 