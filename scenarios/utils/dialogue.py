import json
import os

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

PATH = os.path.join(MAIN_DIR, "../../assets/dialogue.json")
with open(PATH, "r") as f:
    lines = json.load(f)

def get_dialogue():
    """
        return the whole json as a dict
    """
    return lines

def get_dialogue_scenario(scenario):

    """
       Method's function is to return
       all the dialogue lines of a given scenario,
       this means get me the 'scenario' branch in the json
    """

    return lines[scenario]

def get_dialogue_subscenario(scenario, subscenario):
    """
       Method's function is to return
       all the dialogue lines of a given subscenario,
       this means get me the 'scenario' branch and then
       the 'subscenario' dict, in the json
    """
    return lines[scenario][subscenario]
