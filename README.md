# MealGenie


## Setup Instructions

1. Create a virtual environment (venv) at root directory:

`python -m venv venv`

2. Always remember to activate the correct virtual environment & set your VSCode interpreter to the correct path.

Windows: `venv\Scripts\activate`

macOS/Linux: `source venv/bin/activate`


3. Install all the dependencies needed for the project:

`pip install -r requirements.txt`


## Instructions to run the app

1. Run the database migrations to set up your SQLite files:

`python manage.py migrate`

2. To run the Django application:

`python manage.py runserver`