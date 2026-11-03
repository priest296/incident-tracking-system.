## Live App: [https://incident-tracking-system-zy5g.onrender.com](https://incident-tracking-system-zy5g.onrender.com)

GitHub + README + All Matric Numbers: [https://github.com/priest296/incident-tracking-system./tree/main](https://github.com/priest296/incident-tracking-system./tree/main)
---

## Project Topic

**Incident Reporting and Follow-up System**

A complete web-based system for tracking non-emergency IT and facility incidents within community and social services environments (schools, offices, community centers, and public facilities). The system enables structured reporting, role-based access control, incident lifecycle management, Service Level Agreement (SLA) tracking, and comprehensive reporting with analytics dashboards.

---

## Group Members - Group 52

| S/N | Name | Matric Number | Role in Project |
|-----|------|---------------|-----------------|
| 1 | Onoja Emmanuel Ufedojo | FT24CMP0550 | System Architecture & Database Design |
| 2 | Emmanuel Olanike Zena | FT24CMP0182 | User Authentication & Roles |
| 3 | Odebisi Abdul-lateef Ibrahim | FT24CMP0627 | Incident Reporting Module |
| 4 | Isyaka Osabo Yakubu | FT24CMP0308 | Incident Assignment & Workflow |
| 5 | Daniel Kaika Thomas | FT24CMP0616 | SLA Tracking & Due Dates |
| 6 | Emmanuel Elijah Shekwonumwaza | FT23CMP0733 | Reporting & Analytics |
| 7 | Madaki Ogbe Adagayi | FT24CMP0001 | Frontend Development |
| 8 | Egba Samuel Egaji | FT24CMP0229 | Testing, Deployment & Documentation |
| 9 | Maigari Mathias Tukura | FT24CMP0530 | Integration & Final Documentation |

**Course:** NS-CSC229  
**Department:** Computer Science Department 
**Location:** Nasarawa State, Nigeria  
**Institution:** Nasarawa State University, Keffi

---

## Features

### Core Features
- **User Authentication & Roles** – Secure login with hashed passwords and four role-based permission levels:
  - Administrator: Full system access (create, read, update, delete)
  - Reporter: Create incidents and view all incidents
  - Assignee: Update assigned incidents (status, resolution, due date)
  - Viewer: Read-only access to incidents and dashboard

- **Incident Management** – Full CRUD operations for incident records with:
  - Category classification (Hardware, Software, Network, Electrical, Facility, Other)
  - Detailed description and reporter information
  - Contact information for follow-up
  - Status tracking (Open → In Progress → Resolved → Closed)
  - Staff team assignment (IT Support, Network Team, Maintenance, Security)
  - Resolution documentation
  - Timestamps (created, updated)

### Six Core Enhancements
1. **Search & Filter** – Find incidents by keyword, category, or status
2. **CSV Export** – Download all incident data for offline analysis
3. **User Login/Roles** – Authentication with role-based access control
4. **Email Notifications** – Framework for notifications on incident events
5. **Due Date/SLA Tracking** – Target dates with overdue detection and color-coded badges
6. **Dashboard Charts** – Visual analytics with doughnut, bar, line, and pie charts

### Additional Features
- Dark mode support
- Responsive design (mobile-friendly)
- Auto-dismissing flash messages
- Delete confirmation dialogs
- Overdue incident highlighting

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Flask (Python) |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Templating Engine | Jinja2 |
| Charts | Chart.js |
| Password Security | Werkzeug (PBKDF2 with salt) |
| Production Server | Gunicorn |
| Hosting | Render |

---

## Installation & Setup

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/onojaemmanuel08-5572/incident-tracking-system.git
   cd incident-tracking-system
   cd incident_system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   ```
   http://127.0.0.1:5000
   ```

### Demo Credentials

| Username | Password | Role | Access Level |
|----------|----------|------|-------------|
| admin | admin123 | Administrator | Full system access |
| reporter1 | reporter123 | Reporter | Create & view incidents |
| assignee1 | assignee123 | Assignee | Update assigned incidents |
| viewer1 | viewer123 | Viewer | Read-only access |

---

## Project Structure

```
incident_system/
├── app.py              # Flask backend with all routes and logic
├── schema.sql          # SQLite database schema and seed data
├── incidents.db        # SQLite database file
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment configuration
├── .gitignore          # Git ignore rules
├── static/
│   ├── style.css       # Responsive CSS with dark mode support
│   └── app.js          # Frontend interactivity
└── templates/
    ├── base.html       # Base layout with navigation
    ├── login.html      # Login page
    ├── index.html      # Dashboard with charts and filters
    ├── detail.html     # Incident detail view
    └── new.html        # New incident reporting form
```

---

## Documentation

The `NS_CSC229_PDFs/` folder contains 11 comprehensive PDF documents:

| # | Document |
|---|----------|
| 01 | Introduction to Incident Tracking Systems |
| 02 | System Architecture and Design |
| 03 | Database Design and Schema |
| 04 | User Authentication and Roles |
| 05 | Incident Reporting Module |
| 06 | Incident Assignment and Workflow |
| 07 | SLA Tracking and Due Dates |
| 08 | Reporting and Analytics |
| 09 | Frontend Development |
| 10 | Testing, Deployment, and Maintenance |
| 11 | Main Integrated Project Document |

---

## Deployment (Render)

The app is configured for deployment on Render:

1. Push code to GitHub
2. Connect GitHub repository to Render
3. Render will auto-detect `render.yaml` and deploy
4. Your app will be live at [`https://incident-tracking-system-zy5g.onrender.com/]`

---

## Contact

**Group 52** – NS-CSC229 Course Project  
Computer Science Department  
Nasarawa State University, Keffi  
Nasarawa State,Nigeria

---

*This project was developed for NS-CSC229 course requirements.*
