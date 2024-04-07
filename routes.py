# todos.py

from datetime import datetime
from flask import Blueprint, jsonify, request
from database import create_connection
from auth import authenticate_token

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

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todo_list")
            todos = cursor.fetchall()
            result = []
            for todo in todos:
                result.append({
                    'todo_id': todo.todo_id,
                    'user_id': todo.user_id,
                    'todo_description': todo.todo_description,
                    'created_on': todo.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_on': todo.updated_on.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': todo.status,
                    'priority': todo.priority,
                    'due_date': todo.due_date.strftime('%Y-%m-%d %H:%M:%S') if todo.due_date else None
                })
            return jsonify(result), 200
        except Exception as e:
            print("Error executing query:", e)
            return jsonify({'error': 'Error fetching todos'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection error'}), 500

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
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO todo_list (todo_id, user_id, todo_description, created_on, updated_on, status, priority, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (data.get('todo_id'),data.get('user_id'), data.get('todo_description'), datetime.utcnow(), datetime.utcnow(), data.get('status'), data.get('priority'), data.get('due_date')))
            conn.commit()
            return jsonify({'message': 'Todo created successfully'}), 201
        except Exception as e:
            print("Error executing query:", e)
            conn.rollback()
            return jsonify({'error': 'Error creating todo'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection error'}), 500

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

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE todo_list
                SET user_id=?, todo_description=?, updated_on=?, status=?, priority=?, due_date=?
                WHERE todo_id=?
            """, (data.get('user_id'), data.get('todo_description'), datetime.utcnow(), data.get('status'), data.get('priority'), data.get('due_date'), todo_id))
            conn.commit()
            return jsonify({'message': 'Todo updated successfully'}), 200
        except Exception as e:
            print("Error executing query:", e)
            conn.rollback()
            return jsonify({'error': 'Error updating todo'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection error'}), 500

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
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todo_list WHERE todo_id=?", (todo_id,))
            conn.commit()
            return jsonify({'message': 'Todo deleted successfully'}), 200
        except Exception as e:
            print("Error executing query:", e)
            conn.rollback()
            return jsonify({'error': 'Error deleting todo'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection error'}), 500
