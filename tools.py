# tools.py

def get_weather(city: str) -> str:
    """Returns the current weather for a given city to help with trip planning."""
    # This is where you'd eventually put a real API call
    if "London" in city:
        return "It is 10°C and raining in London."
    elif "Lagos" in city:
        return "It is 32°C and sunny in Lagos."
    else:
        return f"The weather in {city} is mild and cloudy."

def save_to_file(filename: str, content: str) -> str:
    """Saves text content to a file on the local computer."""
    with open(filename, "w") as f:
        f.write(content)
    return f"Successfully saved content to {filename}"