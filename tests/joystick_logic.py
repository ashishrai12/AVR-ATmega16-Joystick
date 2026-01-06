"""
Joystick Logic Module - Python implementation for testing.

This module mirrors the C joystick.c logic for PC-side testing.
"""

from enum import IntEnum
from typing import Tuple


class Direction(IntEnum):
    """Joystick direction enumeration matching C implementation."""
    CENTER = 0
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    NORTH_EAST = 5
    NORTH_WEST = 6
    SOUTH_EAST = 7
    SOUTH_WEST = 8


class JoystickLogic:
    """
    Joystick direction detection logic.
    
    This class implements the same algorithm as joystick.c for
    detecting direction from X/Y ADC values.
    """
    
    DIRECTION_NAMES = {
        Direction.CENTER: "C",
        Direction.NORTH: "N",
        Direction.SOUTH: "S",
        Direction.EAST: "E",
        Direction.WEST: "W",
        Direction.NORTH_EAST: "NE",
        Direction.NORTH_WEST: "NW",
        Direction.SOUTH_EAST: "SE",
        Direction.SOUTH_WEST: "SW",
    }
    
    def __init__(self, config):
        """
        Initialize with configuration matching config.h.
        
        Args:
            config: Configuration object with threshold values
        """
        self.config = config
    
    def is_centered(self, x: int, y: int) -> bool:
        """
        Check if position is in center (dead) zone.
        
        Args:
            x: X-axis value (0-255)
            y: Y-axis value (0-255)
            
        Returns:
            True if in center zone
        """
        return (self.config.CENTER_X_MIN <= x <= self.config.CENTER_X_MAX and
                self.config.CENTER_Y_MIN <= y <= self.config.CENTER_Y_MAX)
    
    def get_direction(self, x: int, y: int) -> Direction:
        """
        Determine direction from X/Y values.
        
        Uses threshold-based zone detection matching the C implementation.
        
        Args:
            x: X-axis value (0-255)
            y: Y-axis value (0-255)
            
        Returns:
            Detected direction
        """
        # Check center zone first
        if self.is_centered(x, y):
            return Direction.CENTER
        
        # Check diagonal directions (corners)
        # North-East: high X, high Y
        if (x > self.config.DIAGONAL_THRESHOLD_HIGH and 
            y > self.config.DIAGONAL_THRESHOLD_HIGH):
            return Direction.NORTH_EAST
        
        # North-West: low X, high Y
        if (x < self.config.DIAGONAL_THRESHOLD_LOW and 
            y > (self.config.ADC_MAX - self.config.DIAGONAL_THRESHOLD_LOW)):
            return Direction.NORTH_WEST
        
        # South-East: high X, low Y
        if (x > self.config.DIAGONAL_THRESHOLD_HIGH and 
            y < self.config.DIAGONAL_THRESHOLD_LOW):
            return Direction.SOUTH_EAST
        
        # South-West: low X, low Y
        if (x < self.config.DIAGONAL_THRESHOLD_LOW and 
            y < self.config.DIAGONAL_THRESHOLD_LOW):
            return Direction.SOUTH_WEST
        
        # Check cardinal directions
        # North: high Y, X near center
        if (y >= self.config.THRESHOLD_NORTH_Y and 
            self.config.CENTER_X_MIN <= x <= self.config.CENTER_X_MAX):
            return Direction.NORTH
        
        # South: low Y, X near center
        if (y <= self.config.THRESHOLD_SOUTH_Y and 
            self.config.CENTER_X_MIN <= x <= self.config.CENTER_X_MAX):
            return Direction.SOUTH
        
        # East: high X, Y near center
        if (x >= self.config.THRESHOLD_EAST_X and 
            self.config.CENTER_Y_MIN <= y <= self.config.CENTER_X_MAX):
            return Direction.EAST
        
        # West: low X, Y near center
        if (x <= self.config.THRESHOLD_WEST_X and 
            self.config.CENTER_Y_MIN <= y <= self.config.CENTER_X_MAX):
            return Direction.WEST
        
        # Default to center if no direction matched
        return Direction.CENTER
    
    def direction_to_string(self, direction: Direction) -> str:
        """
        Convert direction enum to string.
        
        Args:
            direction: Direction enumeration value
            
        Returns:
            Human-readable direction string
        """
        return self.DIRECTION_NAMES.get(direction, "?")
    
    def get_position_info(self, x: int, y: int) -> dict:
        """
        Get comprehensive position information.
        
        Args:
            x: X-axis value (0-255)
            y: Y-axis value (0-255)
            
        Returns:
            Dictionary with position details
        """
        direction = self.get_direction(x, y)
        return {
            "x": x,
            "y": y,
            "x_percent": round(x / 255 * 100, 1),
            "y_percent": round(y / 255 * 100, 1),
            "direction": direction,
            "direction_name": self.direction_to_string(direction),
            "is_centered": self.is_centered(x, y),
        }
