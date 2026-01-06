"""
Interactive Joystick Visualizer.

Provides an interactive visualization of joystick position and direction
detection. Useful for understanding the detection algorithm.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider
import numpy as np
from pathlib import Path


class JoystickVisualizer:
    """
    Interactive joystick position visualizer.
    
    Displays joystick position in real-time with direction detection
    zones overlay.
    """
    
    # Configuration matching config.h
    ADC_MIN = 0
    ADC_MAX = 255
    
    THRESHOLD_NORTH_Y = 240
    THRESHOLD_SOUTH_Y = 50
    THRESHOLD_EAST_X = 240
    THRESHOLD_WEST_X = 70
    
    CENTER_X_MIN = 70
    CENTER_X_MAX = 180
    CENTER_Y_MIN = 110
    CENTER_Y_MAX = 160
    
    DIAGONAL_THRESHOLD_HIGH = 230
    DIAGONAL_THRESHOLD_LOW = 50
    
    DIRECTIONS = [
        'CENTER', 'NORTH', 'SOUTH', 'EAST', 'WEST',
        'NORTH_EAST', 'NORTH_WEST', 'SOUTH_EAST', 'SOUTH_WEST'
    ]
    
    def __init__(self):
        """Initialize the visualizer."""
        self.fig = None
        self.ax = None
        self.position_marker = None
        self.direction_text = None
        self.x_slider = None
        self.y_slider = None
    
    def get_direction(self, x: int, y: int) -> str:
        """
        Determine direction from X/Y values.
        
        Args:
            x: X-axis value (0-255)
            y: Y-axis value (0-255)
            
        Returns:
            Direction name string
        """
        # Check center zone
        if (self.CENTER_X_MIN <= x <= self.CENTER_X_MAX and
            self.CENTER_Y_MIN <= y <= self.CENTER_Y_MAX):
            return 'CENTER'
        
        # Check diagonals
        if x > self.DIAGONAL_THRESHOLD_HIGH and y > self.DIAGONAL_THRESHOLD_HIGH:
            return 'NORTH_EAST'
        if x < self.DIAGONAL_THRESHOLD_LOW and y > (255 - self.DIAGONAL_THRESHOLD_LOW):
            return 'NORTH_WEST'
        if x > self.DIAGONAL_THRESHOLD_HIGH and y < self.DIAGONAL_THRESHOLD_LOW:
            return 'SOUTH_EAST'
        if x < self.DIAGONAL_THRESHOLD_LOW and y < self.DIAGONAL_THRESHOLD_LOW:
            return 'SOUTH_WEST'
        
        # Check cardinals
        if y >= self.THRESHOLD_NORTH_Y and self.CENTER_X_MIN <= x <= self.CENTER_X_MAX:
            return 'NORTH'
        if y <= self.THRESHOLD_SOUTH_Y and self.CENTER_X_MIN <= x <= self.CENTER_X_MAX:
            return 'SOUTH'
        if x >= self.THRESHOLD_EAST_X and self.CENTER_Y_MIN <= y <= self.CENTER_X_MAX:
            return 'EAST'
        if x <= self.THRESHOLD_WEST_X and self.CENTER_Y_MIN <= y <= self.CENTER_X_MAX:
            return 'WEST'
        
        return 'CENTER'
    
    def _draw_zones(self, ax):
        """Draw the direction zones on the axes."""
        # Colors
        colors = {
            'center': '#4CAF50',
            'north': '#2196F3',
            'south': '#FF9800',
            'east': '#9C27B0',
            'west': '#F44336',
            'ne': '#00BCD4',
            'nw': '#3F51B5',
            'se': '#FFEB3B',
            'sw': '#795548',
        }
        
        # Background
        ax.add_patch(patches.Rectangle((0, 0), 255, 255, facecolor='#E0E0E0'))
        
        # Diagonal zones
        ax.add_patch(patches.Rectangle(
            (self.DIAGONAL_THRESHOLD_HIGH, self.DIAGONAL_THRESHOLD_HIGH),
            255 - self.DIAGONAL_THRESHOLD_HIGH, 255 - self.DIAGONAL_THRESHOLD_HIGH,
            facecolor=colors['ne'], alpha=0.6))
        ax.add_patch(patches.Rectangle(
            (0, 255 - self.DIAGONAL_THRESHOLD_LOW),
            self.DIAGONAL_THRESHOLD_LOW, self.DIAGONAL_THRESHOLD_LOW,
            facecolor=colors['nw'], alpha=0.6))
        ax.add_patch(patches.Rectangle(
            (self.DIAGONAL_THRESHOLD_HIGH, 0),
            255 - self.DIAGONAL_THRESHOLD_HIGH, self.DIAGONAL_THRESHOLD_LOW,
            facecolor=colors['se'], alpha=0.6))
        ax.add_patch(patches.Rectangle(
            (0, 0), self.DIAGONAL_THRESHOLD_LOW, self.DIAGONAL_THRESHOLD_LOW,
            facecolor=colors['sw'], alpha=0.6))
        
        # Cardinal zones
        ax.add_patch(patches.Rectangle(
            (self.CENTER_X_MIN, self.THRESHOLD_NORTH_Y),
            self.CENTER_X_MAX - self.CENTER_X_MIN, 255 - self.THRESHOLD_NORTH_Y,
            facecolor=colors['north'], alpha=0.6))
        ax.add_patch(patches.Rectangle(
            (self.CENTER_X_MIN, 0),
            self.CENTER_X_MAX - self.CENTER_X_MIN, self.THRESHOLD_SOUTH_Y,
            facecolor=colors['south'], alpha=0.6))
        ax.add_patch(patches.Rectangle(
            (self.THRESHOLD_EAST_X, self.CENTER_Y_MIN),
            255 - self.THRESHOLD_EAST_X, self.CENTER_X_MAX - self.CENTER_Y_MIN,
            facecolor=colors['east'], alpha=0.6))
        ax.add_patch(patches.Rectangle(
            (0, self.CENTER_Y_MIN),
            self.THRESHOLD_WEST_X, self.CENTER_X_MAX - self.CENTER_Y_MIN,
            facecolor=colors['west'], alpha=0.6))
        
        # Center zone
        ax.add_patch(patches.Rectangle(
            (self.CENTER_X_MIN, self.CENTER_Y_MIN),
            self.CENTER_X_MAX - self.CENTER_X_MIN, self.CENTER_Y_MAX - self.CENTER_Y_MIN,
            facecolor=colors['center'], alpha=0.8))
    
    def create_interactive(self):
        """Create an interactive matplotlib visualization with sliders."""
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        plt.subplots_adjust(bottom=0.25)
        
        self.ax.set_xlim(0, 255)
        self.ax.set_ylim(0, 255)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X Axis (ADC Value)', fontsize=12)
        self.ax.set_ylabel('Y Axis (ADC Value)', fontsize=12)
        self.ax.set_title('Interactive Joystick Visualizer', fontsize=14, fontweight='bold')
        
        # Draw zones
        self._draw_zones(self.ax)
        
        # Initial position marker
        self.position_marker, = self.ax.plot(128, 128, 'ko', markersize=15)
        
        # Direction text
        self.direction_text = self.ax.text(
            128, 270, 'Direction: CENTER',
            fontsize=14, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )
        
        # Create sliders
        ax_x = plt.axes([0.2, 0.1, 0.6, 0.03])
        ax_y = plt.axes([0.2, 0.05, 0.6, 0.03])
        
        self.x_slider = Slider(ax_x, 'X', 0, 255, valinit=128, valstep=1)
        self.y_slider = Slider(ax_y, 'Y', 0, 255, valinit=128, valstep=1)
        
        def update(val):
            x = int(self.x_slider.val)
            y = int(self.y_slider.val)
            
            self.position_marker.set_data([x], [y])
            direction = self.get_direction(x, y)
            self.direction_text.set_text(f'Direction: {direction}\n(X={x}, Y={y})')
            self.fig.canvas.draw_idle()
        
        self.x_slider.on_changed(update)
        self.y_slider.on_changed(update)
        
        self.ax.grid(True, alpha=0.3)
        
        plt.show()
    
    def simulate_movement(self, output_dir: str = None):
        """
        Generate a simulation showing joystick movement.
        
        Creates a series of frames showing the joystick moving through
        all directions.
        
        Args:
            output_dir: Directory to save output images
        """
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = Path(__file__).parent.parent / 'docs' / 'images'
        output_path.mkdir(parents=True, exist_ok=True)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Positions for a full rotation demo
        positions = [
            (128, 128, 'CENTER'),
            (128, 250, 'NORTH'),
            (250, 250, 'NORTH_EAST'),
            (250, 128, 'EAST'),
            (250, 30, 'SOUTH_EAST'),
            (128, 30, 'SOUTH'),
            (30, 30, 'SOUTH_WEST'),
            (30, 128, 'WEST'),
            (30, 220, 'NORTH_WEST'),
            (128, 128, 'CENTER'),  # Return to center
        ]
        
        print("Generating movement simulation...")
        
        for i, (x, y, expected_dir) in enumerate(positions):
            ax.clear()
            ax.set_xlim(0, 255)
            ax.set_ylim(0, 255)
            ax.set_aspect('equal')
            ax.set_xlabel('X Axis')
            ax.set_ylabel('Y Axis')
            ax.set_title(f'Joystick Position: {expected_dir}', fontsize=14, fontweight='bold')
            
            self._draw_zones(ax)
            
            ax.plot(x, y, 'ko', markersize=20)
            ax.plot(x, y, 'wo', markersize=10)
            
            ax.text(128, 270, f'X={x}, Y={y}', fontsize=12, ha='center',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            ax.grid(True, alpha=0.3)
            
            filename = output_path / f'simulation_frame_{i:02d}.png'
            plt.savefig(filename, dpi=100, bbox_inches='tight')
            print(f"  Saved: {filename}")
        
        plt.close()
        print(f"Simulation frames saved to: {output_path}")


def main():
    """Run the interactive visualizer or generate simulation."""
    import sys
    
    visualizer = JoystickVisualizer()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--simulate':
        visualizer.simulate_movement()
    else:
        print("Starting interactive visualizer...")
        print("Use the sliders to move the joystick position.")
        visualizer.create_interactive()


if __name__ == '__main__':
    main()
