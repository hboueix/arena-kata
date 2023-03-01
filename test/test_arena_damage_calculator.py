from src.arena_damage_calculator import ArenaDamageCalculator, Hero, HeroElement


class TestArenaDamageCalculator:

    def setup_method(self, method):
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

    def test_compute_damage_return_same_objects(self):
        updated_defenders = self.calculator.compute_damage(self.attackers[0], self.defenders)

        assert all([self.defenders[i] is updated_defenders[i] for i in range(len(self.defenders))])

    def test_get_best_target_if_one_alive(self):
        self.defenders[0].lp = 0
        self.defenders[1].lp = 0

        target = self.calculator.get_best_target(self.attackers[0], self.defenders)

        assert target is self.defenders[2]

    def test_get_best_target_if_fire_attacker(self):
        target = self.calculator.get_best_target(self.attackers[0], self.defenders)

        assert target is self.defenders[2]
