from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place = request.form["place_name"]

    if place.strip() == "":
        return render_template("error.html", message="Please enter a valid place name.")
    
    try:
        result = mbta_helper.find_stop_near_with_weather(place)

        if result is None:
            return render_template(
                "error.html",
                message="Could not find an MBTA station for that location!!!! ."
            )

        return render_template(
            "mbta_station.html",
            place = place,
            stop = result["stop"],
            wheelchair_accessible = result["wheelchair_accessible"],
            weather = result["weather"],
            system_type=result["system_type"]
        )
    except Exception as e:
        print("FLASK ERROR:", e)
        return render_template(
            "error.html",
            message="Could not find an MBTA station for that locationn!."
        )




if __name__ == "__main__":
    app.run(debug=True)
