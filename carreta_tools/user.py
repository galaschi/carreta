from carreta_tools import login_manager
from flask_login import UserMixin
from collections import defaultdict
import requests, json

user_list = []
api_key = '867FB447FE65F77F5377BDAF7EE82E73'
steam_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'


class User(UserMixin):
    __refs__ = defaultdict(list)

    def __init__(self, steam_id):
        self.id = steam_id
        user_list.append(self)
        self.user_data = self.get_user_data()
        self.steam_name = self.get_steam_name()
        self.steam_image = self.get_steam_image()
        self.steamId3 = int(steam_id) - 76561197960265728

    def get_steam_name(self):
        return self.user_data['response']['players'][0]['personaname']

    def get_steam_image(self):
        return self.user_data['response']['players'][0]['avatar']

    def get_user_data(self):
        user_data = requests.get(f'{steam_url}?key={api_key}&steamids={self.id}')
        return user_data.json()


@login_manager.user_loader
def load_user(user_id):
    for user in user_list:
        if user.id == user_id:
            return user
    return None
