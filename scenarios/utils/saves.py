import json
import os

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

PATH = os.path.join(MAIN_DIR, "../../saves.json")
with open(PATH, "r") as f:
    saves = json.load(f)

SLOT1 = saves["saves"]["slot_1"]
SLOT2 = saves["saves"]["slot_2"]
SLOT3 = saves["saves"]["slot_3"]
STAGES = ("aldea_1",
          "aldea_2",
          "bazar",
          "aldea_3",
          "valle",
          "espacio",
          "ciudad",
          "cuerpo",
          "completado")

def load():
    """
       Method's function is to return
       the three save slots.
    """
    return saves["saves"]

def load_slot(slot):
    """
       Method's function is to return
       the three save slots.
    """
    return saves["saves"][slot]

def first_save(slot, team, food):
    """
       used when initialising an empty save slot,
       team ena expect a boolean, if true uses the pair
       Ena and Cesar, if false goes with Ezer and Diego.
    """
    saves["saves"][slot] = {}
    saves["saves"][slot]["team_ena"] = team
    saves["saves"][slot]["stages"] = {}
    saves["saves"][slot]["last_level_passed"] = {"code": 1, "name": "Casa"}
    saves["saves"][slot]["stages"]["casa"] = True
    for stage in STAGES:
        saves["saves"][slot]["stages"][stage] = False
    saves["saves"][slot]["food"] = food

    with open(PATH, "w") as s:
        json.dump(saves, s)

def save(slot, code, name, stage):
    saves["saves"][slot]["last_level_passed"] = {"code": code, "name": name}
    saves["saves"][slot]["stages"][stage] = True
    with open(PATH, "w") as s:
        json.dump(saves, s)
