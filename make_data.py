"""
Before use this script, you should make nickname list file.
also, file name is must be "nickname_list.txt"

format like
[nickname_1]
[nickname_2]

Ex)
kcr0ng
lol_zzang
달달한아침햇살
"""

from parsing_data.parser import GameInfoParser

if __name__ == '__main__':
    with open('nickname_list.txt', 'r', encoding='utf8') as f:
        nickname_list = f.read().splitlines()

    for nickname in nickname_list:
        print(f"{nickname} start!")
        g = GameInfoParser(nickname, file='output.csv')
        g.run()

    # Remove duplicate data
    from data_balancer.balancer import set_balance
    set_balance('output.csv')

    from preprocess import process
    process('output.csv')
