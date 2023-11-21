import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from entities import Entity
from utils import *


class TestEntity(unittest.TestCase):

    def setUp(self):
        self.entity = Entity("Isaura", 5, 100, (0, 0), "In the kitchen")
        self.target = Entity("Leôncio", 10, 50, (1, 1), "In the bar")
    
    def test_take_damage(self):
        damage = 20
        expected_health = self.entity.health - damage
        self.entity.take_damage(damage)
        self.assertEqual(self.entity.health, expected_health)
    
    def test_move(self):
        movement_vector = (5, 5)
        expected_position = (self.entity.position[0] + movement_vector[0],
                             self.entity.position[1] + movement_vector[1])
        self.entity.move(movement_vector)
        self.assertEqual(self.entity.position, expected_position)
    
    def test_attack_entity_dead(self):
        self.entity.health = 0 # Unalive the entity
        with self.assertRaises(UnaliveException):
            self.entity.attack(self.target)
    
    def test_attack_entity_far_away(self):
        self.entity.position = (-5, -5) # Move the entity far away
        with self.assertRaises(OutOfRangeError):
            self.entity.attack(self.target)
    
    def test_attack_entity_attack_fails(self):
        with patch('random.randint', return_value=20):
            print(self.entity.attack(self.target))

if __name__ == '__main__':
    unittest.main()