import logging
import aiohttp

from asyncio import TimeoutError
from typing import Optional

from app.database.regions import REGION_TRANSLATIONS
from app.core.exceptions import GeocodeFetchingError


logger = logging.getLogger(__name__)

async def get_region_name(session: aiohttp.ClientSession, lat: float, lng: float) -> Optional[str]:
    url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lng}&localityLanguage=en"
    
    try:
        async with session.get(url) as response:
            
            response.raise_for_status()
            data = await response.json()
            raw_region = data.get('principalSubdivision')

            if not raw_region:
                logger.warning('Geocoding fetching skipped lat=%s, lng=%s')
                return None
                
            clean_region = raw_region.removesuffix('Region').strip()

            return REGION_TRANSLATIONS.get(clean_region, clean_region)


    except TimeoutError as err:
        logger.exception("Geocoding fetching timed out lat=%s, lng=%s", lat, lng)
        raise GeocodeFetchingError(err) from err
    
    except aiohttp.ClientResponseError as err:
        logger.exception("Geocoding fetching failed lat=%s, lng=%s", lat, lng)
        raise GeocodeFetchingError(err) from err
    
    except aiohttp.ClientError as err:
        logger.exception("Geocoding connection failed lat=%s, lng=%s", lat, lng)
        raise GeocodeFetchingError(err) from err
    
    except Exception as err:
        logger.exception('Geocoding unknown error occurred lat=%s, lng=%s', lat, lng)
        raise GeocodeFetchingError(err) from err