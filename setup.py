from flaskBlog import app
from dotenv import load_dotenv, find_dotenv
if __name__ == "__main__":
    load_dotenv(find_dotenv())
    app.run(debug=True)
    