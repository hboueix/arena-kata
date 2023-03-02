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
    HOLY = 3

class Hero:
    def __init__(self, element: HeroElement, power: int, defense: int, leth: int, crtr: int, lp: int) -> None:
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

        if Buff.HOLY in attacker.buffs:
            return valid_targets
        
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
    
    def get_damage(self, attacker: Hero, attacked: Hero) -> int:
        add_crit_damage = random.random() * 100 < attacker.crtr
        if add_crit_damage:
            damage = (attacker.pow + (0.5 + attacker.leth / 5000) * attacker.pow) * (1 - attacked.defense / 7500)
        else:
            damage = attacker.pow * (1 - attacked.defense / 7500)

        if Buff.ATTACK in attacker.buffs:
            if add_crit_damage:
                damage += (attacker.pow * 0.25 + (0.5 + attacker.leth / 5000) * attacker.pow * 0.25) * (1 - attacked.defense / 7500)
            else:
                damage += attacker.pow * 0.25 * (1 - attacked.defense / 7500)

        if Buff.DEFENSE in attacked.buffs:
            damage /= (1 - attacked.defense / 7500)
            damage *= (1 - attacked.defense / 7500 - 0.25)

        if attacker.element == HeroElement.FIRE:
            if attacked.element == HeroElement.WATER:
                damage *= 0.8
            elif attacked.element == HeroElement.EARTH:
                damage *= 1.2
        elif attacker.element == HeroElement.WATER:
            if attacked.element == HeroElement.EARTH:
                damage *= 0.8
            elif attacked.element == HeroElement.FIRE:
                damage *= 1.2
        elif attacker.element == HeroElement.EARTH:
            if attacked.element == HeroElement.FIRE:
                damage *= 0.8
            elif attacked.element == HeroElement.WATER:
                damage *= 1.2

        return math.floor(damage)

    def compute_damage(self, attacker:Hero, defenders: list[Hero]):
        attacked = random.choice(self.get_best_targets(attacker, defenders))

        damage = self.get_damage(attacker, attacked)

        if damage > 0:
            attacked.lp -= damage
            if attacked.lp < 0:
                attacked.lp = 0

        return defenders