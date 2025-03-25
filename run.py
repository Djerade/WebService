from app import create_app, database

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)