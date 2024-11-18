import requests


def get_weather(city=None):
    if not city:
        city = input("Enter the name of the city: ")

    querystring = {"location": city, "format": "json", "u": "f"}
    url = "https://yahoo-weather5.p.rapidapi.com/weather"
    headers = {
        "x-rapidapi-key": "154dbed55dmsh1187fd5770481f8p1cf28fjsn8424d2d80d98",  # Replace with actual API key
        "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)

    try:
        temperature = data["current_observation"]["condition"]["temperature"]
        humidity = data["current_observation"]["atmosphere"]["humidity"]
        description = data["current_observation"]["condition"]["text"]
        wind_speed = data["current_observation"]["wind"]["speed"]

        print(f"City: {city}")
        print(f"Temperature: {temperature}°F")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description}")
        print(f"Wind Speed: {wind_speed} mph")

        # 3-day forecast
        print("3-Day Forecast:")
        forecast_list = []
        for index, forecast in enumerate(data.get("forecasts", [])[:3]):  # 3 days
            day = forecast["day"]
            high = forecast["high"]
            low = forecast["low"]
            forecast_text = forecast["text"]
            forecast_list.append(
                f"{index + 1}. {day}: High of {high}°F, Low of {low}°F, {forecast_text}"
            )
        print("\n".join(forecast_list))

    except KeyError:
        print("Could not find weather data.")

    return data


get_weather("Nairobi")
