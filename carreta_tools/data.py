from lxml import html
import requests
import urllib3
import json
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Data:

    def __init__(self):
        self.data = {}
        self.url_base = 'https://dota2protracker.com'
        self.page = requests.get(self.url_base, verify=False)
        self.tree = html.fromstring(self.page.content)
        self.heroes = self.tree.xpath("//td[@class = 'dt-body-left']/a/@title")
        self.get_heroes()
        self.get_hero_data()

    def get_heroes(self):
        for hero in self.heroes:
            self.data[hero] = {'general': {'matches': self.get_hero_picks(hero), 'winrate': self.get_hero_winrate(hero)}}

    def get_hero_picks(self, hero):
        picks = self.tree.xpath(f"//td[@class = 'dt-body-left']/a[@title = \"{hero}\"]/parent::td/following-sibling::td[1]")[0]
        picks_text = picks.text
        return picks_text

    def get_hero_winrate(self, hero):
        winrate = self.tree.xpath(f"//td[@class = 'dt-body-left']/a[@title = \"{hero}\"]/parent::td/following-sibling::td[2]")[0]
        winrate_text = winrate.text.replace('%', '')
        return winrate_text

    def get_hero_data(self):
        for hero in self.heroes:
            hero_name_fixed = hero.replace(' ', '%20')
            url_hero = self.url_base + '/hero/' + hero_name_fixed
            hero_page = requests.get(url_hero, verify=False)
            tree = html.fromstring(hero_page.content)

            for pos in range(1, 6):
                pos_matches_percent, pos_winrate = self.get_data(pos, tree)
                if pos_matches_percent > 0:
                    self.data[hero][pos] = {'matches': self.get_matches_by_position(hero, pos_matches_percent), 'winrate': pos_winrate}

    def get_matches_by_position(self, hero, pos_matches_percent):
        total_matches = float(self.data[hero]['general']['matches'])
        pos_matches_percent = float(pos_matches_percent)

        matches_by_position = (pos_matches_percent * total_matches)/100
        return int(round(matches_by_position))

    def get_data(self, pos, tree):
        return {
            1: self.get_hc_data(tree),
            2: self.get_mid_data(tree),
            3: self.get_off_data(tree),
            4: self.get_sup_data(tree),
            5: self.get_hsup_data(tree)
        }[pos]

    def get_hc_data(self, tree):
        try:
            pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Carry']/div[1]/div")
            matches = fix_number_percentual_data(pos_matches)
            winrate = fix_number_percentual_data(pos_winrate)
            return matches, winrate
        except ValueError:
            return 0, 0

    def get_mid_data(self, tree):
        try:
            pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Mid']/div[1]/div")
            matches = fix_number_percentual_data(pos_matches)
            winrate = fix_number_percentual_data(pos_winrate)
            return matches, winrate
        except ValueError:
            return 0, 0

    def get_off_data(self, tree):
        try:
            pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Offlane']/div[1]/div")
            matches = fix_number_percentual_data(pos_matches)
            winrate = fix_number_percentual_data(pos_winrate)
            return matches, winrate
        except ValueError:
            return 0, 0

    def get_sup_data(self, tree):
        try:
            pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Support (4)']/div[1]/div")
            matches = fix_number_percentual_data(pos_matches)
            winrate = fix_number_percentual_data(pos_winrate)
            return matches, winrate
        except ValueError:
            return 0, 0

    def get_hsup_data(self, tree):
        try:
            pos_matches, pos_winrate = tree.xpath("//div[@id = 'role_Support (5)']/div[1]/div")
            matches = fix_number_percentual_data(pos_matches)
            winrate = fix_number_percentual_data(pos_winrate)
            return matches, winrate
        except ValueError:
            return 0, 0

    def data_to_json(self):
        if os.path.exists('carreta_tools/static/data.json'):
            os.remove('carreta_tools/static/data.json')

        with open('carreta_tools/static/data.json', 'w') as outfile:
            json.dump(self.data, outfile)


def fix_number_percentual_data(number):
    fixed_number = number.text.split(' ')[0].replace('%', '')
    return float(fixed_number)


def prepare_data(position):
    hero_data, match_data, winrate_data = [], [], []
    f = open('carreta_tools/static/data.json')
    data = json.load(f)

    for hero in data:
        for pos in data[hero]:
            if pos != 'general':
                if pos == str(position):
                    hero_data.append(hero)
                    match_data.append(data[hero][pos]['matches'])
                    winrate_data.append(data[hero][pos]['winrate'])
    return hero_data, match_data, winrate_data
