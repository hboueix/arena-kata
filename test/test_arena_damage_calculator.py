from typing import Callable

from src.arena_damage_calculator import ArenaDamageCalculator, Hero, HeroElement


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

    def test_get_damage_if_fire_attacker_fire_defender_no_buff_no_crit(self) -> None:
        self.attackers[0].crtr = 0
        self.defenders[0].defense = 150

        damage = self.calculator.get_damage(self.attackers[0], self.defenders[0])

        assert damage == 98
