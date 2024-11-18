import asyncio
import aiohttp
from superagentx.handler.base import BaseHandler
from superagentx.handler.decorators import tool


class CoffeeCompassHandler(BaseHandler):

    @tool
    async def find_coffee_shops(self, latitude: str, longitude: str, radius: int = 1000) -> dict:
        """
            To find the best coffee shops based on given latitude and longitude.
        """

        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
                    [out:json];
                    (
                      node["amenity"="cafe"]
                        (around:{1000},{latitude},{longitude});
                    );
                    out body;
                    """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=overpass_url,
                    data=query
            ) as resp:
                result = await resp.json()
                return result

    @tool
    async def get_lat_long(
            self,
            place: str
    ) -> dict:
        """
        Get the coordinates of a city based on a location.

        Args:
            @param place: The place name

            @return result (Str): Return the real latitude & longitude for the given place.

        """

        header_dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "referer": 'https://www.superagentx.ai'
        }
        url = "http://nominatim.openstreetmap.org/search"

        params = {
            'q': place,
            'format': 'json',
            'limit': 1
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=url,
                    params=params,
                    headers=header_dict
            ) as resp:
                resp_data = await resp.json()
                if resp_data:
                    lat = resp_data[0]["lat"]
                    lon = resp_data[0]["lon"]
                    return {
                        "latitude": lat,
                        "longitude": lon
                    }



