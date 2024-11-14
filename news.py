import requests

def get_topics():
    url = "https://news-api14.p.rapidapi.com/v2/info/topics"
    headers = {
        "x-rapidapi-key": "a3f9f07565msh96d3248c8e65690p1c5e4bjsnde60b0b3ffca",  
        "x-rapidapi-host": "news-api14.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 

        data = response.json()
        main_topics = [topic["name"] for topic in data.get("data", []) if "name" in topic]
        return main_topics if main_topics else []

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch topics: {e}")
        return []

def get_news(categories=None):
    url = "https://news-api14.p.rapidapi.com/v2/trendings"

    if categories is None:
        topics = get_topics()
        if topics:
            print("Today's Main Topics:")
            for index, topic in enumerate(topics, start=1):
                print(f"{index}. {topic}")
            selected_index = input("Choose a topic number or type the topic name: ")
            try:
                categories = topics[int(selected_index) - 1]  
            except (ValueError, IndexError):
                categories = selected_index  
        else:
            print("No main topics available.")
            return

    querystring = {"topic": categories, "language": "en"}
    headers = {
        "x-rapidapi-key": "a3f9f07565msh96d3248c8e65690p1c5e4bjsnde60b0b3ffca",  
        "x-rapidapi-host": "news-api14.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()

        data = response.json()
        articles = data.get("data", [])

        if not articles:
            print("No articles available for this topic.")
            return

        for article in articles:
            title = article.get("title", "No title available")
            url = article.get("url", "No URL available")
            excerpt = article.get("excerpt", "No excerpt available")
            date = article.get("date", "No date available")

            print("\n----------------------------")
            print(f"Title: {title}")
            print(f"Link: {url}")
            print(f"Excerpt: {excerpt}")
            print(f"Date Published: {date}")

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
    except KeyError:
        print("Unexpected data format received.")


# topics = get_topics()
# print(topics)

get_news('Sports')
