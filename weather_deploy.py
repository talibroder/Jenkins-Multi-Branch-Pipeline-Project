from flask import Flask, render_template, request
import requests

app = Flask(__name__)
@app.route("/")
def home():
    """
    Render the home page.
    """
    return render_template("home.html")
@app.route("/city", methods=["GET", "POST"])
def get_weather():
    """
    Handle the user's input for the city, retrieve weather data, and display the results.
    """
    if request.method == "POST":
        city = request.form["city"]
        try:
            data = get_api(city)
            days = data['days'][:7]
            state = data['resolvedAddress']
            return render_template("search_result.html",
                                   day=days, city=city, state=state)
        except:
            return "Invalid City. Go back and try again."
def get_api(city):
    """
    Get weather data for a specified city from an external API.

    Args:
        city (str): The name of the city for which weather data is requested.

    Returns:
        dict: Weather data in JSON format.
    """
    url_path = ('https://weather.visualcrossing.com/'
                'VisualCrossingWebServices/rest/services/timeline/'
                + city + '?unitGroup=metric&key=HY7GXEUM2RZVWZJ79U9UJ6ASD&format=json')
    data = requests.get(url_path).json()
    return data
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

