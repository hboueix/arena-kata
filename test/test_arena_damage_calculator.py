from typing import Callable

from src.arena_damage_calculator import ArenaDamageCalculator, Buff, Hero, HeroElement


class TestArenaDamageCalculator:

    def setup_method(self, method: Callable) -> None:
        self.calculator = ArenaDamageCalculator()
        self.attackers = [
            Hero(HeroElement.FIRE, 100, 100, 100, 100, 100),
            Hero(HeroElement.WATER, 100, 100, 100, 100, 100),
            Hero(HeroElement.EARTH, 100, 100, 100, 100, 100)
        ]
        self.defenders = [
            Hero(HeroElement.FIRE, 100, 100, 100, 100, 100),
            Hero(HeroElement.WATER, 100, 100, 100, 100, 100),
            Hero(HeroElement.EARTH, 100, 100, 100, 100, 100)
        ]

    def test_compute_damage_return_same_objects(self) -> None:
        updated_defenders = self.calculator.compute_damage(self.attackers[0], self.defenders)

        assert all([self.defenders[i] is updated_defenders[i] for i in range(len(self.defenders))])

    def test_compute_damage_return_updated_attacked_lp(self) -> None:
        self.attackers[0].pow = 50
        self.attackers[0].crtr = 0
        self.defenders[2].defense = 75

        updated_defenders = self.calculator.compute_damage(self.attackers[0], self.defenders)

        assert updated_defenders[2].lp == 41

    def test_compute_damage_return_not_negative_defender_lp(self) -> None:
        self.attackers[0].pow = 1000
        self.attackers[0].crtr = 100
        self.defenders[2].defense = 0

        updated_defenders = self.calculator.compute_damage(self.attackers[0], self.defenders)

        assert updated_defenders[2].lp == 0

    def test_compute_damage_if_turncoat_buff_attacker_retrieve_real_element(self) -> None:
        self.attackers[0].buffs = [Buff.TURNCOAT]

        updated_defenders = self.calculator.compute_damage(self.attackers[0], self.defenders)

        assert self.attackers[0].element == HeroElement.FIRE

    def test_compute_damage_if_turncoat_buff_defender_retreive_real_element(self) -> None:
        self.defenders[2].buffs = [Buff.TURNCOAT]

        updated_defenders = self.calculator.compute_damage(self.attackers[0], self.defenders)

        assert self.defenders[2].element == HeroElement.EARTH

    def test_get_best_targets_if_one_alive(self) -> None:
        self.defenders[0].lp = 0
        self.defenders[1].lp = 0

        targets = self.calculator.get_best_targets(self.attackers[0], self.defenders)

        assert targets == [self.defenders[2]]

    def test_get_best_targets_if_fire_attacker(self) -> None:
        targets = self.calculator.get_best_targets(self.attackers[0], self.defenders)

        assert targets == [self.defenders[2]]

    def test_get_best_targets_if_water_attacker(self) -> None:
        targets = self.calculator.get_best_targets(self.attackers[1], self.defenders)

        assert targets == [self.defenders[0]]

    def test_get_best_targets_if_earth_attacker(self) -> None:
        targets = self.calculator.get_best_targets(self.attackers[2], self.defenders)

        assert targets == [self.defenders[1]]

    def test_best_targets_if_fire_attacker_should_return_fire_defender(self) -> None:
        self.defenders[2].lp = 0

        targets = self.calculator.get_best_targets(self.attackers[0], self.defenders)

        assert targets == [self.defenders[0]]

    def test_best_targets_if_water_attacker_should_return_water_defender(self) -> None:
        self.defenders[0].lp = 0

        targets = self.calculator.get_best_targets(self.attackers[1], self.defenders)

        assert targets == [self.defenders[1]]

    def test_best_targets_if_earth_attacker_should_return_earth_defender(self) -> None:
        self.defenders[1].lp = 0

        targets = self.calculator.get_best_targets(self.attackers[2], self.defenders)

        assert targets == [self.defenders[2]]

    def test_get_best_targets_if_fire_attacker_should_return_water_defender(self) -> None:
        self.defenders[0].lp = 0
        self.defenders[2].element = HeroElement.WATER

        targets = self.calculator.get_best_targets(self.attackers[0], self.defenders)

        assert targets == [self.defenders[1], self.defenders[2]]

    def test_get_best_targets_if_water_attacker_should_return_earth_defender(self) -> None:
        self.defenders[1].lp = 0
        self.defenders[0].element = HeroElement.EARTH

        targets = self.calculator.get_best_targets(self.attackers[1], self.defenders)

        assert targets == [self.defenders[0], self.defenders[2]]

    def test_get_best_targets_if_earth_attacker_should_return_fire_defender(self) -> None:
        self.defenders[2].lp = 0
        self.defenders[1].element = HeroElement.FIRE

        targets = self.calculator.get_best_targets(self.attackers[2], self.defenders)

        assert targets == [self.defenders[0], self.defenders[1]]

    def test_get_best_targets_if_holy_buff_attacker(self) -> None:
        self.attackers[0].buffs = [Buff.HOLY]

        targets = self.calculator.get_best_targets(self.attackers[0], self.defenders)

        assert targets == [self.defenders[0], self.defenders[1], self.defenders[2]]

    def test_get_best_targets_if_fire_attacker_turncoat_buff(self) -> None:
        self.attackers[0].buffs = [Buff.TURNCOAT]

        targets = self.calculator.get_best_targets(self.attackers[0], self.defenders)

        assert targets == [self.defenders[0]]

    def test_get_best_targets_if_water_attacker_turncoat_buff(self) -> None:
        self.attackers[1].buffs = [Buff.TURNCOAT]

        targets = self.calculator.get_best_targets(self.attackers[1], self.defenders)

        assert targets == [self.defenders[1]]

    def test_get_best_targets_if_defender_turncoat_buff(self) -> None:
        self.defenders[2].buffs = [Buff.TURNCOAT]

        targets = self.calculator.get_best_targets(self.attackers[0], self.defenders)

        assert targets == [self.defenders[0], self.defenders[2]]

    def test_get_best_targets_if_earth_attacker_turncoat_buff(self) -> None:
        self.attackers[2].buffs = [Buff.TURNCOAT]

        targets = self.calculator.get_best_targets(self.attackers[2], self.defenders)

        assert targets == [self.defenders[2]]

    def test_get_damage_if_fire_attacker_fire_defender_no_buff_no_crit(self) -> None:
        self.attackers[0].crtr = 0
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[0])

        assert damage == 98

    def test_get_damage_if_fire_attacker_water_defender_no_buff_no_crit(self) -> None:
        self.attackers[0].crtr = 0
        self.defenders[1].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[1])

        assert damage == 78

    def test_get_damage_if_fire_attacker_earth_defender_no_buff_no_crit(self) -> None:
        self.attackers[0].crtr = 0
        self.defenders[2].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[2])

        assert damage == 117

    def test_get_damage_if_water_attacker_fire_defender_no_buff_no_crit(self) -> None:
        self.attackers[1].crtr = 0
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[1], self.defenders[0])

        assert damage == 117

    def test_get_damage_if_water_attacker_water_defender_no_buff_no_crit(self) -> None:
        self.attackers[1].crtr = 0
        self.defenders[1].defense = 150

        damage = self.calculator.get_damage(self.attackers[1], self.defenders[1])

        assert damage == 98

    def test_get_damage_if_water_attacker_earth_defender_no_buff_no_crit(self) -> None:
        self.attackers[1].crtr = 0
        self.defenders[2].defense = 150

        damage = self.calculator.get_damage(self.attackers[1], self.defenders[2])

        assert damage == 78

    def test_get_damage_if_earth_attacker_fire_defender_no_buff_no_crit(self) -> None:
        self.attackers[2].crtr = 0
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[2], self.defenders[0])

        assert damage == 78

    def test_get_damage_if_earth_attacker_water_defender_no_buff_no_crit(self) -> None:
        self.attackers[2].crtr = 0
        self.defenders[1].defense = 150

        damage = self.calculator.get_damage(self.attackers[2], self.defenders[1])

        assert damage == 117

    def test_get_damage_if_earth_attacker_earth_defender_no_buff_no_crit(self) -> None:
        self.attackers[2].crtr = 0
        self.defenders[2].defense = 150

        damage = self.calculator.get_damage(self.attackers[2], self.defenders[2])

        assert damage == 98

    def test_get_damage_if_crit_damage(self) -> None:
        self.attackers[0].crtr = 100
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[0])

        assert damage == 148

    def test_get_damage_if_attack_buff_no_crit(self) -> None:
        self.attackers[0].buffs = [Buff.ATTACK]
        self.attackers[0].crtr = 0
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[0])

        assert damage == 122

    def test_get_damage_if_attack_buff_crit_damage(self) -> None:
        self.attackers[0].buffs = [Buff.ATTACK]
        self.attackers[0].crtr = 100
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[0])

        assert damage == 186

    def test_get_damage_if_defense_buff(self) -> None:
        self.attackers[0].crtr = 0
        self.defenders[0].defense = 150
        self.defenders[0].buffs = [Buff.DEFENSE]

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[0])

        assert damage == 73

    def test_get_damage_if_holy_buff_attacker(self) -> None:
        self.attackers[0].crtr = 0
        self.attackers[0].buffs = [Buff.HOLY]
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[0])

        assert damage == 80

    def test_get_turncoat_element_if_fire(self) -> None:
        assert self.calculator.get_turncoat_element(HeroElement.FIRE) == HeroElement.WATER

    def test_get_turncoat_element_if_water(self) -> None:
        assert self.calculator.get_turncoat_element(HeroElement.WATER) == HeroElement.EARTH

    def test_get_turncoat_element_if_earth(self) -> None:
        assert self.calculator.get_turncoat_element(HeroElement.EARTH) == HeroElement.FIRE
