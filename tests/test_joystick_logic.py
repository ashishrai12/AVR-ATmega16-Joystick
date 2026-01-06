"""
Unit tests for joystick direction detection logic.

These tests verify the direction detection algorithm matches
the expected behavior defined in the C implementation.
"""

import pytest
from joystick_logic import JoystickLogic, Direction


class TestJoystickCenterDetection:
    """Tests for center (dead zone) detection."""
    
    def test_exact_center(self, direction_detector):
        """Test exact center position (128, 128)."""
        # Note: 128 is in center zone (70-180 for X, 110-160 for Y)
        result = direction_detector.get_direction(128, 135)
        assert result == Direction.CENTER
    
    def test_center_zone_min_bounds(self, direction_detector):
        """Test minimum bounds of center zone."""
        result = direction_detector.get_direction(70, 110)
        assert result == Direction.CENTER
    
    def test_center_zone_max_bounds(self, direction_detector):
        """Test maximum bounds of center zone."""
        result = direction_detector.get_direction(180, 160)
        assert result == Direction.CENTER
    
    def test_is_centered_true(self, direction_detector):
        """Test is_centered returns True for center positions."""
        assert direction_detector.is_centered(100, 130) is True
        assert direction_detector.is_centered(150, 140) is True
    
    def test_is_centered_false(self, direction_detector):
        """Test is_centered returns False for non-center positions."""
        assert direction_detector.is_centered(0, 0) is False
        assert direction_detector.is_centered(255, 255) is False


class TestCardinalDirections:
    """Tests for cardinal direction (N, S, E, W) detection."""
    
    def test_north_direction(self, direction_detector):
        """Test North direction (high Y, centered X)."""
        # Y >= 240, X in center zone
        result = direction_detector.get_direction(128, 250)
        assert result == Direction.NORTH
    
    def test_south_direction(self, direction_detector):
        """Test South direction (low Y, centered X)."""
        # Y <= 50, X in center zone
        result = direction_detector.get_direction(100, 30)
        assert result == Direction.SOUTH
    
    def test_east_direction(self, direction_detector):
        """Test East direction (high X, centered Y)."""
        # X >= 240, Y in center zone
        result = direction_detector.get_direction(250, 135)
        assert result == Direction.EAST
    
    def test_west_direction(self, direction_detector):
        """Test West direction (low X, centered Y)."""
        # X <= 70, Y in center zone
        result = direction_detector.get_direction(50, 140)
        assert result == Direction.WEST


class TestDiagonalDirections:
    """Tests for diagonal direction (NE, NW, SE, SW) detection."""
    
    def test_north_east_direction(self, direction_detector):
        """Test North-East direction (high X, high Y)."""
        # X > 230, Y > 230
        result = direction_detector.get_direction(250, 250)
        assert result == Direction.NORTH_EAST
    
    def test_north_west_direction(self, direction_detector):
        """Test North-West direction (low X, high Y)."""
        # X < 50, Y > 205 (255 - 50)
        result = direction_detector.get_direction(30, 240)
        assert result == Direction.NORTH_WEST
    
    def test_south_east_direction(self, direction_detector):
        """Test South-East direction (high X, low Y)."""
        # X > 230, Y < 50
        result = direction_detector.get_direction(250, 30)
        assert result == Direction.SOUTH_EAST
    
    def test_south_west_direction(self, direction_detector):
        """Test South-West direction (low X, low Y)."""
        # X < 50, Y < 50
        result = direction_detector.get_direction(20, 20)
        assert result == Direction.SOUTH_WEST


class TestBoundaryConditions:
    """Tests for boundary/edge cases."""
    
    def test_exact_north_threshold(self, direction_detector):
        """Test exact North threshold (Y = 240)."""
        result = direction_detector.get_direction(128, 240)
        assert result == Direction.NORTH
    
    def test_just_below_north_threshold(self, direction_detector):
        """Test just below North threshold (Y = 239)."""
        # Should not be North since Y < 240
        result = direction_detector.get_direction(128, 239)
        assert result != Direction.NORTH
    
    def test_exact_south_threshold(self, direction_detector):
        """Test exact South threshold (Y = 50)."""
        result = direction_detector.get_direction(100, 50)
        assert result == Direction.SOUTH
    
    def test_minimum_values(self, direction_detector):
        """Test minimum ADC values (0, 0)."""
        result = direction_detector.get_direction(0, 0)
        assert result == Direction.SOUTH_WEST
    
    def test_maximum_values(self, direction_detector):
        """Test maximum ADC values (255, 255)."""
        result = direction_detector.get_direction(255, 255)
        assert result == Direction.NORTH_EAST


