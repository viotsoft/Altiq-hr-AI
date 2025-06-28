# 🏢 HR-ASSIST: Agentic AI HR Management System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.9.4+-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

**HR-ASSIST** is an intelligent Agentic AI system designed to automate and streamline HR workflows, particularly focusing on employee onboarding and day-to-day HR operations. Built as an MCP (Model Context Protocol) server, it integrates seamlessly with Claude Desktop to provide a powerful AI-powered HR management experience.

### 🎯 Key Features

- **🤖 AI-Powered Employee Onboarding**: Automated workflow for new employee setup
- **👥 Employee Management**: Complete employee lifecycle management with hierarchical structures
- **📧 Email Automation**: Automated email notifications and communications
- **🎫 Ticket Management**: IT equipment and resource request tracking
- **📅 Meeting Scheduling**: Intelligent meeting coordination and management
- **🏖️ Leave Management**: Comprehensive leave tracking and approval workflows
- **✈️ Business Trip Management**: Complete travel request and expense tracking system
- **🔍 Smart Search**: Fuzzy name matching for employee lookups

## 🏗️ Architecture

### Core Components

```
atliq-hr-assist/
├── HRMS/                    # HR Management System Core
│   ├── employee_manager.py  # Employee lifecycle management
│   ├── leave_manager.py     # Leave tracking and approval
│   ├── meeting_manager.py   # Meeting scheduling and coordination
│   ├── ticket_manager.py    # IT ticket management
│   └── schemas.py          # Pydantic data models
├── server.py               # MCP server implementation
├── emails.py               # Email automation service
├── utils.py                # Data seeding and utilities
└── main.py                 # Application entry point
```

### Technology Stack

- **Backend**: Python 3.10+
- **AI Integration**: Model Context Protocol (MCP) 1.9.4+
- **Data Validation**: Pydantic v2
- **Email Service**: SMTP with TLS support
- **Package Management**: uv (modern Python package manager)

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Claude Desktop application
- Gmail account with App Password (for email functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/atliq-hr-assist.git
   cd atliq-hr-assist
   ```

2. **Install dependencies using uv**
   ```bash
   uv init
   uv add mcp[cli]>=1.9.4
   uv add pydantic>=2.0
   uv add python-dotenv
   ```

3. **Configure environment variables**
   ```bash
   cp sample.env .env
   ```
   
   Edit `.env` file with your email credentials:
   ```env
   CB_EMAIL=your-email@gmail.com
   CB_EMAIL_PWD=your-app-password
   ```

4. **Configure Claude Desktop**
   
   Add the following configuration to your `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "hr-assist": {
         "command": "C:\\Users\\your-username\\.local\\bin\\uv",
         "args": [
           "--directory",
           "C:\\path\\to\\atliq-hr-assist",
           "run",
           "server.py"
         ],
         "env": {
           "CB_EMAIL": "your-email@gmail.com",
           "CB_EMAIL_PWD": "your-app-password"
         }
       }
     }
   }
   ```

5. **Start the MCP server**
   ```bash
   uv run server.py
   ```

## 🛠️ Available Tools

### Employee Management
- `add_employee(emp_name, manager_id, email)` - Add new employee to system
- `get_employee_details(name)` - Retrieve employee information
- `search_employee_by_name(name_query)` - Fuzzy search for employees

### Email Automation
- `send_email(to_emails, subject, body, html)` - Send automated emails
- Supports HTML formatting and attachments

### Ticket Management
- `create_ticket(emp_id, item, reason)` - Create IT equipment requests
- `update_ticket_status(ticket_id, status)` - Update ticket progress
- `list_tickets(employee_id, status)` - View ticket history

### Meeting Management
- `schedule_meeting(employee_id, meeting_datetime, topic)` - Schedule meetings
- `get_meetings(employee_id)` - View scheduled meetings
- `cancel_meeting(employee_id, meeting_datetime, topic)` - Cancel meetings

### Leave Management
- `get_employee_leave_balance(emp_id)` - Check leave balance
- `apply_leave(emp_id, leave_dates)` - Submit leave requests
- `get_leave_history(emp_id)` - View leave history

### Business Trip Management
- `create_business_trip(emp_id, destination, purpose, start_date, end_date, estimated_cost, manager_id)` - Create travel request
- `approve_business_trip(trip_id, manager_id, approved)` - Approve/reject trip requests
- `get_business_trips(employee_id, status, manager_id)` - List trips with filters
- `get_pending_trip_approvals(manager_id)` - Get pending approvals for manager
- `add_trip_expense(trip_id, expense_type, amount, description, expense_date)` - Add trip expenses
- `get_trip_summary(trip_id)` - Get comprehensive trip summary with expenses
- `cancel_business_trip(trip_id, reason)` - Cancel business trip

## 📖 Usage Examples

### Employee Onboarding Workflow

The system includes a pre-built prompt for complete employee onboarding:

```python
@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str):
    # Automatically handles:
    # 1. Employee registration
    # 2. Welcome email with credentials
    # 3. Manager notification
    # 4. Equipment ticket creation
    # 5. Introductory meeting scheduling
```

### Basic Operations

```python
# Add a new employee
add_employee("John Doe", "E001", "john.doe@atliq.com")

# Send welcome email
send_email(
    to_emails=["john.doe@atliq.com"],
    subject="Welcome to Atliq!",
    body="Welcome aboard! Your login credentials are...",
    html=True
)

# Create equipment tickets
create_ticket("E002", "Laptop", "New hire setup")
create_ticket("E002", "ID Card", "New hire setup")

# Schedule onboarding meeting
schedule_meeting("E002", "2024-01-15T10:00:00", "Onboarding Introduction")

# Business Trip Management
create_business_trip("E001", "New York", "Client Meeting", "2024-02-15", "2024-02-18", 2500.0, "E002")
approve_business_trip("TR001", "E002", True)
add_trip_expense("TR001", "Transport", 500.0, "Flight tickets", "2024-02-15")
get_trip_summary("TR001")
```

## 🗄️ Data Models

### Employee Schema
```python
class EmployeeCreate(BaseModel):
    emp_id: str
    name: str
    manager_id: Optional[str]
    email: Optional[str]
```

### Leave Management
```python
class LeaveApplyRequest(BaseModel):
    emp_id: str
    leave_dates: List[date]
```

### Meeting Management
```python
class MeetingCreate(BaseModel):
    emp_id: str
    meeting_dt: datetime
    topic: str
```

### Ticket Management
```python
class TicketCreate(BaseModel):
    emp_id: str
    item: str
    reason: str
```

### Business Trip Management
```python
class BusinessTripCreate(BaseModel):
    emp_id: str
    destination: str
    purpose: str
    start_date: date
    end_date: date
    estimated_cost: float
    manager_id: Optional[str]
```

## 🔧 Configuration

### Email Settings
The system supports Gmail SMTP with TLS:
- SMTP Server: `smtp.gmail.com`
- Port: `587`
- Security: TLS enabled

### Sample Data
The system comes pre-loaded with sample data including:
- 8 employees with hierarchical structure
- Leave balances and history
- Scheduled meetings
- Active tickets
- Business trips with various destinations and purposes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Codebasics Inc** - Original project development
- **LearnerX India Private Ltd** - Educational support
- **Anthropic** - Claude Desktop and MCP framework
- **Pydantic** - Data validation framework

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the [documentation](docs/)
- Review the [FAQ](docs/FAQ.md)

---

**Made with ❤️ for modern HR workflows**