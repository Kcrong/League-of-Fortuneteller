import csv
from random import choice

import os

from collections import defaultdict

import pandas as pd

# Pre-processing with features
import re

TEAM_LIST = ['red_', 'blue_']


def process(csv_name, output_name):
    train_data = pd.read_csv(csv_name, delimiter=',')

    changed_data_dict = defaultdict(dict)

    # CKRate (percentage) to integer
    train_data['CKRate'] = [int(re.findall('\d+', rate)[0]) for rate in train_data['CKRate']]

    # Make team data using each user's data

    def save_new_features_for_team(team_data):
        def transform_tier_to_integer(tier):
            if 'Level' in tier:
                return int(tier.split()[1])
            elif 'Master' in tier:
                return 25 + 30
            elif 'Challenger' in tier:
                return 30 + 30
            elif 'Unranked' in tier:
                return 30
            else:
                tier_dict = {
                    'Bronze': 0,
                    'Silver': 5,
                    'Gold': 10,
                    'Platinum': 15,
                    'Diamond': 20,
                }
                name, level = tier.split()

                return (tier_dict[name] + (5 - int(level))) + 30

        game_dict = changed_data_dict[team_data['game_id'].values[0]]

        if not game_dict:
            team_type = choice(TEAM_LIST)
        else:
            team_type = {
                'blue': 'red_',
                'red': 'blue_'
            }[next(iter(game_dict.keys())).split('_')[0]]

        game_dict[team_type + 'team_level'] = team_data['level'].sum()
        game_dict[team_type + 'team_kill'] = team_data['Kill'].sum()
        game_dict[team_type + 'team_death'] = team_data['Death'].sum()
        game_dict[team_type + 'team_assist'] = team_data['Assist'].sum()
        game_dict[team_type + 'team_ckrate'] = team_data['CKRate'].sum()
        game_dict[team_type + 'team_damage'] = team_data['ChampionDamage'].sum()
        game_dict[team_type + 'team_bought_pink_ward'] = team_data['bought_pink_ward'].sum()
        game_dict[team_type + 'team_installed_ward'] = team_data['installed_ward'].sum()
        game_dict[team_type + 'team_removed_ward'] = team_data['removed_ward'].sum()
        game_dict[team_type + 'team_cs'] = team_data['total_cs'].sum()
        game_dict[team_type + 'team_cs_per_minute'] = team_data['cs_per_minute'].mean()
        game_dict[team_type + 'team_gold'] = team_data['gold'].sum()
        game_dict[team_type + 'team_tier'] = team_data['tier'].apply(transform_tier_to_integer).sum()

        if (team_data['result'] == 1).all():  # if this team win
            game_dict['result'] = team_type

    # Grouping by each games
    train_data.groupby(['game_id', 'result']).apply(save_new_features_for_team)

    writer = csv.DictWriter(open(output_name, 'w', encoding='utf8'),
                            next(iter(changed_data_dict.values())).keys())
    writer.writeheader()
    writer.writerows(changed_data_dict.values())
