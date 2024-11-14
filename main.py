import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import time


from weather import get_weather
from news import get_news


load_dotenv()
BOT_TOKEN = os.getenv("Telegram_Token")



def format_weather_data(data, city):
    if data:
        temperature = data["current_observation"]["condition"]["temperature"]
        humidity = data["current_observation"]["atmosphere"]["humidity"]
        description = data["current_observation"]["condition"]["text"]
        wind_speed = data["current_observation"]["wind"]["speed"]
        return (
            f"**Weather in {city}**\n"
            f"Temperature: {temperature}°F\n"
            f"Humidity: {humidity}%\n"
            f"Condition: {description}\n"
            f"Wind Speed: {wind_speed} mph\n"
        )
    return "No weather data available."


def format_forecast_data(data):
    forecast_response = "\n**3-Day Forecast:**\n"
    for index, forecast in enumerate(data["forecasts"][:3]):  # 3-day forecast
        day = forecast["day"]
        high = forecast["high"]
        low = forecast["low"]
        forecast_text = forecast["text"]
        forecast_response += (
            f"{index + 1}. {day}: High of {high}°F, Low of {low}°F, {forecast_text}\n"
        )
    return forecast_response



def format_news_data(data):
    if data and isinstance(data, list):  
        response = "**Top News Articles:**\n"
        for article in data[:5]:  # at least 5
            title = article.get("title", "No title")
            url = article.get("url", "No URL")
            excerpt = article.get("excerpt", "No description")
            response += f"\n**Title**: {title}\n**Link**: {url}\n**Description**: {excerpt}\n"
        return response
    return "No news data available."


# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Use /weather <city> to get the weather or /news <topic> for news."
    )


# Weather
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
        weather_data = get_weather(city)

        weather_message = format_weather_data(weather_data, city)

        await update.message.reply_text(weather_message)

        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data=f"forecast_{city}"),
                InlineKeyboardButton("No", callback_data="no_forecast"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Would you like to see a 3-day forecast?", reply_markup=reply_markup
        )

    else:
        await update.message.reply_text(
            "Please specify a city, e.g., /weather Nairobi."
        )


async def handle_forecast_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    city = query.data.split("_")[1] if query.data.startswith("forecast_") else None

    if city:

        weather_data = get_weather(city)

        forecast_message = format_forecast_data(weather_data)
        await query.answer()
        await query.edit_message_text(forecast_message)

    elif query.data == "no_forecast":
        # await query.answer()
        await query.edit_message_text("You chose not to see the forecast.")



user_last_command_time = {}

# Rate limit 
RATE_LIMIT_SECONDS = 10  

# News
async def news_command(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id  
    current_time = time.time()  

    
    if user_id in user_last_command_time:
        last_command_time = user_last_command_time[user_id]
        if current_time - last_command_time < RATE_LIMIT_SECONDS:
            remaining_time = RATE_LIMIT_SECONDS - (current_time - last_command_time)
            await update.message.reply_text(f"Please wait {int(remaining_time)} seconds before using this command again.")
            return

   
    user_last_command_time[user_id] = current_time

    if context.args:
        topic = " ".join(context.args)
        # print(f"Debug: Topic : {topic}")  
        try:
            news_data = get_news(topic)
            # print(f"Debug: news data: {news_data}")  

            if news_data:  
                response = format_news_data(news_data)
                # print(f"Debug: Formatted response: {response}")  
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("No news articles found for this topic.")
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {str(e)}")
    else:
        await update.message.reply_text(
            "Please specify a topic, e.g., /news Technology."
        )


# run bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("news", news_command))

    application.add_handler(
        CallbackQueryHandler(handle_forecast_response, pattern="forecast_")
    )

    application.run_polling()


if __name__ == "__main__":
    main()
