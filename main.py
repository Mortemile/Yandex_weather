import matplotlib
import requests
import json
from matplotlib import pyplot as plt
import datetime

from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

from geopy import geocoders

import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


class Yandex_weather:
    def __init__(self, city):
        self.longitude = None
        self.latitude = None
        self.token = '1a7c29b2-384b-461f-8ff5-62c3e784f8ed'
        self.forecast_week_temp = []
        self.date = []
        self.city = city

        self.now_temp = None
        self.feels_like = None
        self.condition = None

    def geo_pos(self):  # get location of city
        city = self.city

        try:
            geolocator = geocoders.Nominatim(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
            self.latitude = str(geolocator.geocode(city).latitude)
            self.longitude = str(geolocator.geocode(city).longitude)
            print(self.latitude, self.longitude)
            return self.latitude, self.longitude

        except AttributeError:
            return 'Can not find city :('

    def get_data(self):
        api_url = f'https://api.weather.yandex.ru/v2/forecast?lat={self.latitude}&lon={self.longitude}&limit=7'  # тариф тестовый
        yandex_req = requests.get(api_url, headers={'X-Yandex-API-Key': self.token}, verify=False)
        yandex_json = json.loads(yandex_req.text)

        for day in yandex_json['forecasts']:  # week forecast
            self.forecast_week_temp.append(day['parts']['day_short']['temp'])
            self.date.append(day['date'])

        self.now_temp = yandex_json['fact']['temp']  # weather now
        self.feels_like = yandex_json['fact']['feels_like']
        self.condition = yandex_json['fact']['condition']

    def create_hist(self):
        # 1st variant

        # my_cmap = plt.get_cmap("viridis")
        # rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
        # # plt.colorbar()
        # plt.bar(self.date, self.forecast_week_temp, color=my_cmap(rescale(self.forecast_week_temp)))

        # 2st variant

        plt.figure(figsize=(25 / 2.54, 19 / 2.54))

        ax = plt.subplot()
        ax.set_xticks(ticks=[0, 1, 2, 3, 4, 5, 6],
                      labels=self.date)
        ax.set_yticks([])
        ax.set_title(f'Weekly weather forecast for {self.city}')

        im = ax.imshow(np.array(self.forecast_week_temp * 5).reshape(5, 7))

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)

        plt.colorbar(im, cax=cax)

        ms = datetime.datetime.now().strftime("%f")  # microseconds, to name file

        plt.savefig(f'Forecast for {self.city}_{ms}.png')

        # plt.show()

        return ms


def main():
    a = Yandex_weather('санкт-петербург')
    a.geo_pos()
    a.get_data()
    a.create_hist()


if __name__ == '__main__':
    main()
