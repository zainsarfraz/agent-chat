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


google_search_tool = GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())

wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

youtube_search_tool = YouTubeSearchTool()

image_generation_tool = Tool(
    name="image_generation",
    description="Useful for when you need to generate an image based on a text prompt",
    func=image_generation_api_wrapper,
)

google_image_search_tool = Tool(
    name="google_images_search",
    description="Useful for when you need to search for images url on google",
    func=GoogleSerperAPIWrapper(type="images").results
)