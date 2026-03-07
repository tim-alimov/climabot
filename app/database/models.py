from datetime import datetime
from dataclasses import dataclass
from typing import Iterator, Sequence

from app.database.wmo_codes import WMO_EMOJIS

@dataclass(frozen=True, slots=True)
class Coordinate:
    region_name: str
    lat: float
    lng: float


@dataclass(frozen=True, slots=True)
class CurrentWeather:
    temperature: float
    feels_like: float
    humidity: int
    cloud_cover: int
    wind_speed: float
    weather_code: int

    @property
    def condition_emoji(self) -> str:
        return WMO_EMOJIS.get(self.weather_code, 'No description')
    
    @property
    def formatted_message(self) -> str:
        return (
            f"<b>{self.condition_emoji}</b>\n\n"
            f"🌡 <b>Temp:</b> {self.temperature}°C\n"
            f"💧 <b>Humidity:</b> {self.humidity}%\n"
            f"🌬 <b>Wind:</b> {self.wind_speed} km/h\n"
            f"☁️ <b>Cloudiness:</b> {self.cloud_cover}%"
        )
    
    

@dataclass(frozen=True, slots=True)
class DailyWeather:
    date: str
    temperature: float
    feels_like: float
    humidity: int 
    cloud_cover: int
    weather_code: int

    @property
    def week_day(self) -> str:
        date = datetime.fromisoformat(self.date)
        return date.strftime("%a")
    
    @property
    def description(self) -> str:
        desc = WMO_EMOJIS.get(self.weather_code)
        if desc is None:
            return "Unknown"
        return desc[1:]
    
    @property
    def formatted_message(self) -> str:
        return f"{self.week_day:<3} | {self.temperature:>5}°C | 💧{self.humidity:>3}% | ☁️{self.cloud_cover:>3}%\n"


@dataclass(frozen=True, slots=True)
class ForecastWeather:
    dates: Sequence[str]
    temperatures: Sequence[float]
    feels_likes: Sequence[float]
    humidities: Sequence[int]
    cloud_covers: Sequence[int] 
    weather_codes: Sequence[int]

    @property
    def days(self) -> Iterator[DailyWeather]:
        for date, temp, feels, humidity, cloud, w_code in zip(
            self.dates,
            self.temperatures,
            self.feels_likes,
            self.humidities,
            self.cloud_covers,
            self.weather_codes,
            strict=True
        ):
            yield DailyWeather(
                date=date,
                temperature=temp,
                feels_like=feels,
                humidity=humidity,
                cloud_cover=cloud,
                weather_code=w_code
            )

    @property
    def formatted_message(self) -> str:
        return f"<pre>{''.join(daily.formatted_message for daily in self.days)}</pre>"

