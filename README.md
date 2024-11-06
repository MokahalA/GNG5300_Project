# MealGenie


## Setup Instructions

1. Create a virtual environment (env) at root directory:

    `python3 -m venv venv`

2. Always remember to activate the virtual environment & set your VSCode interpreter to the correct path.

    Windows: `venv\Scripts\activate`

    macOS/Linux: `source venv/bin/activate`


3. Install the dependencies needed for the project:


    `pip install -r requirements.txt`


## Instructions to run the app

1. Run the database migrations to set up your SQLite

    `python manage.py migrate`

2. To start the application:

    `python manage.py runserver`