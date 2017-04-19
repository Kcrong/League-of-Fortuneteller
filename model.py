import pandas as pd

from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

train_data = pd.read_csv('./output_train_format.csv', delimiter=',')


x = train_data[train_data.keys()[:-1]].values
y = train_data['result'].values

result_encoder = LabelEncoder()
result_encoder.fit(y)
y = result_encoder.transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = Sequential([
    Dense(64, input_dim=x.shape[1]),
    Activation('relu'),
    Dense(1),
    Activation('sigmoid')
])

model.compile(
    optimizer=SGD(lr=1e-4),
    loss='binary_crossentropy',
    metrics=['acc']
)


model.fit(x_train, y_train)

"""
    ['champion_name', 'level', 'spell_1', 'spell_2', 'mastery',
       'summoner_name', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5',
       'item6', 'KDARatio', 'Kill', 'Death', 'Assist', 'CKRate',
       'ChampionDamage', 'bought_pink_ward', 'installed_ward', 'removed_ward',
       'total_cs', 'cs_per_minute', 'gold', 'tier', 'game_id', 'result']

"""

"""
# Make integer Label for string data

def get_columns_list(column_list):
    total = []
    for column in column_list:
        total += list(train_data[column].values)
    return total


def transform_train_data(encoder, column_data):
    if isinstance(column_data, list):
        for column_name in column_data:
            train_data[column_name] = encoder.transform(train_data[column_name])
    elif isinstance(column_data, str):
        train_data[column_data] = encoder.transform(train_data[column_data])
    else:
        raise TypeError("Wrong Type instance!!!")

champion_encoder = LabelEncoder()
champion_encoder.fit(train_data['champion_name'])
# Replace string data to integer
transform_train_data(champion_encoder, 'champion_name')

spell_encoder = LabelEncoder()
spell_encoder.fit(get_columns_list(['spell_1', 'spell_2']))
# Replace
transform_train_data(spell_encoder, ['spell_1', 'spell_2'])

mastery_encoder = LabelEncoder()
mastery_encoder.fit(train_data['mastery'])
# Replace
transform_train_data(mastery_encoder, 'mastery')

item_encoder = LabelEncoder()
item_encoder.fit(get_columns_list(['item0', 'item1', 'item2', 'item3', 'item4', 'item5']))
# Replace
transform_train_data(item_encoder, ['item0', 'item1', 'item2', 'item3', 'item4', 'item5'])

trinket_encoder = LabelEncoder()
trinket_encoder.fit(get_columns_list(['item6']))
# Replace
transform_train_data(trinket_encoder, 'item6')

tier_encoder = LabelEncoder()
tier_encoder.fit(get_columns_list(['tier']))
# Replace
transform_train_data(tier_encoder, 'tier')
"""