import requests
from urllib.parse import quote


def image_generation_api_wrapper(input: str):
    print(f"Generating image of #{input}# ")

    base_url = "https://image.pollinations.ai/prompt/"
    formatted_prompt = quote(input)
    url = f"{base_url}{formatted_prompt}"
    print(url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return url
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
