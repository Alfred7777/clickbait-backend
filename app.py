import os
from __init__ import create_app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 62266))
    app.run(host = '0.0.0.0', port = port)
else:
    gunicorn_app = create_app()
