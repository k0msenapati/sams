# Student Attendance Management System

A modern, role-based **Student Attendance Management System**.


## Problem It Solves

Manual attendance tracking in engineering colleges is time-consuming, error-prone, and difficult to manage for monthly reports and eligibility checks (75% attendance rule). 

SAMS automates the entire process from daily attendance marking to generating accurate monthly reports with the university rule of **capping 30 classes per subject**.


## How It Solves

- Professors can mark attendance daily through a clean web interface.
- Automatic calculation of attendance percentage with **max 30 classes** rule.
- Clear **Eligible / Not Eligible** status for each subject.
- Students can view their own attendance anytime.
- Centralized database with proper university structure (Department → Section → Course → Lecture → Attendance).


## Features

### For Students
- Login and view personal attendance dashboard
- Subject-wise attendance details
- Overall attendance percentage
- Eligible / Not Eligible status
- 30-class cap clearly applied

### For Professors
- Login and see department courses
- Take daily attendance for any section (checkbox interface)
- View complete **Section/Class Report** in one page
- See total lectures, present count, percentage, and eligibility for all students

### For Administrators
- Full management via Django Admin Panel
- Manage Users, Departments, Sections, Courses, Students & Professors
- Add/Edit academic structure

### General
- Clean, responsive login page
- Role-based access control (Student / Professor / Admin)
- Secure and centralized SQLite database


## Project Structure

| App Name       | What it does                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **core**       | Handles users. It stores login details and defines roles like admin, professor, and student.                                    |
| **attendance** | Main part of the system. Manages everything related to attendance such as students, professors, courses, lectures, and records. |
| **sams**       | Project setup. Controls overall configuration like settings and URL routing.                                                    |


## Setup Instructions (Using UV)

### 1. Clone / Setup Project

```bash
git clone https://github.com/k0msenapati/sams.git
cd sams
```

### 2. Install Dependencies

```bash
uv venv
uv sync
```

### 3. Run Migrations

```bash
uv run python manage.py makemigrations core
uv run python manage.py makemigrations attendance
uv run python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
uv run python manage.py createsuperuser
```

**Important:** After creating superuser:
- Login to `/admin/`
- Edit the superuser and **change Role to "admin"**

### 5. Create Sample Data (Recommended)

In Django Admin (`/admin/`), create in this order:
1. Department (e.g., CSE)
2. Section (e.g., Sem 5 - A)
3. Course
4. Professor User + Professor Profile
5. Student Users + Student Profiles (with section linked)

### 6. Run the Application

```bash
uv run python manage.py runserver
```

Open: `http://127.0.0.1:8000`


## Login Information

- **Students & Professors**: Use `/accounts/login/`
- **Admin**: Use `/admin/login/` 


## Tech Stack

- **Backend**: Django 5.x
- **Database**: SQLite 
- **Frontend**: HTML + Bootstrap 5
- **Package Manager**: UV

