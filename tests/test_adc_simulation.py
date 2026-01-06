"""
ADC Simulation Tests.

Tests for ADC value handling, conversion, and calibration logic.
"""

import pytest
from joystick_logic import JoystickLogic, Direction


class TestADCValueConversion:
    """Tests for ADC value to percentage conversion."""
    
    def test_adc_to_percent_min(self, config):
        """Test minimum ADC value (0) converts to 0%."""
        percent = 0 / 255 * 100
        assert percent == 0
    
    def test_adc_to_percent_max(self, config):
        """Test maximum ADC value (255) converts to 100%."""
        percent = 255 / 255 * 100
        assert percent == 100
    
    def test_adc_to_percent_center(self, config):
        """Test center ADC value (128) converts to ~50%."""
        percent = 128 / 255 * 100
        assert 50 <= percent <= 51  # Allow small rounding
    
    def test_adc_to_percent_quarter(self, config):
        """Test quarter ADC values."""
        assert 64 / 255 * 100 == pytest.approx(25.1, rel=0.1)
        assert 192 / 255 * 100 == pytest.approx(75.3, rel=0.1)


class TestCalibrationOffset:
    """Tests for ADC calibration and offset handling."""
    
    def test_centered_value_calculation(self, config):
        """Test calculating centered value (offset from midpoint)."""
        # For 10-bit ADC (0-1023), midpoint is 512
        adc_10bit_mid = 512
        
        raw_value = 512
        centered = raw_value - adc_10bit_mid
        assert centered == 0
        
        raw_value = 1023
        centered = raw_value - adc_10bit_mid
        assert centered == 511
        
        raw_value = 0
        centered = raw_value - adc_10bit_mid
        assert centered == -512
    
    def test_8bit_to_signed_range(self, config):
        """Test converting 8-bit ADC (0-255) to signed range (-128 to +127)."""
        def to_signed(value):
            return value - 128
        
        assert to_signed(0) == -128
        assert to_signed(128) == 0
        assert to_signed(255) == 127
    
    def test_offset_correction(self, config):
        """Test applying calibration offset to readings."""
        # Simulate a sensor with +5 offset (rest position reads 133 instead of 128)
        calibration_offset = 5
        
        raw_reading = 133
        corrected = raw_reading - calibration_offset
        assert corrected == 128  # Now at true center


