import json
import random
CoreVersion = "1.0.0"
def BanUser(UserId):
    with open("Data/Bans.json", "r") as f:
        DataBase = json.load(f)
    DataBase["BannedUsers"].append(UserId)
    with open("Data/Bans.json", "w") as r:
        json.dump(DataBase, r)
def UnBanUser(UserId):
    with open("Data/Bans.json", "r") as f:
        DataBase = json.load(f)
    DataBase["BannedUsers"].remove(UserId)
    with open("Data/Bans.json", "w") as r:
        json.dump(DataBase, r)
def IsAdmin(UserId):
    with open("Data/Admins.json", "r") as f:
        DataBase = json.load(f)
    if UserId in DataBase["AdminTable"]:
        return True
    else:
        return False
def GetBannedUsers():
    with open("Data/Bans.json", "r") as f:
        DataBase = json.load(f)
    return DataBase["BannedUsers"]
def AddAdmin(UserId):
    with open("Data/Admins.json", "r") as f:
        DataBase = json.load(f)
    DataBase["AdminTable"].append(UserId)
    with open("Data/Admins.json", "w") as r:
        json.dump(DataBase, r)
def WritePlayerData(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    DataBase[str(UserId)] = {"Balance": 0, "shovel": False}
    with open("Data/DataBase.json", "w") as r:
        json.dump(DataBase, r)
def IsProfileExist(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if not str(UserId) in DataBase:
        return False
    else:
        return True
def BuyShovel(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if IsProfileExist(UserId):
        if DataBase[str(UserId)]["shovel"] != True:
            if DataBase[str(UserId)]["Balance"] >= 30:
                DataBase[str(UserId)]["Balance"] -= 30
                DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"], "shovel": True}
                with open("Data/DataBase.json", "w") as r:
                    json.dump(DataBase, r)
                return 1
            else:
                return 2
        else:
            return 3
    else:
        return 4
def Pay(UserId, TargerId, Value):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if DataBase[str(UserId)]["Balance"] >= Value:
        DataBase[str(UserId)]["Balance"] -= Value
        DataBase[str(TargerId)]["Balance"] += Value
        with open("Data/DataBase.json", "w") as r:
            json.dump(DataBase, r)
        return 1
    else:
        return 2
def GetBalance(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    return DataBase[str(UserId)]["Balance"]
def GetShovelExistEmoji(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if DataBase[str(UserId)]["shovel"] == True:
        return ":white_check_mark:"
    else:
        return ":x:"
def RemoveAdmin(UserId):
    with open("Data/Admins.json", "r") as f:
        DataBase = json.load(f)
    DataBase["AdminTable"].remove(UserId)
    with open("Data/Admins.json", "w") as r:
        json.dump(DataBase, r)
def AddSand(UserId, value):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] + int(value), "shovel": DataBase[str(UserId)]["shovel"]}
    with open("Data/DataBase.json", "w") as r:
        json.dump(DataBase, r)
def RemoveSand(UserId, value):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] -  int(value), "shovel": DataBase[str(UserId)]["shovel"]}
    with open("Data/DataBase.json", "w") as r:
        json.dump(DataBase, r)
def DigSand(UserId):
    value = 0
    BannedIds = GetBannedUsers()
    if not UserId in BannedIds:
        with open("Data/DataBase.json", "r") as f:
            DataBase = json.load(f)
        if DataBase[str(UserId)]["shovel"] == True:
            value = random.randint(4, 10)
        else:
            value = random.randint(1, 4)
        DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] + value, "shovel": DataBase[str(UserId)]["shovel"]}
        with open("Data/DataBase.json", "w") as r:
            json.dump(DataBase, r)
    return value