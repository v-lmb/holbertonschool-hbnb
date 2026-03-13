from app import create_app, db

app = create_app()

# Create tables in the DB if they don't exist yet
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
