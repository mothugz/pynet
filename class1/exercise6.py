import json
import yaml

randomWordList = [ "brake", "depressed", "frightened", "rabbits", "lovely",
                   {"word1": "juice", "word2": "workable"} ]

with open ("class1_yaml_dump.yml", "w") as file:
   file.write(yaml.dump(randomWordList, default_flow_style=False))

with open ("class1_json_dump.json", "w") as file:
   json.dump(randomWordList, file)

