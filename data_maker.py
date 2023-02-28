import json

a = [[False, True, True, False, False, False, False, False, False], [False, True, False, False, False, True, False, False, False], [False, False, False, False, False, False, False, False, False], [False, True, False, False, True, False, False, False, False], [False, False, True, False, False, False, False, False, False], [False, False, False, True, True, False, False, False, False], [False, False, False, False, True, False, False, False, False]]
data = {"board": a}

with open("/mnt/insa/lkusno/Home_INSA/Informatique/Algo/A2/Search/data.json", "w") as f:
    json.dump(data, f)