import pygame

class Attack:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown

    def attack_effect(self, attacker, defender):
        # Placeholder for attack effect logic, will be used to apply damage and any additional effects during combat encounters in the future
        defender.health -= defender.percent_impact * self.damage

        #for energy, it will increase with every attack cast by the player (?), building up for a final ultimate full-energy spell
        attacker.energy += self.cooldown * 10  # Example energy cost, can be adjusted as needed
