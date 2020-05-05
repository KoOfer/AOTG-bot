import os
import sys
import pickle
import json


MinionSlotsList = [0, 5, 15, 30, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 450, 500, 550]
SkillXPList = [0, 50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425, 97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425, 4722425, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425, 17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425, 38072425, 40972425, 44072425, 47472425, 51172425, 55172425]
players = {}
profiles = {}

class Player:
    def __init__(self,*, IGN, kwnIGNs, JoinDate, ProfileIDs, LastLogin, Rank, TaxTotal = 0, Req = False):
        self.IGNs = kwnIGNs
        self.IGN = IGN
        self.joinDate = JoinDate
        self.profiles = ProfileIDs
        self.taxTotal = TaxTotal
        self.taxLog = []
        self.meetsReq = Req
        self.lastLogin = LastLogin
        self.rank = Rank
        self.taxDue = JoinDate

    def __repr__(self):
        return f'IGNs: {self.IGNs}\nJoin Date: {self.joinDate}\nProfiles: {self.profiles}\nTax Total: {self.taxTotal}\nReq: {self.meetsReq}\n\n'
    
class Profile:
    def __init__(self, n_members):
        self.minionSlots = 0
        self.members = {}

    def update(self, parsed):
        self.minionSlots = self.unique2slots(parsed["unique"], MinionSlotsList)
        for uuid in parsed["member"]:
            if uuid not in self.members: self.members[uuid] = {}
            if "skills" not in self.members[uuid]: self.members[uuid]["skills"] = {}
            for skill in parsed["member"][uuid]["skills"]:
                self.members[uuid]["skills"][skill] = self.xp2lvl(parsed["member"][uuid]["skills"][skill], SkillXPList)
            if "slayers" not in self.members[uuid]: self.members[uuid]["slayers"] = {}
            for slayer in parsed["member"][uuid]["slayer"]:
                self.members[uuid]["slayers"][slayer] = parsed["member"][uuid]["slayer"][slayer]

    def unique2slots(self, uniques, slotlist):
        return 4 + self.xp2lvl(uniques, slotlist)

    def xp2lvl(self, xp,xplist):                
        for i in range(len(xplist)):      
            if xp<=xplist[i]: return i 
        return len(xplist)

def save_data():
    with open("data.pkl", 'wb') as f:
        pickle.dump(players, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(profiles, f, pickle.HIGHEST_PROTOCOL)

def load_data():
    global MinionSlotsList, SkillXPList, players, profiles
    MinionSlotsList = [0, 5, 15, 30, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 450, 500, 550]
    SkillXPList = [0, 50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425, 97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425, 4722425, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425, 17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425, 38072425, 40972425, 44072425, 47472425, 51172425, 55172425]
    players = {}
    profiles = {}
    if os.path.exists("data.pkl"):
        with open("data.pkl", 'rb') as f:
            players = pickle.load(f)
            profiles = pickle.load(f)

def load_config():
    global config
    with open("config.json",'r') as f:
        config = json.load(f)

def save_config(config_data):
    with open("config.json", 'w') as f:
        json.dump(config_data, f)