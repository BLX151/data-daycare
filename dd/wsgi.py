from main import app
from werkzeug.debug import DebuggedApplication
app7 = DebuggedApplication(app, True)

if __name__ == "__main__":
    app.run()