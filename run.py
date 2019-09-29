from app import create_app
import os

# test confg
# os.environ['FLASK_CONFIG'] = os.environ.get('FLASK_CONFIG', "development")

app = create_app()
app.run(host='127.0.0.1', port=5000, use_reloader=True)
