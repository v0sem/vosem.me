from flask import Flask, render_template
import os
from exif import Image
from geopy import Nominatim

app = Flask(__name__)

def get_locale(latitude, longitude):
    dlat = (-1 if latitude[4] == "S" else 1)* (latitude[0] + latitude[1] / 60 + latitude[2] / 3600)
    dlon = (-1 if longitude[4] == "W" else 1)* (longitude[0] + longitude[1] / 60 + longitude[2] / 3600)

    gl = Nominatim(user_agent="GetLoc")
    return gl.reverse(f"{dlat}, {dlon}")

def get_file_meta(filepath):
    with open(filepath, "rb") as photof:
        photoi = Image(photof)

    if photoi.has_exif:
        locale = None
        if photoi.get("gps_latitude", "--") != "--":
            locale = get_locale(photoi.gps_latitude + [photoi.gps_latitude_ref], photoi.gps_longitude + [photoi.gps_longitude_ref])

        return photoi.get("image_description", "--"), photoi.get("datetime_original", "--"), locale or "--"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/photos")
def photos():
    photos = []
    for file in os.listdir("static/img/photos"):
        mdata = get_file_meta("static/img/photos/" + file)

        if mdata is None:
            continue

        desc, date, locale = mdata
        photos.append(
            {
                "date": date,
                "desc": desc,
                "local": locale,
                "img": "static/img/photos/" + file,
            }
        )
    return render_template("photos.html", photos=photos)

if __name__ == "__main__":
    app.run()
