from langchain_community.utilities import GoogleSerperAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import (
    WikipediaQueryRun,
    GoogleSerperRun,
    YouTubeSearchTool,
)
from langchain_community.tools import Tool
from custom_tools.image_generation_tool import image_generation_api_wrapper
from dotenv import load_dotenv

load_dotenv()


google_search_tool = GoogleSerperRun(
    api_wrapper=GoogleSerperAPIWrapper(),
    metadata={
        "display_text": "Search for information on google",
        "name": "Google Search",
    },
)

wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(),
    metadata={
        "display_text": "Search for information on wikipedia",
        "name": "Wikipedia Search",
    },
)

youtube_search_tool = YouTubeSearchTool(
    metadata={
        "display_text": "Search for video links on youtube",
        "name": "YouTube Search",
    }
)

image_generation_tool = Tool(
    name="image_generation",
    description="Useful for when you need to generate an image based on a text prompt",
    func=image_generation_api_wrapper,
    metadata={
        "display_text": "Generate an image based on a text prompt",
        "name": "Image Generation",
    },
)

google_image_search_tool = Tool(
    name="google_images_search",
    description="Useful for when you need to search for images url on google",
    func=GoogleSerperAPIWrapper(type="images").results,
    metadata={
        "display_text": "Search for images on google",
        "name": "Google Image Search",
    },
)

all_tools = [
    google_search_tool,
    wikipedia_tool,
    youtube_search_tool,
    image_generation_tool,
    google_image_search_tool,
]
