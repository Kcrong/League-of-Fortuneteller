import re

from bs4 import BeautifulSoup


def ChampionImage_parser(data):
    champion = data.find('div', {'class': 'Image'}).text
    level = int(data.find('div', {'class': 'Level'}).text)

    return ['champion_name', 'level'], [champion, level]


def SummonerSpell_parser(data):
    spell_list = [BeautifulSoup(img_tag['title'], 'lxml').find('b').text for img_tag in data.find_all('img')]

    return ['spell_1', 'spell_2'], spell_list


def KeystoneMastery_parser(data):
    try:
        mastery = BeautifulSoup(data.find('img')['title'], 'lxml').find('b').text
    except KeyError:
        # No mastery
        mastery = 'noMastery'

    return ['mastery'], [mastery]


def SummonerName_parser(data):
    summoner_name = data.find('a').text

    return ['summoner_name'], [summoner_name]


def Items_parser(data):
    item_list = []

    for item in data.find_all('div', {'class': 'Item'}):
        try:
            item_name = item.find('img')['alt']
        except TypeError:
            item_name = 'noItem'
        item_list.append(item_name)

    return ['item%d' % i for i in range(len(item_list))], item_list


def KDA_parser(data):
    name_list = []
    value_list = []

    for info in data.find_all('span'):
        name_list.append(info['class'][0])
        try:
            data = int(info.text)
        except ValueError:
            data = info.text

        value_list.append(data)

    return name_list, value_list


def Damage_parser(data):
    damage = int(data.find('div', {'class': 'ChampionDamage'}).text.replace(',', ''))

    return ['ChampionDamage'], [damage]


def Ward_parser(data):
    bought_pink_ward = int(data.find('span', {'class': 'SightWard'}).text)
    installed_ward, removed_ward = (span_tag.text for span_tag in data.find('div', {'class': 'Stats'}).find_all('span'))

    return ['bought_pink_ward', 'installed_ward', 'removed_ward'], \
           [bought_pink_ward, int(installed_ward), int(removed_ward)]


def CS_parser(data):
    total_cs = int(data.find('div', {'class': 'CS'}).text)
    cs_per_minute = int(re.findall('\d+', data.find('div', {'class': 'CSPerMinute'}).text)[0])

    return ['total_cs', 'cs_per_minute'], [total_cs, cs_per_minute]


def Gold_parser(data):
    gold_str = data.text

    assert 'k' in gold_str
    gold = int(re.findall('\d+', gold_str)[0]) * 1000

    return ['gold'], [gold]


def Tier_parser(data):
    return ['tier'], [data.text.strip()]
