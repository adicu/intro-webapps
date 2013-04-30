from application import app, db
import routes
import os

if __name__ == '__main__':
    if not os.path.isfile('/tmp/example.db'):
        db.create_all()
    app.run()
