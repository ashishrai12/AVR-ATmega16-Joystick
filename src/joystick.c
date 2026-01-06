/**
 * @file joystick.c
 * @brief Joystick Interface Implementation
 */

#include "../include/config.h"
#include "../include/adc.h"
#include "../include/joystick.h"

/* Direction name lookup table */
static const char* direction_names[] = {
    "C",    /* DIR_CENTER */
    "N",    /* DIR_NORTH */
    "S",    /* DIR_SOUTH */
    "E",    /* DIR_EAST */
    "W",    /* DIR_WEST */
    "NE",   /* DIR_NORTH_EAST */
    "NW",   /* DIR_NORTH_WEST */
    "SE",   /* DIR_SOUTH_EAST */
    "SW"    /* DIR_SOUTH_WEST */
};

void joystick_init(void)
{
    /* Initialize ADC for joystick readings */
    adc_init();
}

void joystick_read(joystick_position_t *pos)
{
    pos->x = adc_read_8bit(JOYSTICK_X_CHANNEL);
    pos->y = adc_read_8bit(JOYSTICK_Y_CHANNEL);
}

uint8_t joystick_get_x(void)
{
    return adc_read_8bit(JOYSTICK_X_CHANNEL);
}

uint8_t joystick_get_y(void)
{
    return adc_read_8bit(JOYSTICK_Y_CHANNEL);
}

uint8_t joystick_is_centered(uint8_t x, uint8_t y)
{
    return (x >= CENTER_X_MIN && x <= CENTER_X_MAX &&
            y >= CENTER_Y_MIN && y <= CENTER_Y_MAX);
}

joystick_direction_t joystick_get_direction(uint8_t x, uint8_t y)
{
    /* Check center zone first (dead zone) */
    if (joystick_is_centered(x, y)) {
        return DIR_CENTER;
    }
    
    /* Check diagonal directions (corners) */
    /* North-East: high X, high Y */
    if (x > DIAGONAL_THRESHOLD_HIGH && y > DIAGONAL_THRESHOLD_HIGH) {
        return DIR_NORTH_EAST;
    }
    
    /* North-West: low X, high Y */
    if (x < DIAGONAL_THRESHOLD_LOW && y > (ADC_MAX - DIAGONAL_THRESHOLD_LOW)) {
        return DIR_NORTH_WEST;
    }
    
    /* South-East: high X, low Y */
    if (x > DIAGONAL_THRESHOLD_HIGH && y < DIAGONAL_THRESHOLD_LOW) {
        return DIR_SOUTH_EAST;
    }
    
    /* South-West: low X, low Y */
    if (x < DIAGONAL_THRESHOLD_LOW && y < DIAGONAL_THRESHOLD_LOW) {
        return DIR_SOUTH_WEST;
    }
    
    /* Check cardinal directions */
    /* North: high Y, X near center */
    if (y >= THRESHOLD_NORTH_Y && x >= CENTER_X_MIN && x <= CENTER_X_MAX) {
        return DIR_NORTH;
    }
    
    /* South: low Y, X near center */
    if (y <= THRESHOLD_SOUTH_Y && x >= CENTER_X_MIN && x <= CENTER_X_MAX) {
        return DIR_SOUTH;
    }
    
    /* East: high X, Y near center */
    if (x >= THRESHOLD_EAST_X && y >= CENTER_Y_MIN && y <= CENTER_X_MAX) {
        return DIR_EAST;
    }
    
    /* West: low X, Y near center */
    if (x <= THRESHOLD_WEST_X && y >= CENTER_Y_MIN && y <= CENTER_X_MAX) {
        return DIR_WEST;
    }
    
    /* If no specific direction matched, return center */
    return DIR_CENTER;
}

const char* joystick_direction_to_string(joystick_direction_t dir)
{
    if (dir >= 0 && dir <= DIR_SOUTH_WEST) {
        return direction_names[dir];
    }
    return "?";
}
