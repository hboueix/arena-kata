import math
import random
from enum import Enum
from typing import List

class HeroElement(Enum):
    FIRE = 1
    WATER = 2
    EARTH = 3

class Buff(Enum):
    ATTACK = 1
    DEFENSE = 2

class Hero:
    def __init__(self, element: HeroElement, power, defense, leth, crtr, lp):
        self.element = element
        self.pow = power
        self.defense = defense
        self.leth = leth
        self.crtr = crtr
        self.lp = lp
        self.buffs = list()

class ArenaDamageCalculator:

    def get_best_targets(self, attacker: Hero, defenders: list[Hero]) -> List[Hero]:
        valid_targets = [defender for defender in defenders if defender.lp > 0]
        
        if attacker.element == HeroElement.FIRE:
            best_opponents = [defender for defender in valid_targets if defender.element == HeroElement.EARTH]
            equal_opponents = [defender for defender in valid_targets if defender.element == HeroElement.FIRE]

        elif attacker.element == HeroElement.WATER:
            best_opponents = [defender for defender in valid_targets if defender.element == HeroElement.FIRE]
            equal_opponents = [defender for defender in valid_targets if defender.element == HeroElement.WATER]
            
        elif attacker.element == HeroElement.EARTH:
            best_opponents = [defender for defender in valid_targets if defender.element == HeroElement.WATER]
            equal_opponents = [defender for defender in valid_targets if defender.element == HeroElement.EARTH]
            
        if len(best_opponents) > 0:
            valid_targets = best_opponents
        elif len(equal_opponents) > 0:
            valid_targets = equal_opponents

        return valid_targets

    def compute_damage(self, attacker:Hero, defenders: list[Hero]):
        power = attacker.pow

        adv = list()
        eq = list()
        dis = list()

        attacked = random.choice(self.get_best_targets(attacker, defenders))

        c = random.random() * 100 < attacker.crtr
        dmg = 0
        if c:
            dmg = (attacker.pow + (0.5 + attacker.leth / 5000) * attacker.pow) * (1-attacked.defense /7500)
        else:
            dmg = attacker.pow * (1-attacked.defense / 7500)

        ## BUFFS
        if Buff.ATTACK in attacker.buffs:
            if c:
                dmg += (attacker.pow * 0.25 + (0.5 + attacker.leth / 5000) * attacker.pow * 0.25) * (1-attacked.defense/7500)
            else:
                dmg += attacker.pow * 0.25* (1-attacked.defense/7500)

        if Buff.DEFENSE in attacked.buffs:
            dmg = dmg / (1-attacked.defense/7500) * (1-attacked.defense/7500 -0.25)

        dmg = max(dmg, 0)
        if dmg > 0:
            if attacked in adv:
                dmg = dmg + dmg * 20/100
            elif attacked in eq:
                pass
            else:
                dmg = dmg - dmg *20/100

        dmg = math.floor(dmg)

        if dmg > 0:
            attacked.lp = attacked.lp - dmg
            if attacked.lp < 0:
                attacked.lp = 0

        return defenders