from app import app
from app.resources import api

  # Registrar os recursos (APIs) no aplicativo Flask
api.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
