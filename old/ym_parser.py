from bs4 import BeautifulSoup
import requests
from time import sleep

def get_time_from_yamaps(start, end, date, time):
    sleep(1)

    url = f'https://yandex.ru/maps/?ll=39.908396%2C50.795065&mode=routes&routes%5BtimeDependent%5D%5Btime%5D={date}T{time[0]}%3A{time[1]}%3A00&rtext={start[0]}%2C{start[1]}~{end[0]}%2C{end[1]}&rtt=auto&ruri=~&z=14'

    routes = []

    d = BeautifulSoup(requests.get(url).text, "html.parser").findAll('div', class_='auto-route-snippet-view__route-title-primary')
    for route in d:
        routes.append(str(route).replace('<div class="auto-route-snippet-view__route-title-primary">', '').replace('</div>', '').replace(' ч ' , ':').replace(' мин', '').replace('\xa0', ' '))
    
    if len(routes) == 0:
        print(requests.get(url).text)

    routes = [int(e) for e in routes[0].split(":")]

    if len(routes) == 1:
        return routes[0]

    return routes[0] * 60 + routes[1]

def get_address_from_cords(cords):
    url = f'https://yandex.ru/maps/?ll=47.900240%2C47.203171&mode=routes&rtext={cords[0]}%2C{cords[1]}&rtt=auto&ruri=~&z=14'

    inputs = []

    for inp in BeautifulSoup(requests.get(url).text, "html.parser").findAll('input', class_='input__control'):
        inp = str(inp)
        inp = inp[inp.find('value') + 7:].replace('"/>', '')

        if inp != '':
            inputs.append(inp)

    return inputs[0]

#print(get_time_from_yamaps([55.837788, 37.617321], [55.6058121, 37.2882462], '2021-11-08', ['17', '30']))