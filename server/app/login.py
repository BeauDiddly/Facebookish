from flask import Flask, render_template, request

def setup_login(app: Flask):
    @app.route("/login/", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            print(request.form["name"])
            return f"<p>ur name is {request.form['name']} :))</p>"
        return render_template("login.html", name="test")
