"""
1. Get summonerId
2. Add Queue game info
3. Parsing and add DB

DB - SQLite3
Back Queue - Celery
"""
import re

import requests
import cell_parser

from urllib.parse import urljoin
from bs4 import BeautifulSoup


class GameInfoParser:
    """
    Parsing Game Info from op.gg.
    """

    host = 'https://www.op.gg/'
    summoner_info_url_format = urljoin(host, 'summoner/userName=%s')
    ingame_info_url_format = urljoin(host, 'summoner/matches/ajax/detail/gameId=%s&summonerId=%s')

    def __init__(self, nickname):
        self.nickname = nickname

        self.summonerId, self.games = self.get_summoner_id_and_games()

    @staticmethod
    def get_response_with_soup(url):
        return BeautifulSoup(requests.get(url).content, 'lxml')

    def get_summoner_id_and_games(self):
        soup = self.get_response_with_soup(self.summoner_info_url_format % self.nickname)
        container = soup.find('div', {'class': 'GameListContainer'})
        summoner_id = container['data-summoner-id']

        def get_game_list(cont):
            game_htmls = cont.findAll('div', {'class': 'GameItemWrap'})

            game_ids = []

            for html in game_htmls:
                a_tag = html.find('a', {'class': 'Button MatchDetail'})
                event_string = a_tag['onclick']

                game_id, game_summoner_id = re.findall('\d+', event_string)

                try:
                    assert game_summoner_id == summoner_id
                except AssertionError:
                    continue
                else:
                    game_ids.append(game_id)

            return game_ids

        return summoner_id, get_game_list(container)

    @staticmethod
    def parse_team_info(team_html_table):
        """
            'ChampionImage': None,
            'SummonerSpell': None,
            'KeystoneMastery': None,
            'SummonerName': None,
            'Items': None,
            'KDA': None,
            'Damage': None,
            'Ward': None,
            'CS': None,
            'Gold': None,
            'Tier': None
        """

        content_tbody = team_html_table.find('tbody', {'class': 'Content'})
        rows = content_tbody.find_all('tr', {'class': 'Row'})

        team_member_info_list = []

        for row in rows:
            cells = row.find_all('td', {'class': 'Cell'})

            data_dict = {}

            for cell in cells:
                cell_type = cell['class'][0]
                parse_func = getattr(cell_parser, cell_type + '_parser')

                # name, value = parse_func(cell)
                # data_dict[name] = value

                for name, value in zip(*parse_func(cell)):
                    data_dict[name] = value

            team_member_info_list.append(data_dict)

        return team_member_info_list

    def run(self):
        for game_id in self.games:
            game_info_url = self.ingame_info_url_format % (game_id, self.summonerId)
            soup = self.get_response_with_soup(game_info_url)
            print(game_info_url)
            table_wrapper = soup.find('div', {'class': 'GameDetailTableWrap'})

            # Be careful with draw
            winner_table = table_wrapper.find('table', {'class': 'Result-WIN'})
            looser_table = table_wrapper.find('table', {'class': 'Result-LOSE'})

            self.parse_team_info(winner_table)
            self.parse_team_info(looser_table)


if __name__ == '__main__':
    g = GameInfoParser('index0')
    g.run()

    print(1)
