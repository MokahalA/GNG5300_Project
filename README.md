# MealGenie

## Contributors

| Name           | GitHub Profile                                     |
|----------------|----------------------------------------------------|
| Ahmad El Mokahal    | [@MokahalA](https://github.com/MokahalA)      |
| Shiqi Cui           | [@s-cui801](https://github.com/s-cui801)      |
| Fehmidabanu Saiyed  | [@F-saiyed](https://github.com/F-saiyed)      |
| Vibhu Puri          | [@purivibhu](https://github.com/purivibhu)    |

## Setup Instructions

1. Create a virtual environment (env) at root directory:

    `python3 -m venv venv`

    Note: Make sure you have Python 3.10+

2. Always remember to activate the virtual environment & set your VSCode interpreter to the correct path.

    Windows: `venv\Scripts\activate`

    macOS/Linux: `source venv/bin/activate`

3. Download llama3.2 (3b) from [Ollama](https://ollama.com/library/llama3.2):

    `ollama run llama3.2:3b`

4. Install the dependencies needed for the project:

    `pip install -r requirements.txt`


## Instructions to run the app

1. Run the database migrations to set up your SQLite files:

    `python manage.py migrate`

2. Populate the grocery categories in the database:
   
    `python manage.py populate_categories`

3. To start the application:

    `python manage.py runserver`