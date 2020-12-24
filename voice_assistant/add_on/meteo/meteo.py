from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps


class Meteo:
    def __init__(self, city):
        self.city = city
        config_dict = get_default_config()
        config_dict['language'] = 'ja'
        self.owm = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa')
        self.mgr = self.owm.weather_manager()

    def current_weather(self):
        observation = self.mgr.weather_at_place(f"{self.city},jp")
        w = observation.weather

        return {
            'detailed_status': w.detailed_status,
            'wind': w.wind(),
            'humidity': w.humidity,
            'temperature': w.temperature('celsius'),
            'rain': w.rain,
            'heat_index': w.heat_index,
            'clouds': w.clouds,
        }

    def forecast_weather(self):
        forecast = self.mgr.forecast_at_place(f"{self.city},jp", '3h')
        w = forecast.get_weather_at(timestamps.tomorrow())

        return {
            'detailed_status': w.detailed_status,
            'wind': w.wind(),
            'humidity': w.humidity,
            'temperature': w.temperature('celsius'),
            'rain': w.rain,
            'heat_index': w.heat_index,
            'clouds': w.clouds,
        }


if __name__ == '__main__':
    me = Meteo('osaka')
    print(me.current_weather())
    print(me.forecast_weather())

