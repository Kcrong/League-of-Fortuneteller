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
