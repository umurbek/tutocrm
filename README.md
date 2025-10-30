# TutorCRM

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2.7-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**TutorCRM** is a modern, user-friendly Customer Relationship Management system designed specifically for educational institutions, private tutoring centers, and individual tutors. It streamlines administrative tasks, manages students, classes, schedules, and staff efficiently, and enhances communication between teachers, students, and administrators.

## Key Features

- **Role-based access**: Administrators (“boss”) and teachers.
- **Student & class management**: Add, update, organize student records and class schedules.
- **Secure login**: Email-based authentication with verification codes.
- **Profile management**: Users can upload avatars and track first-time logins.
- **Notifications & messaging**: Smooth communication between staff, teachers, and students.
- **Reports & analytics**: Track student progress, attendance, and overall performance.
- **Scalable & customizable**: Built on Django for easy expansion and customization.

## Project Structure

tutocrm/
│
├── accounts/ # Custom user model, authentication, login
├── home/ # Home page and dashboard
├── students/ # Student management
├── teachers/ # Teacher management
├── tasks/ # Task and schedule management
├── notifications/ # Notifications system
├── templates/ # HTML templates
├── static/ # CSS, JS, and media files
└── manage.py



## Installation

1. Clone the repository:
```bash```,
 git clone https://github.com/username/tutorcrm.git
cd tutorcrm ,

2.Create a virtual environment and install dependencies:

python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt

3 .Apply migrations and run the server:

python manage.py migrate
python manage.py runserver
License

This project is licensed under the MIT License.
