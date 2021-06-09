from lxml import html
import requests
import urllib3
import json
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_base = 'https://dota2protracker.com'
heroes = []


def get_heroes():
    page = requests.get(url_base, verify=False)
    tree = html.fromstring(page.content)
    heroes_list = tree.xpath("//table[@id = 'table_id']/tbody//a")

    for hero in heroes_list:
        if '  ' not in hero.text:
            hero_name = hero.text.replace(' ', '%20')
            heroes.append(hero_name)


def get_hero_data(pos):
    data_hero = []
    data_match = []
    data_winrate = []

    for hero in heroes:
        url_hero = url_base + '/hero/' + hero
        page = requests.get(url_hero, verify=False)
        tree = html.fromstring(page.content)

        matches, winrate = get_data(pos, tree)

        if matches > 0:
            data_hero.append(hero.replace('%20','_'))
            data_match.append(matches)
            data_winrate.append(winrate)

    return data_hero, data_match, data_winrate


def clean_str(string):
    string = string.replace('\n', '')
    string = string.replace('  ', '')
    return string


def get_data(pos, tree):
    return {
        0: get_total_data(tree),
        1: get_hc_data(tree),
        2: get_mid_data(tree),
        3: get_off_data(tree),
        4: get_sup_data(tree),
        5: get_hsup_data(tree)
    }[pos]


def get_total_data(tree):
    try:
        total_heroi = tree.xpath("//div[@class = 'hero-stats-descr']")[0].text
        matches = clean_str(total_heroi).split(' ')[1]
        winrate = clean_str(total_heroi).split('of')[-1].replace('%', '')
        return int(matches), float(winrate)
    except ValueError:
        return 0, 0


def get_hc_data(tree):
    try:
        pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Carry']/div[1]/div")
        matches = pos_matches.text.split(' ')[0].replace('%', '')
        winrate = pos_winrate.text.split(' ')[0].replace('%', '')
        return float(matches), float(winrate)
    except ValueError:
        return 0, 0


def get_mid_data(tree):
    try:
        pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Mid']/div[1]/div")
        matches = pos_matches.text.split(' ')[0].replace('%', '')
        winrate = pos_winrate.text.split(' ')[0].replace('%', '')
        return float(matches), float(winrate)
    except ValueError:
        return 0, 0


def get_off_data(tree):
    try:
        pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Offlane']/div[1]/div")
        matches = pos_matches.text.split(' ')[0].replace('%', '')
        winrate = pos_winrate.text.split(' ')[0].replace('%', '')
        return float(matches), float(winrate)
    except ValueError:
        return 0, 0


def get_sup_data(tree):
    try:
        pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Support (4)']/div[1]/div")
        matches = pos_matches.text.split(' ')[0].replace('%', '')
        winrate = pos_winrate.text.split(' ')[0].replace('%', '')
        return float(matches), float(winrate)
    except ValueError:
        return 0, 0


def get_hsup_data(tree):
    try:
        pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Support (5)']/div[1]/div")
        matches = pos_matches.text.split(' ')[0].replace('%', '')
        winrate = pos_winrate.text.split(' ')[0].replace('%', '')
        return float(matches), float(winrate)
    except ValueError:
        return 0, 0


def update_data():
    get_heroes()
    data = {}

    for pos in range(6):
        data_hero, data_match, data_winrate = get_hero_data(pos)
        data[pos] = {'hero': data_hero, 'match': data_winrate, 'winrate': data_winrate}

    if os.path.exists('carreta_tools/static/data.json'):
        os.remove('carreta_tools/static/data.json')

    with open('carreta_tools/static/data.json', 'w') as outfile:
        json.dump(data, outfile)
