from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_input_data(post_data):
    if "title" not in post_data or "content" not in post_data:
        return False
    return True


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get("sort")
    direction = request.args.get("direction", "asc").lower()
    if (sort_by is not None and sort_by not in ("title", "content")
            or direction not in ("asc", "desc")):
        return jsonify({"error": "Invalid input for sort_by and direction"}), 400

    sorted_post = POSTS.copy()
    if sort_by == "title":
        sorted_post.sort(key=lambda x: x["title"], reverse=(direction == "desc"))
    elif sort_by == "content":
        sorted_post.sort(key=lambda x: x["content"], reverse=(direction == "desc"))

    return Response(json.dumps(sorted_post, indent=4, sort_keys=False), mimetype='application/json'), 201


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()
    if not validate_input_data(new_post):
        return jsonify({"error": "Invalid book data (Keys 'title' and 'content' are necessary)"}), 400

    new_id = max([post["id"] for post in POSTS]) + 1

    new_post = {
        "id": new_id,
        "title": new_post.get("title"),
        "content": new_post.get("content")
    }
    POSTS.append(new_post)

    return Response(json.dumps(new_post, indent=4, sort_keys=False), mimetype='application/json'), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_to_delete = next((post for post in POSTS if post['id'] == post_id), None)
    if not post_to_delete:
        return jsonify({"error": "Post ID is not existing"}), 404
    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    if not post_to_update:
        return jsonify({"error": "Post ID is not existing"}), 404
    new_data = request.get_json()
    new_title = new_data.get("title", None)
    new_content = new_data.get("content", None)
    if new_title:
        post_to_update["title"] = new_title
    if new_content:
        post_to_update["content"] = new_content
    return Response(json.dumps(post_to_update, indent=4, sort_keys=False), mimetype='application/json'), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    title = request.args.get("title")
    content = request.args.get("content")

    if not title and not content:
        return jsonify([])

    search_results = [post for post in POSTS if
                      (title is None or title.lower() in post["title"].lower()) and
                      (content is None or title.lower() in post["content"].lower())]

    return Response(json.dumps(search_results, indent=4, sort_keys=False), mimetype='application/json'), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
