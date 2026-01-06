/**
 * @file joystick.h
 * @brief Joystick Interface for Analog Joystick Module
 * 
 * This module provides functions for reading joystick position and
 * determining the direction based on X/Y axis values.
 */

#ifndef JOYSTICK_H
#define JOYSTICK_H

#include <stdint.h>

/**
 * @brief Joystick direction enumeration
 * 
 * Represents the 9 possible directions: center, 4 cardinal, and 4 diagonal.
 */
typedef enum {
    DIR_CENTER = 0,     /**< Joystick at rest position */
    DIR_NORTH,          /**< Up direction */
    DIR_SOUTH,          /**< Down direction */
    DIR_EAST,           /**< Right direction */
    DIR_WEST,           /**< Left direction */
    DIR_NORTH_EAST,     /**< Up-Right diagonal */
    DIR_NORTH_WEST,     /**< Up-Left diagonal */
    DIR_SOUTH_EAST,     /**< Down-Right diagonal */
    DIR_SOUTH_WEST      /**< Down-Left diagonal */
} joystick_direction_t;

/**
 * @brief Joystick position structure
 * 
 * Holds the raw X and Y axis values from the ADC.
 */
typedef struct {
    uint8_t x;          /**< X-axis value (0-255) */
    uint8_t y;          /**< Y-axis value (0-255) */
} joystick_position_t;

/**
 * @brief Initialize the joystick interface
 * 
 * Configures ADC channels for X and Y axis reading.
 */
void joystick_init(void);

/**
 * @brief Read current joystick position
 * 
 * @param pos Pointer to joystick_position_t structure to store result
 */
void joystick_read(joystick_position_t *pos);

/**
 * @brief Get X-axis value
 * 
 * @return uint8_t X-axis ADC value (0-255)
 */
uint8_t joystick_get_x(void);

/**
 * @brief Get Y-axis value
 * 
 * @return uint8_t Y-axis ADC value (0-255)
 */
uint8_t joystick_get_y(void);

/**
 * @brief Determine direction from X/Y values
 * 
 * Uses threshold-based zone detection to categorize the joystick
 * position into one of 9 directions.
 * 
 * @param x X-axis value (0-255)
 * @param y Y-axis value (0-255)
 * @return joystick_direction_t Detected direction
 */
joystick_direction_t joystick_get_direction(uint8_t x, uint8_t y);

/**
 * @brief Convert direction enum to string
 * 
 * @param dir Direction enumeration value
 * @return const char* Human-readable direction string (e.g., "N", "NE", "C")
 */
const char* joystick_direction_to_string(joystick_direction_t dir);

/**
 * @brief Check if joystick is in center (dead) zone
 * 
 * @param x X-axis value (0-255)
 * @param y Y-axis value (0-255)
 * @return uint8_t 1 if in center zone, 0 otherwise
 */
uint8_t joystick_is_centered(uint8_t x, uint8_t y);

#endif /* JOYSTICK_H */
