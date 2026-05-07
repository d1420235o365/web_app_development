"""
app.py
Flask 應用程式啟動點。
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
