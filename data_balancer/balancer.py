import os

import pandas as pd


# Pasta!

def set_balance(input_file):
    csv_obj = pd.read_csv(input_file)

    for i in csv_obj.index:
        find_value = list(csv_obj.ix[i][['game_id', 'summoner_name']].values)

        if [list(tmp_data) for tmp_data in csv_obj[['game_id', 'summoner_name']].values].count(find_value) > 1:
            csv_obj.ix[i] = None

    csv_obj.to_csv(input_file, encoding='utf8', index=False)

    # Remove None Row

    output_f = open('tmp.csv', 'w', encoding='utf8')

    with open(input_file, encoding='utf8') as f:
        output_f.write(f.readline())  # Skip check CSV header
        lines = f.readlines()
        for line in lines:
            if 'game_id' in line or ',,,,' in line:  # DUP HEADER or None DATA
                continue
            else:
                output_f.write(line)

    os.remove(input_file)
    os.rename('tmp.csv', input_file)