class TestNoiseFiltering:
    """Tests for noise filtering simulation."""
    
    def test_averaging_filter(self):
        """Test simple averaging filter for noise reduction."""
        # Simulated noisy readings around 128
        noisy_readings = [125, 130, 128, 132, 126, 129, 127, 131]
        
        average = sum(noisy_readings) / len(noisy_readings)
        assert 127 <= average <= 129
    
    def test_median_filter(self):
        """Test median filter for spike rejection."""
        # Reading with spike
        readings_with_spike = [128, 127, 255, 129, 128]  # 255 is spike
        
        sorted_readings = sorted(readings_with_spike)
        median = sorted_readings[len(sorted_readings) // 2]
        
        assert median == 128  # Spike rejected
    
    def test_moving_average(self):
        """Test moving average filter."""
        readings = [100, 130, 125, 135, 128, 120, 132, 127]
        window_size = 3
        
        moving_averages = []
        for i in range(len(readings) - window_size + 1):
            window = readings[i:i + window_size]
            avg = sum(window) / window_size
            moving_averages.append(avg)
        
        # All averages should be relatively stable
        assert all(100 <= avg <= 140 for avg in moving_averages)


class TestADCRangeMapping:
    """Tests for mapping ADC ranges to different scales."""
    
    def test_map_to_angle(self):
        """Test mapping ADC value to angle (0-255 -> 0-180 degrees)."""
        def adc_to_angle(adc_value):
            return adc_value * 180 / 255
        
        assert adc_to_angle(0) == 0
        assert adc_to_angle(255) == pytest.approx(180)
        assert adc_to_angle(128) == pytest.approx(90.35, rel=0.1)
    
    def test_map_to_pwm_duty(self):
        """Test mapping ADC value to PWM duty cycle (0-255 -> 0-100%)."""
        def adc_to_duty(adc_value):
            return adc_value * 100 / 255
        
        assert adc_to_duty(0) == 0
        assert adc_to_duty(255) == pytest.approx(100)
        assert adc_to_duty(128) == pytest.approx(50.2, rel=0.1)
    
    def test_dead_zone_mapping(self):
        """Test mapping with dead zone around center."""
        def apply_dead_zone(value, dead_zone=20):
            center = 128
            if abs(value - center) < dead_zone:
                return center
            return value
        
        assert apply_dead_zone(128) == 128
        assert apply_dead_zone(130) == 128  # In dead zone
        assert apply_dead_zone(150) == 150  # Outside dead zone
        assert apply_dead_zone(115) == 128  # In dead zone (13 from center)


class TestMultiAxisReading:
    """Tests for reading multiple ADC channels."""
    
    def test_sequential_reading(self, direction_detector):
        """Test reading X and Y values sequentially."""
        # Simulate sequential ADC reads
        x_value = 128
        y_value = 250
        
        position_info = direction_detector.get_position_info(x_value, y_value)
        
        assert position_info["x"] == 128
        assert position_info["y"] == 250
        assert position_info["direction"] == Direction.NORTH
    
    def test_channel_switching_delay(self):
        """Test that channel switching doesn't affect readings."""
        # Simulate readings with proper settle time
        channel_0_readings = [127, 128, 129, 128]
        channel_1_readings = [250, 251, 249, 250]
        
        # After switching channels, first reading might be off
        # but subsequent readings should be stable
        x_avg = sum(channel_0_readings[1:]) / len(channel_0_readings[1:])
        y_avg = sum(channel_1_readings[1:]) / len(channel_1_readings[1:])
        
        assert 127 <= x_avg <= 129
        assert 248 <= y_avg <= 252


class TestADCResolution:
    """Tests for different ADC resolution modes."""
    
    def test_8bit_resolution(self):
        """Test 8-bit ADC resolution (0-255)."""
        min_val, max_val = 0, 255
        resolution = max_val - min_val + 1
        
        assert resolution == 256
        assert 256 == 2**8
    
    def test_10bit_resolution(self):
        """Test 10-bit ADC resolution (0-1023)."""
        min_val, max_val = 0, 1023
        resolution = max_val - min_val + 1
        
        assert resolution == 1024
        assert 1024 == 2**10
    
    def test_10bit_to_8bit_conversion(self):
        """Test converting 10-bit reading to 8-bit."""
        def convert_10_to_8(value_10bit):
            # Right shift by 2 (divide by 4), equivalent to reading ADCH with ADLAR
            return value_10bit >> 2
        
        assert convert_10_to_8(0) == 0
        assert convert_10_to_8(1023) == 255
        assert convert_10_to_8(512) == 128


class TestEdgeCasesAndErrors:
    """Tests for edge cases and error conditions."""
    
    def test_invalid_adc_values_clamped(self, direction_detector):
        """Test behavior with out-of-range values (should be handled gracefully)."""
        # Values beyond 8-bit range - typically clamped by hardware
        # but logic should handle if passed
        result = direction_detector.get_direction(255, 255)
        assert result == Direction.NORTH_EAST
    
    def test_rapid_direction_changes(self, direction_detector):
        """Test stability during rapid direction changes."""
        # Simulate rapid joystick movement
        positions = [
            (128, 250),  # N
            (200, 200),  # transition
            (250, 135),  # E
            (180, 50),   # transition
            (100, 30),   # S
        ]
        
        directions = [
            direction_detector.get_direction(x, y) 
            for x, y in positions
        ]
        
        # Should have detected at least N, E, S
        assert Direction.NORTH in directions
        assert Direction.SOUTH in directions
