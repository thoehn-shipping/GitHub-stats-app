import os
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    username = request.args.get("username")
    
    if not username:
        return """
            <h1>GitHub Stats Lookup</h1>
            <form>
                <input name="username" placeholder="Enter GitHub username">
                <button type="submit">Look up</button>
            </form>
        """
    
    response = requests.get(f"https://api.github.com/users/{username}")
    
    if response.status_code != 200:
        return f"<h1>User '{username}' not found.</h1><a href='/'>Try again</a>"
    
    data = response.json()
    
    return f"""
        <h1>{data.get('name') or data['login']}</h1>
        <p><strong>Bio:</strong> {data.get('bio') or 'No bio'}</p>
        <p><strong>Public repos:</strong> {data['public_repos']}</p>
        <p><strong>Followers:</strong> {data['followers']}</p>
        <p><strong>Following:</strong> {data['following']}</p>
        <a href='/'>Look up another user</a>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)