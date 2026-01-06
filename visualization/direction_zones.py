"""
Direction Zones Visualization.

Generates static visualizations of joystick direction detection zones
matching the thresholds defined in config.h.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path


class DirectionZonesVisualizer:
    """
    Visualizer for joystick direction detection zones.
    
    Creates diagrams showing how the ADC value space is divided
    into different direction zones.
    """
    
    # Configuration matching config.h
    ADC_MIN = 0
    ADC_MAX = 255
    
    # Thresholds
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
    
    # Colors for each direction
    COLORS = {
        'center': '#4CAF50',      # Green
        'north': '#2196F3',       # Blue
        'south': '#FF9800',       # Orange
        'east': '#9C27B0',        # Purple
        'west': '#F44336',        # Red
        'north_east': '#00BCD4',  # Cyan
        'north_west': '#3F51B5',  # Indigo
        'south_east': '#FFEB3B',  # Yellow
        'south_west': '#795548',  # Brown
        'undefined': '#E0E0E0',   # Grey
    }
    
    def __init__(self, output_dir: str = None):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save output images
        """
        if output_dir:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.output_dir = Path(__file__).parent.parent / 'docs' / 'images'
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_zone_diagram(self, save: bool = True, show: bool = False) -> str:
        """
        Create a diagram showing all direction detection zones.
        
        Args:
            save: Whether to save the image
            show: Whether to display the image
            
        Returns:
            Path to saved image (if saved)
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Set up the axes
        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        ax.set_aspect('equal')
        ax.set_xlabel('X Axis (ADC Value)', fontsize=12)
        ax.set_ylabel('Y Axis (ADC Value)', fontsize=12)
        ax.set_title('Joystick Direction Detection Zones', fontsize=14, fontweight='bold')
        
        # Draw background (undefined zones)
        ax.add_patch(patches.Rectangle(
            (0, 0), 255, 255,
            facecolor=self.COLORS['undefined'],
            edgecolor='none'
        ))
        
        # Draw diagonal zones first (corners)
        # North-East (high X, high Y)
        self._draw_zone(ax, 
                       self.DIAGONAL_THRESHOLD_HIGH, self.DIAGONAL_THRESHOLD_HIGH,
                       255, 255,
                       'north_east', 'NE')
        
        # North-West (low X, high Y)
        self._draw_zone(ax,
                       0, 255 - self.DIAGONAL_THRESHOLD_LOW,
                       self.DIAGONAL_THRESHOLD_LOW, 255,
                       'north_west', 'NW')
        
        # South-East (high X, low Y)
        self._draw_zone(ax,
                       self.DIAGONAL_THRESHOLD_HIGH, 0,
                       255, self.DIAGONAL_THRESHOLD_LOW,
                       'south_east', 'SE')
        
        # South-West (low X, low Y)
        self._draw_zone(ax,
                       0, 0,
                       self.DIAGONAL_THRESHOLD_LOW, self.DIAGONAL_THRESHOLD_LOW,
                       'south_west', 'SW')
        
        # Draw cardinal zones
        # North (high Y, centered X)
        self._draw_zone(ax,
                       self.CENTER_X_MIN, self.THRESHOLD_NORTH_Y,
                       self.CENTER_X_MAX, 255,
                       'north', 'N')
        
        # South (low Y, centered X)
        self._draw_zone(ax,
                       self.CENTER_X_MIN, 0,
                       self.CENTER_X_MAX, self.THRESHOLD_SOUTH_Y,
                       'south', 'S')
        
        # East (high X, centered Y)
        self._draw_zone(ax,
                       self.THRESHOLD_EAST_X, self.CENTER_Y_MIN,
                       255, self.CENTER_X_MAX,
                       'east', 'E')
        
        # West (low X, centered Y)
        self._draw_zone(ax,
                       0, self.CENTER_Y_MIN,
                       self.THRESHOLD_WEST_X, self.CENTER_X_MAX,
                       'west', 'W')
        
        # Draw center zone (dead zone)
        self._draw_zone(ax,
                       self.CENTER_X_MIN, self.CENTER_Y_MIN,
                       self.CENTER_X_MAX, self.CENTER_Y_MAX,
                       'center', 'CENTER\n(Dead Zone)')
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Add threshold lines
        self._add_threshold_lines(ax)
        
        # Add legend
        self._add_legend(ax)
        
        plt.tight_layout()
        
        output_path = None
        if save:
            output_path = self.output_dir / 'direction_zones.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"Saved: {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(output_path) if output_path else None
    
    def _draw_zone(self, ax, x1, y1, x2, y2, color_key, label):
        """Draw a rectangular zone with label."""
        width = x2 - x1
        height = y2 - y1
        
        ax.add_patch(patches.Rectangle(
            (x1, y1), width, height,
            facecolor=self.COLORS[color_key],
            edgecolor='black',
            linewidth=1,
            alpha=0.7
        ))
        
        # Add label at center
        cx = x1 + width / 2
        cy = y1 + height / 2
        ax.text(cx, cy, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    
    def _add_threshold_lines(self, ax):
        """Add dashed lines showing threshold boundaries."""
        line_style = {'linestyle': '--', 'alpha': 0.5, 'linewidth': 1}
        
        # Horizontal thresholds
        ax.axhline(y=self.THRESHOLD_NORTH_Y, color='blue', **line_style)
        ax.axhline(y=self.THRESHOLD_SOUTH_Y, color='orange', **line_style)
        ax.axhline(y=self.CENTER_Y_MIN, color='green', **line_style)
        ax.axhline(y=self.CENTER_Y_MAX, color='green', **line_style)
        
        # Vertical thresholds
        ax.axvline(x=self.THRESHOLD_EAST_X, color='purple', **line_style)
        ax.axvline(x=self.THRESHOLD_WEST_X, color='red', **line_style)
        ax.axvline(x=self.CENTER_X_MIN, color='green', **line_style)
        ax.axvline(x=self.CENTER_X_MAX, color='green', **line_style)
    
    def _add_legend(self, ax):
        """Add a legend for the zones."""
        legend_elements = [
            patches.Patch(facecolor=self.COLORS['center'], edgecolor='black',
                         label='Center (Dead Zone)'),
            patches.Patch(facecolor=self.COLORS['north'], edgecolor='black',
                         label='North'),
            patches.Patch(facecolor=self.COLORS['south'], edgecolor='black',
                         label='South'),
            patches.Patch(facecolor=self.COLORS['east'], edgecolor='black',
                         label='East'),
            patches.Patch(facecolor=self.COLORS['west'], edgecolor='black',
                         label='West'),
            patches.Patch(facecolor=self.COLORS['north_east'], edgecolor='black',
                         label='North-East'),
            patches.Patch(facecolor=self.COLORS['north_west'], edgecolor='black',
                         label='North-West'),
            patches.Patch(facecolor=self.COLORS['south_east'], edgecolor='black',
                         label='South-East'),
            patches.Patch(facecolor=self.COLORS['south_west'], edgecolor='black',
                         label='South-West'),
        ]
        ax.legend(handles=legend_elements, loc='upper left', 
                 bbox_to_anchor=(1.02, 1), fontsize=9)
    
    def create_response_curve(self, save: bool = True, show: bool = False) -> str:
        """
        Create a joystick response curve visualization.
        
        Shows how ADC values map to direction zones.
        
        Args:
            save: Whether to save the image
            show: Whether to display the image
            
        Returns:
            Path to saved image (if saved)
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # X-axis response curve
        ax1 = axes[0]
        x_values = np.arange(0, 256)
        
        # Define zones for X axis
        x_zones = np.zeros_like(x_values, dtype=float)
        for i, x in enumerate(x_values):
            if x <= self.THRESHOLD_WEST_X:
                x_zones[i] = -1  # West
            elif x >= self.THRESHOLD_EAST_X:
                x_zones[i] = 1   # East
            elif self.CENTER_X_MIN <= x <= self.CENTER_X_MAX:
                x_zones[i] = 0   # Center
            else:
                x_zones[i] = np.interp(x, 
                                       [self.THRESHOLD_WEST_X, self.CENTER_X_MIN,
                                        self.CENTER_X_MAX, self.THRESHOLD_EAST_X],
                                       [-1, 0, 0, 1])
        
        ax1.plot(x_values, x_zones, 'b-', linewidth=2)
        ax1.fill_between(x_values, x_zones, alpha=0.3)
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax1.axvline(x=self.CENTER_X_MIN, color='g', linestyle='--', alpha=0.5, label='Center Zone')
        ax1.axvline(x=self.CENTER_X_MAX, color='g', linestyle='--', alpha=0.5)
        ax1.axvline(x=self.THRESHOLD_WEST_X, color='r', linestyle='--', alpha=0.5, label='West Threshold')
        ax1.axvline(x=self.THRESHOLD_EAST_X, color='purple', linestyle='--', alpha=0.5, label='East Threshold')
        ax1.set_xlabel('X-Axis ADC Value')
        ax1.set_ylabel('Direction (-1=West, 0=Center, 1=East)')
        ax1.set_title('X-Axis Response Curve')
        ax1.legend(loc='lower right')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 255)
        ax1.set_ylim(-1.2, 1.2)
        
        # Y-axis response curve
        ax2 = axes[1]
        y_values = np.arange(0, 256)
        
        y_zones = np.zeros_like(y_values, dtype=float)
        for i, y in enumerate(y_values):
            if y <= self.THRESHOLD_SOUTH_Y:
                y_zones[i] = -1  # South
            elif y >= self.THRESHOLD_NORTH_Y:
                y_zones[i] = 1   # North
            elif self.CENTER_Y_MIN <= y <= self.CENTER_Y_MAX:
                y_zones[i] = 0   # Center
            else:
                y_zones[i] = np.interp(y,
                                       [self.THRESHOLD_SOUTH_Y, self.CENTER_Y_MIN,
                                        self.CENTER_Y_MAX, self.THRESHOLD_NORTH_Y],
                                       [-1, 0, 0, 1])
        
        ax2.plot(y_values, y_zones, 'orange', linewidth=2)
        ax2.fill_between(y_values, y_zones, alpha=0.3, color='orange')
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.axvline(x=self.CENTER_Y_MIN, color='g', linestyle='--', alpha=0.5, label='Center Zone')
        ax2.axvline(x=self.CENTER_Y_MAX, color='g', linestyle='--', alpha=0.5)
        ax2.axvline(x=self.THRESHOLD_SOUTH_Y, color='orange', linestyle='--', alpha=0.5, label='South Threshold')
        ax2.axvline(x=self.THRESHOLD_NORTH_Y, color='blue', linestyle='--', alpha=0.5, label='North Threshold')
        ax2.set_xlabel('Y-Axis ADC Value')
        ax2.set_ylabel('Direction (-1=South, 0=Center, 1=North)')
        ax2.set_title('Y-Axis Response Curve')
        ax2.legend(loc='lower right')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 255)
        ax2.set_ylim(-1.2, 1.2)
        
        plt.suptitle('Joystick Response Curves', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        output_path = None
        if save:
            output_path = self.output_dir / 'joystick_response.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"Saved: {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(output_path) if output_path else None
    
    def create_hardware_diagram(self, save: bool = True, show: bool = False) -> str:
        """
        Create a hardware connection diagram.
        
        Args:
            save: Whether to save the image
            show: Whether to display the image
            
        Returns:
            Path to saved image (if saved)
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Hardware Connection Diagram', fontsize=14, fontweight='bold')
        
        # Draw ATmega16/32 MCU
        mcu_x, mcu_y = 6, 4
        mcu_w, mcu_h = 2.5, 3
        ax.add_patch(patches.FancyBboxPatch(
            (mcu_x - mcu_w/2, mcu_y - mcu_h/2), mcu_w, mcu_h,
            boxstyle="round,pad=0.1",
            facecolor='#3F51B5',
            edgecolor='black',
            linewidth=2
        ))
        ax.text(mcu_x, mcu_y, 'ATmega16/32', ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')
        
        # Draw Joystick module
        joy_x, joy_y = 1.5, 5
        joy_w, joy_h = 2, 1.8
        ax.add_patch(patches.FancyBboxPatch(
            (joy_x - joy_w/2, joy_y - joy_h/2), joy_w, joy_h,
            boxstyle="round,pad=0.1",
            facecolor='#4CAF50',
            edgecolor='black',
            linewidth=2
        ))
        ax.text(joy_x, joy_y + 0.3, 'Joystick', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
        ax.text(joy_x, joy_y - 0.3, 'Module', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
        
        # Draw LCD module
        lcd_x, lcd_y = 10.5, 4
        lcd_w, lcd_h = 2, 2
        ax.add_patch(patches.FancyBboxPatch(
            (lcd_x - lcd_w/2, lcd_y - lcd_h/2), lcd_w, lcd_h,
            boxstyle="round,pad=0.1",
            facecolor='#2196F3',
            edgecolor='black',
            linewidth=2
        ))
        ax.text(lcd_x, lcd_y + 0.3, 'LCD', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
        ax.text(lcd_x, lcd_y - 0.3, '16x2', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
        
        # Draw connections
        # Joystick to MCU
        self._draw_connection(ax, joy_x + joy_w/2, joy_y + 0.3,
                             mcu_x - mcu_w/2, mcu_y + 0.8,
                             'VRx → PA0', '#FF5722')
        self._draw_connection(ax, joy_x + joy_w/2, joy_y - 0.3,
                             mcu_x - mcu_w/2, mcu_y + 0.4,
                             'VRy → PA1', '#FF9800')
        
        # Power connections (joystick)
        ax.text(joy_x - joy_w/2 - 0.2, joy_y + 0.5, 'VCC', ha='right', va='center',
                fontsize=8, color='red')
        ax.text(joy_x - joy_w/2 - 0.2, joy_y - 0.5, 'GND', ha='right', va='center',
                fontsize=8, color='black')
        
        # MCU to LCD
        self._draw_connection(ax, mcu_x + mcu_w/2, mcu_y + 0.6,
                             lcd_x - lcd_w/2, lcd_y + 0.4,
                             'PORTC → D0-D7', '#9C27B0')
        self._draw_connection(ax, mcu_x + mcu_w/2, mcu_y,
                             lcd_x - lcd_w/2, lcd_y,
                             'PB0-2 → RS,RW,E', '#00BCD4')
        
        # Pin labels on MCU
        ax.text(mcu_x - mcu_w/2 - 0.1, mcu_y + 0.8, 'PA0', ha='right', va='center', fontsize=7)
        ax.text(mcu_x - mcu_w/2 - 0.1, mcu_y + 0.4, 'PA1', ha='right', va='center', fontsize=7)
        ax.text(mcu_x + mcu_w/2 + 0.1, mcu_y + 0.6, 'PORTC', ha='left', va='center', fontsize=7)
        ax.text(mcu_x + mcu_w/2 + 0.1, mcu_y, 'PORTB', ha='left', va='center', fontsize=7)
        
        # Add power supply box
        psu_x, psu_y = 1.5, 1.5
        ax.add_patch(patches.FancyBboxPatch(
            (psu_x - 0.8, psu_y - 0.5), 1.6, 1,
            boxstyle="round,pad=0.05",
            facecolor='#F44336',
            edgecolor='black',
            linewidth=1
        ))
        ax.text(psu_x, psu_y, '5V DC', ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')
        
        # Legend
        ax.text(0.5, 0.5, 'Connection Legend:', fontsize=9, fontweight='bold')
        legend_items = [
            ('VRx (X-axis analog)', '#FF5722'),
            ('VRy (Y-axis analog)', '#FF9800'),
            ('LCD Data Bus', '#9C27B0'),
            ('LCD Control', '#00BCD4'),
        ]
        for i, (label, color) in enumerate(legend_items):
            y_pos = 0.5 - (i + 1) * 0.4
            ax.plot([0.5, 1.2], [y_pos, y_pos], color=color, linewidth=2)
            ax.text(1.4, y_pos, label, fontsize=8, va='center')
        
        plt.tight_layout()
        
        output_path = None
        if save:
            output_path = self.output_dir / 'hardware_diagram.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
            print(f"Saved: {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(output_path) if output_path else None
    
    def _draw_connection(self, ax, x1, y1, x2, y2, label, color):
        """Draw a connection line with label."""
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 0.15
        ax.text(mid_x, mid_y, label, fontsize=7, ha='center', va='bottom',
                color=color, fontweight='bold')


def main():
    """Generate all visualization images."""
    print("Generating joystick visualizations...")
    
    visualizer = DirectionZonesVisualizer()
    
    # Generate all diagrams
    zone_path = visualizer.create_zone_diagram(save=True, show=False)
    response_path = visualizer.create_response_curve(save=True, show=False)
    hardware_path = visualizer.create_hardware_diagram(save=True, show=False)
    
    print("\nAll visualizations generated successfully!")
    print(f"Output directory: {visualizer.output_dir}")
    
    return [zone_path, response_path, hardware_path]


if __name__ == '__main__':
    main()
