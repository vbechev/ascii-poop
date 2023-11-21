import os
import sys
import unittest
from unittest.mock import call, patch


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import entities
from entities import Entity
from utils import *


class TestEntity(unittest.TestCase):
    """TODO: Never."""

    def setUp(self):
        """Initialize the entity to be tested."""
        self.entity = Entity('Izaura', 5, 100, (1, 2), "In the kitchen")
        self.target = Entity('Leôncio', 10, 50, (2, 2), "In the bar")

    def test_take_damage(self):
        """Health should be decreased by the number of damage taken when take_damage is called."""
        damage = 10
        expected = self.entity.health - damage
        self.entity.take_damage(damage)
        self.assertEqual(self.entity.health, expected)

    def test_move(self):
        """The entity's position should change according to the movement vector when move is called."""
        movement_vector = (3, 2)
        expected = (self.entity.position[0] + movement_vector[0],
                    self.entity.position[1] + movement_vector[1])
        self.entity.move(movement_vector)
        self.assertEqual(self.entity.position, expected)

    def test_attack_entity_dead(self):
        """UnaliveException should be raised if the target attempts to attack whilst dead."""
        self.entity.health = 0
        with self.assertRaises(UnaliveException):
            self.entity.attack(self.target)

    def test_attack_out_of_range(self):
        """OutOfRangeError should be raised if the target attempts to attack when out of range."""
        self.target.position = (10, 10)
        with self.assertRaises(OutOfRangeError):
            self.entity.attack(self.target)

    def test_attack_successful_hit(self):
        """On a successful hit the target should take damage according to the attack damage.

        The Entity.attack function should return a tuple, consisting of
        (bool: attack_success (True), int: attack_roll, int: damage_roll).
        """
        expected_health = self.target.health - 100
        # Option 1
        with patch('entities.randint', return_value=20):
            self.assertEqual((True, 25, 100), self.entity.attack(self.target))
        self.assertEqual(self.target.health, expected_health)

    def test_attack_failed_hit(self):
        """On a failed hit the target should take no damage.

        The Entity.attack function should return a tuple, consisting of
        (bool: attack_success (False), int: attack_roll, int: damage_roll).
        """
        health_before = self.target.health
        # Option 2
        with patch.object(entities, 'randint', return_value=1):
            self.assertEqual((False, 6, 0), self.entity.attack(self.target))
        self.assertEqual(self.target.health, health_before)

    # With decorators for illustration purposes, don't duplicate tests! :p
    @patch('entities.randint', return_value=20)
    def test_attack_successful_hit_decorator(self, mock_randint):
        """On a successful hit the target should take damage according to the attack damage.

        The Entity.attack function should return a tuple, consisting of
        (bool: attack_success (True), int: attack_roll, int: damage_roll).
        """
        expected_health = self.target.health - 100
        self.assertEqual((True, 25, 100), self.entity.attack(self.target))
        self.assertEqual(self.target.health, expected_health)
        # We can even check the calls
        # One for hit (D20) and 5 for damage (D8), since our player level is 5
        mock_randint.assert_has_calls([call(1, 20)] + [call(1, 8)] * self.entity._level)

    @patch.object(entities, 'randint', return_value=1)
    def test_attack_failed_hit_decorator(self, mock_randint):
        """On a failed hit the target should take no damage.

        The Entity.attack function should return a tuple, consisting of
        (bool: attack_success (False), int: attack_roll, int: damage_roll).
        """
        health_before = self.target.health
        self.assertEqual((False, 6, 0), self.entity.attack(self.target))
        self.assertEqual(self.target.health, health_before)
        # We can even check the calls
        mock_randint.assert_called_once_with(1, 20)


if __name__ == '__main__':
    unittest.main()