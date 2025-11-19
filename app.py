from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html") #replaces the plain text with the HTML template

@app.route("/nearest_mbta", methods=["POST"]) #specifies that this route will only accept POST requests
def nearest_mbta():
    place = request.form["place_name"]

    if place.strip() == "":
        return render_template("error.html", message = "Please enter a valid place name.")
    
    try:
        stop, wheelchair_accessible = mbta_helper.find_stop_near(place)
        return render_template(
            "mbta_station.html",
            place = place,
            stop = stop,
            wheelchair_accessible = wheelchair_accessible
        )
    except:
        return render_template(
            "error.html", 
            message = "Could not find an MBTA station for that location.")


if __name__ == "__main__":
    app.run(debug=True)
