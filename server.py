from emails import EmailSender
from HRMS import *
from typing import List, Dict, Optional
from mcp.server.fastmcp import FastMCP

# load the env
from dotenv import load_dotenv
load_dotenv()

import os
from utils import seed_services

employee_manager = EmployeeManager()
meeting_manager = MeetingManager()
leave_manager = LeaveManager()
ticket_manager = TicketManager()
business_trip_manager = BusinessTripManager()

seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager, business_trip_manager)

emailer = EmailSender(
    smtp_server="smtp.gmail.com",
    port=587,
    username=os.getenv("CB_EMAIL"),
    password=os.getenv("CB_EMAIL_PWD"),
    use_tls=True
)

mcp = FastMCP("hr-assist")

@mcp.tool()
def add_employee(emp_name:str, manager_id:str, email:str) -> str:
    """
    Add a new employee to the HRMS system.
    :param emp_name: Employee name
    :param manager_id: Manager ID (optional)
    :return: Confirmation message
    """
    emp = EmployeeCreate(
        emp_id=employee_manager.get_next_emp_id(),
        name=emp_name,
        manager_id=manager_id,
        email=email
    )
    employee_manager.add_employee(emp)
    return f"Employee {emp_name} added successfully."

@mcp.tool()
def get_employee_details(name: str) -> Dict[str, str]:
    """
    Get employee details by name.
    :param name: Name of the employee
    :return: Employee ID and manager ID
    """
    matches = employee_manager.search_employee_by_name(name)

    if len(matches) == 0:
        raise ValueError(f"No employees found with name {name}.")

    emp_id = matches[0]
    emp_details = employee_manager.get_employee_details(emp_id)
    return emp_details

@mcp.tool()
def send_email(to_emails: List[str], subject: str, body: str, html: bool = False) -> None:
    emailer.send_email(subject, body, to_emails, from_email=emailer.username, html=html)
    return "Email sent successfully."


@mcp.tool()
def create_ticket(emp_id: str, item: str, reason:str) -> str:
    """
    Create a ticket for buying required items for an employee.
    :param emp_id: Employee ID
    :param item: Item requested (Laptop, ID Card, etc.)
    :param reason: Reason for the request
    :return: Confirmation message
    """
    ticket_req = TicketCreate(emp_id=emp_id, item=item, reason=reason)
    return ticket_manager.create_ticket(ticket_req)

@mcp.tool()
def update_ticket_status(ticket_id: str, status: str) -> str:
    """
    Update the status of a ticket.
    :param ticket_id: Ticket ID
    :param status: New status of the ticket
    :return: Confirmation message
    """
    ticket_status_update = TicketStatusUpdate(status=status)
    return ticket_manager.update_ticket_status(ticket_status_update, ticket_id)

@mcp.tool()
def list_tickets(employee_id: str, status: str) -> str:
    """
    List tickets for an employee with optional status filter.
    :param employee_id: Employee ID
    :param status: Ticket status (optional)
    :return: List of tickets
    """
    return ticket_manager.list_tickets(employee_id=employee_id, status=status)


@mcp.tool()
def schedule_meeting(employee_id: str, meeting_datetime: datetime, topic: str) -> str:
    """
    Schedule a meeting for an employee.
    :param employee_id: Employee ID
    :param meeting_datetime: Date and time of the meeting in python datetime format
    :param topic: Topic of the meeting
    :return: Confirmation message
    """
    meeting_req = MeetingCreate(
        emp_id=employee_id,
        meeting_dt=meeting_datetime,
        topic=topic
    )
    return meeting_manager.schedule_meeting(meeting_req)


@mcp.tool()
def get_meetings(employee_id: str) -> str:
    """
    Get the list of meetings scheduled for an employee.
    :param employee_id: Employee ID
    :return: List of meetings
    """
    return meeting_manager.get_meetings(employee_id)


@mcp.tool()
def cancel_meeting(employee_id: str, meeting_datetime: datetime, topic: str) -> str:
    """
    Cancel a scheduled meeting for an employee.
    :param employee_id: Employee ID
    :param meeting_datetime: Date and time of the meeting in python datetime format
    :param topic: Topic of the meeting (optional)
    :return: Confirmation message
    """
    meeting_req = MeetingCancelRequest(
        emp_id=employee_id,
        meeting_dt=meeting_datetime,
        topic=topic
    )
    return meeting_manager.cancel_meeting(meeting_req)


@mcp.tool()
def get_employee_leave_balance(emp_id: str) -> str:
    """
    Get the leave balance of an employee.
    :param emp_id: Employee ID
    :return: Leave balance message
    """
    return leave_manager.get_leave_balance(emp_id)

