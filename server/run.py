from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="26.170.28.0", port="5000", debug=True)
