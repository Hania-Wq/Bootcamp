from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory "database"
todos = []
next_id = 1

def find_todo(todo_id):
    return next((t for t in todos if t["id"] == todo_id), None)

# CREATE
@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, description="Title is required")

    todo = {
        "id": next_id,
        "title": data["title"],
        "done": data.get("done", False)
    }
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

# READ ALL
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos), 200

# READ ONE
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        abort(404, description="Todo not found")
    return jsonify(todo), 200

# UPDATE
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        abort(404, description="Todo not found")

    data = request.get_json()
    todo["title"] = data.get("title", todo["title"])
    todo["done"] = data.get("done", todo["done"])
    return jsonify(todo), 200

# DELETE
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        abort(404, description="Todo not found")
    todos.remove(todo)
    return jsonify({"message": "Todo deleted"}), 200

# Error handler for cleaner JSON errors
@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({"error": str(e.description)}), e.code

if __name__ == "__main__":
    app.run(debug=True)