from src.arena_damage_calculator import ArenaDamageCalculator, Hero, HeroElement


class TestArenaDamageCalculator:

    def setup_method(self, method):
        self.calculator = ArenaDamageCalculator()

    def test_compute_damage(self):
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
