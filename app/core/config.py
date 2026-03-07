from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    BOT_TOKEN:str
    DEBUG_MODE:bool = False
    WEATHER_BASE_URL:str

    model_config = SettingsConfigDict(
        env_file= '.env',
        env_file_encoding= 'utf-8',
        extra='ignore'
    )

settings = Settings() #type:ignore