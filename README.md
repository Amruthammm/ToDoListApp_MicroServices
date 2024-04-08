**TodoListApp Microservices**
This project implements a scalable Todo List application using microservices architecture, that provides adding, updating, deleting and retrieving list of Todo using authorization functionality.

**Features**
User authentication with token-based authorization
CRUD operations for managing todo items
Scalable architecture using Flask microservice
Interaction with SQL Server database

**Technologies Used**
Flask: Python web framework for building microservices
SQL Server: Relational database management system
pyodbc: Python library for connecting to SQL Server
requests: HTTP library for making requests to external services

**Setup**
1. Clone the repository:
git@github.com:Amruthammm/ToDoListApp_MicroServices.git
2. Install dependencies:
pip install -r requirements.txt

3. Configure the database connection:
Update the conn_str variable in database.py with your SQL Server connection string

4.Run the application:
python app.py

5. The application will start running at http://localhost:5000.
API Endpoints
i) GET /todos: Retrieve all todos
ii) POST /todos: Create a new todo
iii) PUT /todos/:todo_id: Update an existing todo
iv) DELETE /todos/:todo_id: Delete a todo

6. Authentication
To access todo endpoints, you need to provide a valid JWT token in the Authorization header.