class TestDirectionToString:
    """Tests for direction to string conversion."""
    
    def test_center_string(self, direction_detector):
        """Test Center direction string."""
        assert direction_detector.direction_to_string(Direction.CENTER) == "C"
    
    def test_cardinal_strings(self, direction_detector):
        """Test cardinal direction strings."""
        assert direction_detector.direction_to_string(Direction.NORTH) == "N"
        assert direction_detector.direction_to_string(Direction.SOUTH) == "S"
        assert direction_detector.direction_to_string(Direction.EAST) == "E"
        assert direction_detector.direction_to_string(Direction.WEST) == "W"
    
    def test_diagonal_strings(self, direction_detector):
        """Test diagonal direction strings."""
        assert direction_detector.direction_to_string(Direction.NORTH_EAST) == "NE"
        assert direction_detector.direction_to_string(Direction.NORTH_WEST) == "NW"
        assert direction_detector.direction_to_string(Direction.SOUTH_EAST) == "SE"
        assert direction_detector.direction_to_string(Direction.SOUTH_WEST) == "SW"


class TestPositionInfo:
    """Tests for get_position_info method."""
    
    def test_position_info_center(self, direction_detector):
        """Test position info for center position."""
        info = direction_detector.get_position_info(128, 135)
        
        assert info["x"] == 128
        assert info["y"] == 135
        assert info["direction"] == Direction.CENTER
        assert info["direction_name"] == "C"
        assert info["is_centered"] is True
        assert 0 <= info["x_percent"] <= 100
        assert 0 <= info["y_percent"] <= 100
    
    def test_position_info_north(self, direction_detector):
        """Test position info for North position."""
        info = direction_detector.get_position_info(128, 250)
        
        assert info["direction"] == Direction.NORTH
        assert info["direction_name"] == "N"
        assert info["is_centered"] is False


class TestADCSimulation:
    """Tests simulating various ADC reading scenarios."""
    
    def test_adc_sweep_x_axis(self, direction_detector):
        """Test direction changes as X sweeps from 0 to 255 with Y centered."""
        y_centered = 135  # In center Y zone
        
        # Low X should be West
        assert direction_detector.get_direction(30, y_centered) == Direction.WEST
        
        # Center X should be Center
        assert direction_detector.get_direction(128, y_centered) == Direction.CENTER
        
        # High X should be East
        assert direction_detector.get_direction(250, y_centered) == Direction.EAST
    
    def test_adc_sweep_y_axis(self, direction_detector):
        """Test direction changes as Y sweeps from 0 to 255 with X centered."""
        x_centered = 128  # In center X zone
        
        # Low Y should be South
        assert direction_detector.get_direction(x_centered, 30) == Direction.SOUTH
        
        # Center Y should be Center
        assert direction_detector.get_direction(x_centered, 135) == Direction.CENTER
        
        # High Y should be North
        assert direction_detector.get_direction(x_centered, 250) == Direction.NORTH
    
    def test_full_rotation(self, direction_detector):
        """Test all 8 directions in a clockwise rotation."""
        # Starting from North, going clockwise
        expected_sequence = [
            ((128, 250), Direction.NORTH),      # N
            ((250, 250), Direction.NORTH_EAST), # NE
            ((250, 135), Direction.EAST),       # E
            ((250, 30), Direction.SOUTH_EAST),  # SE
            ((100, 30), Direction.SOUTH),       # S
            ((20, 20), Direction.SOUTH_WEST),   # SW
            ((50, 140), Direction.WEST),        # W
            ((30, 240), Direction.NORTH_WEST),  # NW
        ]
        
        for (x, y), expected_dir in expected_sequence:
            result = direction_detector.get_direction(x, y)
            assert result == expected_dir, f"Expected {expected_dir} at ({x}, {y}), got {result}"


class TestNoiseAndJitter:
    """Tests for handling noise and jitter in ADC readings."""
    
    def test_center_zone_stability(self, direction_detector):
        """Test that small jitter around center stays centered."""
        center_positions = [
            (125, 130), (130, 135), (128, 140),
            (120, 125), (140, 150), (100, 135),
        ]
        
        for x, y in center_positions:
            result = direction_detector.get_direction(x, y)
            assert result == Direction.CENTER, f"Position ({x}, {y}) should be CENTER"
    
    def test_edge_jitter_handling(self, direction_detector):
        """Test behavior at threshold edges."""
        # Just at North threshold
        assert direction_detector.get_direction(128, 240) == Direction.NORTH
        
        # Several readings near threshold (simulating jitter)
        readings_near_threshold = [239, 240, 241, 240, 238, 242]
        north_count = sum(
            1 for y in readings_near_threshold 
            if direction_detector.get_direction(128, y) == Direction.NORTH
        )
        
        # At least half should register as North
        assert north_count >= len(readings_near_threshold) // 2
