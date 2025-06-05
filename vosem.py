from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/photos")
def photos():
    photos = []
    for file in os.listdir("static/img/photos"):
        info = file.split(".")[0]
        date, desc, locale = info.split("|")
        photos.append(
            {
                "date": date,
                "desc": desc.replace("_", " ").capitalize(),
                "local": locale.replace("_", " "),
                "img": "static/img/photos/" + file,
            }
        )
    return render_template("photos.html", photos=photos)

if __name__ == "__main__":
    app.run()
