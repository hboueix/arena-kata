from src.arena_damage_calculator import ArenaDamageCalculator, Hero, HeroElement


class TestArenaDamageCalculator:

    def setup_method(self, method):
        self.calculator = ArenaDamageCalculator()

    def test_compute_damage_return_same_objects(self):
        attackers = [
            Hero(HeroElement.FIRE, 100, 100, 100, 100, 100),
            Hero(HeroElement.WATER, 100, 100, 100, 100, 100),
            Hero(HeroElement.EARTH, 100, 100, 100, 100, 100)
        ]
        defenders = [
            Hero(HeroElement.FIRE, 100, 100, 100, 100, 100),
            Hero(HeroElement.WATER, 100, 100, 100, 100, 100),
            Hero(HeroElement.EARTH, 100, 100, 100, 100, 100)
        ]

        updated_defenders = self.calculator.compute_damage(attackers[0], defenders)

        assert all([defenders[i] is updated_defenders[i] for i in range(len(defenders))])

    def test_get_best_target_if_one_alive(self):
        attackers = [
            Hero(HeroElement.FIRE, 100, 100, 100, 100, 100)
        ]
        defenders = [
            Hero(HeroElement.FIRE, 100, 100, 100, 100, lp=0),
            Hero(HeroElement.WATER, 100, 100, 100, 100, lp=0),
            Hero(HeroElement.EARTH, 100, 100, 100, 100, lp=100)
        ]

        target = self.calculator.get_best_target(attackers[0], defenders)

        assert target is defenders[2]
