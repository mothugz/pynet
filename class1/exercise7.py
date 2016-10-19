import json
import yaml
from pprint import pprint

with open("class1_yaml_dump.yml") as file:
    yaml_list = yaml.load(file)
    pprint(yaml_list)

with open("class1_json_dump.json") as file:
    json_list = json.load(file)
    pprint(json_list)

