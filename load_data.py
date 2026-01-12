import os
import base64
import json
import pandas as pd
import numpy as np

path = f'my_spotify_data\Spotify Extended Streaming History'
streaming_dict = {}
streaming_history = os.listdir(path)
streaming_list = []

for file in streaming_history[1:]:
    file_path = os.path.join(path, file)
    with open(file_path, encoding = "utf8") as json_file:
        streaming_dict[file] = json.load(json_file)
    streaming_list.extend(streaming_dict[file])

streaming_table = pd.DataFrame(streaming_list)
print(streaming_table.head())

streaming_table.to_csv('streaming_history_full.csv', index = False)