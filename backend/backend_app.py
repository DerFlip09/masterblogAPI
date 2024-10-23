from flask import Flask, jsonify, request
from flask_cors import CORS

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
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()
    if not validate_input_data(new_post):
        return jsonify({"error": "Invalid book data (Keys 'title' and 'content' are necessary)"}), 400

    new_id = max([post["id"] for post in POSTS]) + 1

    new_post = {
        "id": new_id,
        "title": new_post["title"],
        "content": new_post["content"]
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_to_delete = next((post for post in POSTS if post['id'] == post_id), 0)
    if not post_to_delete:
        return jsonify({"error": "Post ID is not existing"}), 404
    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
