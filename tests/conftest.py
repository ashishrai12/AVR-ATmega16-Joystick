"""
Pytest configuration for AVR-ATmega16-Joystick test suite.

This module provides fixtures and configuration for testing the
joystick direction detection logic on a PC (without hardware).
"""

import pytest
import sys
import os

# Add the tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# Threshold constants matching config.h
class JoystickConfig:
    """Configuration matching the C header file config.h"""
    
    # ADC range (8-bit)
    ADC_MIN = 0
    ADC_MAX = 255
    ADC_CENTER = 128
    
    # Cardinal direction thresholds
    THRESHOLD_NORTH_Y = 240
    THRESHOLD_SOUTH_Y = 50
    THRESHOLD_EAST_X = 240
    THRESHOLD_WEST_X = 70
    
    # Center zone boundaries
    CENTER_X_MIN = 70
    CENTER_X_MAX = 180
    CENTER_Y_MIN = 110
    CENTER_Y_MAX = 160
    
    # Diagonal thresholds
    DIAGONAL_THRESHOLD_HIGH = 230
    DIAGONAL_THRESHOLD_LOW = 50


@pytest.fixture
def config():
    """Provide joystick configuration for tests."""
    return JoystickConfig()


@pytest.fixture
def direction_detector(config):
    """Provide a direction detection function matching C implementation."""
    from joystick_logic import JoystickLogic
    return JoystickLogic(config)