@mcp.tool()
def apply_leave(emp_id: str, leave_dates: list) -> str:
    """
    Apply for leave for an employee.
    :param emp_id: Employee ID
    :param leave_dates: List of leave dates
    :return: Leave application status message
    """
    req = LeaveApplyRequest(emp_id=emp_id, leave_dates=leave_dates)
    return leave_manager.apply_leave(req)


@mcp.tool()
def get_leave_history(emp_id: str) -> str:
    """
    Get the leave history of an employee.
    :param emp_id: Employee ID
    :return: Leave history message
    """
    return leave_manager.get_leave_history(emp_id)


# Business Trip Management Tools
@mcp.tool()
def create_business_trip(emp_id: str, destination: str, purpose: str, start_date: date, end_date: date, estimated_cost: float, manager_id: str) -> str:
    """
    Create a new business trip request for an employee.
    :param emp_id: Employee ID
    :param destination: Travel destination
    :param purpose: Purpose of the business trip
    :param start_date: Trip start date
    :param end_date: Trip end date
    :param estimated_cost: Estimated trip cost
    :param manager_id: Manager ID for approval
    :return: Confirmation message
    """
    trip_req = BusinessTripCreate(
        emp_id=emp_id,
        destination=destination,
        purpose=purpose,
        start_date=start_date,
        end_date=end_date,
        estimated_cost=estimated_cost,
        manager_id=manager_id
    )
    return business_trip_manager.create_trip(trip_req)


@mcp.tool()
def approve_business_trip(trip_id: str, manager_id: str, approved: bool = True) -> str:
    """
    Approve or reject a business trip request.
    :param trip_id: Trip ID
    :param manager_id: Manager ID who is approving/rejecting
    :param approved: True to approve, False to reject
    :return: Confirmation message
    """
    status = "Approved" if approved else "Rejected"
    status_update = BusinessTripStatusUpdate(status=status, approved_by=manager_id)
    return business_trip_manager.update_trip_status(status_update, trip_id)


@mcp.tool()
def get_business_trips(employee_id: str = None, status: str = None, manager_id: str = None) -> List[Dict]:
    """
    Get business trips with optional filters.
    :param employee_id: Filter by employee ID
    :param status: Filter by trip status
    :param manager_id: Filter by manager ID
    :return: List of business trips
    """
    return business_trip_manager.list_trips(employee_id=employee_id, status=status, manager_id=manager_id)


@mcp.tool()
def get_pending_trip_approvals(manager_id: str) -> List[Dict]:
    """
    Get all pending business trip requests for a manager to approve.
    :param manager_id: Manager ID
    :return: List of pending trip requests
    """
    return business_trip_manager.get_pending_approvals(manager_id)


@mcp.tool()
def add_trip_expense(trip_id: str, expense_type: str, amount: float, description: str, expense_date: date) -> str:
    """
    Add an expense to a business trip.
    :param trip_id: Trip ID
    :param expense_type: Type of expense (Transport, Accommodation, Meals, etc.)
    :param amount: Expense amount
    :param description: Description of the expense
    :param expense_date: Date of the expense
    :return: Confirmation message
    """
    expense_req = BusinessTripExpense(
        trip_id=trip_id,
        expense_type=expense_type,
        amount=amount,
        description=description,
        expense_date=expense_date
    )
    return business_trip_manager.add_expense(expense_req)


@mcp.tool()
def get_trip_summary(trip_id: str) -> Dict:
    """
    Get a comprehensive summary of a business trip including expenses.
    :param trip_id: Trip ID
    :return: Trip summary with expenses
    """
    return business_trip_manager.get_trip_summary(trip_id)


@mcp.tool()
def cancel_business_trip(trip_id: str, reason: str = "Cancelled by employee") -> str:
    """
    Cancel a business trip.
    :param trip_id: Trip ID
    :param reason: Reason for cancellation
    :return: Confirmation message
    """
    return business_trip_manager.cancel_trip(trip_id, reason)


@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str):
    return f"""Onboard a new employee with the following details:
    - Name: {employee_name}
    - Manager Name: {manager_name}
    Steps to follow:
    - Add the employee to the HRMS system.
    - Send a welcome email to the employee with their login credentials. (Format: employee_name@atliq.com)
    - Notify the manager about the new employee's onboarding.
    - Raise tickets for a new laptop, id card, and other necessary equipment.
    - Schedule an introductory meeting between the employee and the manager.
    - Create a business trip request if the employee needs to travel for training or onboarding purposes.
    - Ensure all necessary documents are collected and stored securely.
    - Provide the employee with a list of resources and contacts for any queries.
    - Follow up with the employee after a week to ensure they are settling in well.
    """



if __name__ == "__main__":
    mcp.run(transport="stdio")
