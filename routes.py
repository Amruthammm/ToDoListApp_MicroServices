# todos.py

from datetime import datetime
from models import TodoList
from flask import Blueprint, jsonify, request
from database import create_connection
from auth import authenticate_token
from database import db

routes = Blueprint('todos', __name__)

@routes.route('/todos', methods=['GET'])

def get_todos():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Token is missing'}), 401

    # Extract the token from the "Bearer" scheme
    token = token.split(" ")[1] if token.startswith("Bearer ") else None

    if not token:
        return jsonify({'error': 'Invalid token format'}), 401

    if not authenticate_token(token):
        return jsonify({'error': 'Invalid token'}), 401

    try:
        # Query all todos from the database
        todos = TodoList.query.all()

        # Convert TodoList objects to dictionaries
        result = [{
            'todo_id': todo.todo_id,            
            'todo_description': todo.todo_description,
            'created_on': todo.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_on': todo.updated_on.strftime('%Y-%m-%d %H:%M:%S'),
            'status': todo.status,
            'priority': todo.priority,
            'due_date': todo.due_date.strftime('%Y-%m-%d %H:%M:%S') if todo.due_date else None
        } for todo in todos]

        return jsonify(result), 200
    except Exception as e:
        print("Error fetching todos:", e)
        return jsonify({'error': 'Error fetching todos'}), 500
    

@routes.route('/todos', methods=['POST'])
def create_todo():
    token = request.headers.get('Authorization')
    data = request.json

    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    # Extract the token from the "Bearer" scheme
    token = token.split(" ")[1] if token.startswith("Bearer ") else None
    if not token:
        return jsonify({'error': 'Invalid token format'}), 401

    if not authenticate_token(token):
        return jsonify({'error': 'Invalid token'}), 401
    try:
        # Create a new TodoList object
        todo = TodoList(
            todo_id=data.get('todo_id'),
            todo_description=data.get('todo_description'),
            created_on=datetime.utcnow(),
            updated_on=datetime.utcnow(),
            status=data.get('status'),
            priority=data.get('priority'),
            due_date=data.get('due_date')
        )
        # Add the new TodoList object to the database session
        db.session.add(todo)
        db.session.commit()
        return jsonify({'message': 'Todo created successfully'}), 201
    except Exception as e:
        print("Error creating todo:", e)
        db.session.rollback()
        return jsonify({'error': 'Error creating todo'}), 500
    
@routes.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    token = request.headers.get('Authorization')
    data = request.json

    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    # Extract the token from the "Bearer" scheme
    token = token.split(" ")[1] if token.startswith("Bearer ") else None
    if not token:
        return jsonify({'error': 'Invalid token format'}), 401
    if not authenticate_token(token):
        return jsonify({'error': 'Invalid token'}), 401
    try:
        # Query the todo to update
        todo = TodoList.query.filter_by(todo_id=todo_id).first()
        if todo:
            # Update todo attributes
            todo.todo_description = data.get('todo_description')
            todo.updated_on = datetime.utcnow()
            todo.status = data.get('status')
            todo.priority = data.get('priority')
            todo.due_date = data.get('due_date')
            # Commit changes to the database
            db.session.commit()

            return jsonify({'message': 'Todo updated successfully'}), 200
        else:
            return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        print("Error updating todo:", e)
        db.session.rollback()
        return jsonify({'error': 'Error updating todo'}), 500

@routes.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Token is missing'}), 401

    # Extract the token from the "Bearer" scheme
    token = token.split(" ")[1] if token.startswith("Bearer ") else None
    if not token:
        return jsonify({'error': 'Invalid token format'}), 401

    if not authenticate_token(token):
        return jsonify({'error': 'Invalid token'}), 401
 
    try:
        # Query the todo to delete
        todo = TodoList.query.filter_by(todo_id=todo_id).first()

        if todo:
            # Delete the todo
            db.session.delete(todo)
            db.session.commit()

            return jsonify({'message': 'Todo deleted successfully'}), 200
        else:
            return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        print("Error deleting todo:", e)
        db.session.rollback()
        return jsonify({'error': 'Error deleting todo'}), 500
