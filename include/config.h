/**
 * @file config.h
 * @brief Hardware configuration for AVR ATmega16/ATmega32 Joystick Interface
 * 
 * This file contains all hardware-specific definitions including pin assignments,
 * timing constants, and joystick calibration values.
 */

#ifndef CONFIG_H
#define CONFIG_H

/*============================================================================
 * CPU Configuration
 *============================================================================*/
#ifndef F_CPU
#define F_CPU 16000000UL  /**< CPU frequency in Hz (16 MHz default) */
#endif

/*============================================================================
 * Joystick ADC Configuration
 *============================================================================*/
#define JOYSTICK_X_CHANNEL      0       /**< ADC channel for X-axis */
#define JOYSTICK_Y_CHANNEL      1       /**< ADC channel for Y-axis */

/* ADC value range (8-bit mode) */
#define ADC_MIN                 0       /**< Minimum ADC value */
#define ADC_MAX                 255     /**< Maximum ADC value (8-bit) */
#define ADC_CENTER              128     /**< Center position value */

/*============================================================================
 * Direction Detection Thresholds
 *============================================================================*/
/* These thresholds define the zones for direction detection.
 * Values are for 8-bit ADC readings (0-255).
 * 
 *     Y=255 (North)
 *        |
 *  X=0 --+-- X=255
 * (West) |   (East)
 *     Y=0 (South)
 */

/* Cardinal direction thresholds */
#define THRESHOLD_NORTH_Y       240     /**< Y value above this = North */
#define THRESHOLD_SOUTH_Y       50      /**< Y value below this = South */
#define THRESHOLD_EAST_X        240     /**< X value above this = East */
#define THRESHOLD_WEST_X        70      /**< X value below this = West */

/* Center zone boundaries (dead zone) */
#define CENTER_X_MIN            70      /**< X minimum for center zone */
#define CENTER_X_MAX            180     /**< X maximum for center zone */
#define CENTER_Y_MIN            110     /**< Y minimum for center zone */
#define CENTER_Y_MAX            160     /**< Y maximum for center zone */

/* Diagonal detection thresholds */
#define DIAGONAL_THRESHOLD_HIGH 230     /**< High threshold for diagonals */
#define DIAGONAL_THRESHOLD_LOW  50      /**< Low threshold for diagonals */

/*============================================================================
 * LCD Pin Configuration (8-bit mode)
 *============================================================================*/
/* Control pins on PORTB */
#define LCD_RS_PIN              PB0     /**< Register Select pin */
#define LCD_RW_PIN              PB1     /**< Read/Write pin */
#define LCD_EN_PIN              PB2     /**< Enable pin */
#define LCD_CTRL_PORT           PORTB   /**< Control port */
#define LCD_CTRL_DDR            DDRB    /**< Control port direction */

/* Data pins on PORTC */
#define LCD_DATA_PORT           PORTC   /**< Data port */
#define LCD_DATA_DDR            DDRC    /**< Data port direction */

/* LCD timing (in milliseconds) */
#define LCD_ENABLE_PULSE_MS     10      /**< Enable pulse width */
#define LCD_COMMAND_DELAY_MS    10      /**< Delay after commands */

/*============================================================================
 * LCD Commands
 *============================================================================*/
#define LCD_CMD_FUNCTION_SET    0x38    /**< 8-bit, 2 lines, 5x7 font */
#define LCD_CMD_DISPLAY_ON      0x0E    /**< Display on, cursor on */
#define LCD_CMD_CLEAR           0x01    /**< Clear display */
#define LCD_CMD_ENTRY_MODE      0x06    /**< Increment cursor, no shift */
#define LCD_CMD_LINE1           0x80    /**< Start of line 1 */
#define LCD_CMD_LINE2           0xC0    /**< Start of line 2 */

/*============================================================================
 * General GPIO Configuration
 *============================================================================*/
#define LED_PORT                PORTD   /**< LED output port */
#define LED_DDR                 DDRD    /**< LED direction register */
#define JOYSTICK_INPUT_DDR      DDRA    /**< Joystick ADC input direction */

#endif /* CONFIG_H */
