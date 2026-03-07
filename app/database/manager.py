import logging
import asyncpg
from typing import Optional

from app.core.exceptions import DatabaseError
from app.database.models import Coordinate


logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, dsn:str, min_size:int = 2, max_size:int = 10) -> None:
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self._pool:Optional[asyncpg.Pool] = None


    @property
    def pool(self) -> asyncpg.Pool:
        if not self._pool:
            raise RuntimeError("Database pool is not initialized. Call connect() first.")
        return self._pool


    async def connect(self) -> None:
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=self.min_size,
                max_size=self.max_size
            )

            logger.info('Database connection established')

        
    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

            logger.info('Database connection closed')

    
    async def insert_location(self, user_id:int, lat:float, lng:float, 
                              region_name: Optional[str] = None,) -> None:
        try:
            sql = """
            INSERT INTO locations (id, region_name, lat, lng) 
            VALUES($1, $2, $3, $4)
            ON  CONFLICT(id) DO UPDATE SET
            region_name = EXCLUDED.region_name,
            lat = EXCLUDED.lat,
            lng = EXCLUDED.lng"""

            await self.pool.execute(sql, user_id, region_name, round(lat,2), round(lng,2))

            logger.info("Location inserted/updated successfully user_id=%s", user_id)

        except asyncpg.PostgresError as err:
            logger.exception("Database query failed user_id=%s query='insert_location'", user_id)
            raise DatabaseError(err) from err
        

    async def get_location(self, user_id:int) -> Optional[Coordinate]:
        try:
            sql = 'SELECT region_name, lat, lng FROM locations WHERE id = $1'
            record = await self.pool.fetchrow(sql, user_id)

            if not record:
                return None
            
            return Coordinate(**dict(record))

        except asyncpg.PostgresError as err:
            logger.exception("Database query failed user_id=%s query='select_location'", user_id)
            raise DatabaseError(err) from err