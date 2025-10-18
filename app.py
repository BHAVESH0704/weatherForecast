from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# ✅ Your OpenWeatherMap API key
API_KEY = "44b9cf64915fb1ec683f5de8c4b1c76e"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    bg_gif = "default.gif"

    if request.method == 'POST':
        city = request.form['city'].strip().title()  # Clean input, e.g. " new york " -> "New York"
        city = city.replace(" ", "+")  # Handle spaces for URL encoding

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        
        try:
            data = response.json()
        except ValueError:
            weather_data = {"error": "Unable to process weather data. Please try again."}
            return render_template('index.html', weather=weather_data, bg_gif=bg_gif)

        # ✅ Handle success (cod = 200)
        if data.get("cod") == 200:
            desc = data["weather"][0]["description"].lower()

            # ✅ Weather details dictionary
            weather_data = {
                "city": data.get("name", "Unknown"),
                "country": data["sys"].get("country", ""),
                "temp": round(data["main"].get("temp", 0), 1),
                "humidity": data["main"].get("humidity", 0),
                "wind": data["wind"].get("speed", 0),
                "desc": desc.title(),
                "icon": data["weather"][0].get("icon", "")
            }

            # ✅ Background animation logic
            if "rain" in desc:
                bg_gif = "rain.gif"
            elif "cloud" in desc:
                bg_gif = "cloud.gif"
            elif "snow" in desc:
                bg_gif = "snow.gif"
            elif "clear" in desc or "sun" in desc:
                bg_gif = "sunny.gif"
            elif "storm" in desc or "thunder" in desc:
                bg_gif = "storm.gif"
            else:
                bg_gif = "default.gif"
        else:
            # ✅ Handle invalid city names
            message = data.get("message", "City not found.")
            weather_data = {"error": f"❌ {message.capitalize()} — please check the spelling."}

    return render_template('index.html', weather=weather_data, bg_gif=bg_gif)


if __name__ == "__main__":
    app.run(debug=True)
