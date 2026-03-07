import logging
import aiohttp
from aiocache import cached

from app.database.models import CurrentWeather, ForecastWeather
from app.core.exceptions import OpenMeteoFetchingError

logger = logging.getLogger(__name__)

class WeatherAPI:
    def __init__(self, url:str, session: aiohttp.ClientSession) -> None:
        self.url = url
        self.session = session

    @cached(ttl=900)
    async def get_current_weather(self, lat:float, lng:float) -> CurrentWeather:
        try:
            params = {
            "latitude": lat,
            "longitude": lng,
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,cloud_cover"
            }

            async with self.session.get(url=self.url, params=params) as response:
                response.raise_for_status()

                data = await response.json()
                current = data.get('current')

                return CurrentWeather(
                    temperature=current.get('temperature_2m'),
                    feels_like=current.get('apparent_temperature'),
                    humidity=current.get('relative_humidity_2m'),
                    weather_code=current.get('weather_code'),
                    cloud_cover=current.get('cloud_cover'),
                    wind_speed= current.get('wind_speed_10m')
                )
        
        except TimeoutError as err:
            logger.exception("Open-meteo fetching timed out lat=%s, lng=%s", lat, lng)
            raise OpenMeteoFetchingError(err) from err
        
        except aiohttp.ClientResponseError as err:
            logger.exception("Open-meteo fetching failed lat=%s, lng=%s", lat, lng)
            raise OpenMeteoFetchingError(err) from err
        
        except aiohttp.ClientError as err:
            logger.exception("Open-meteo connection failed lat=%s, lng=%s", lat, lng)
            raise OpenMeteoFetchingError(err) from err
        
        except Exception as err:
            logger.exception('Open-meteo unknown error occurred lat=%s, lng=%s', lat, lng)
            raise OpenMeteoFetchingError(err) from err
        
    @cached(ttl=900)
    async def get_forecast(self, lat:float, lng:float) -> ForecastWeather:
        try:
            params = {
            "latitude": lat,
            "longitude": lng,
            "daily": "temperature_2m_mean,apparent_temperature_mean,cloud_cover_mean,relative_humidity_2m_mean,weather_code"
            }

            async with self.session.get(url=self.url, params=params) as response:
                response.raise_for_status()

                data = await response.json()
                daily = data.get('daily')

                return ForecastWeather(
                    dates= daily.get('time'),
                    temperatures= daily.get('temperature_2m_mean'),
                    feels_likes= daily.get('apparent_temperature_mean'),
                    cloud_covers= daily.get('cloud_cover_mean'),
                    humidities= daily.get('relative_humidity_2m_mean'),
                    weather_codes= daily.get('weather_code')
                )
        
        except TimeoutError as err:
            logger.exception("Open-meteo fetching timed out lat=%s, lng=%s", lat, lng)
            raise OpenMeteoFetchingError(err) from err
        
        except aiohttp.ClientResponseError as err:
            logger.exception("Open-meteo fetching failed lat=%s, lng=%s", lat, lng)
            raise OpenMeteoFetchingError(err) from err
        
        except aiohttp.ClientError as err:
            logger.exception("Open-meteo connection failed lat=%s, lng=%s", lat, lng)
            raise OpenMeteoFetchingError(err) from err
        
        except Exception as err:
            logger.exception('Open-meteo unknown error occurred lat=%s, lng=%s', lat, lng)
            raise OpenMeteoFetchingError(err) from err