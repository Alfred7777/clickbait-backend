import os
from . import create_app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 6666))
    app.run(host = '0.0.0.0', port = port)    
    