#==============================================================================
# AVR-ATmega16-Joystick Makefile
# Build system for AVR ATmega16/ATmega32 joystick interface project
#==============================================================================

#------------------------------------------------------------------------------
# Target Configuration
#------------------------------------------------------------------------------
MCU          = atmega16
F_CPU        = 16000000UL
PROGRAMMER   = usbasp
PORT         = usb

#------------------------------------------------------------------------------
# Toolchain Configuration
#------------------------------------------------------------------------------
CC           = avr-gcc
OBJCOPY      = avr-objcopy
OBJDUMP      = avr-objdump
SIZE         = avr-size
AVRDUDE      = avrdude

#------------------------------------------------------------------------------
# Compiler Flags
#------------------------------------------------------------------------------
CFLAGS       = -mmcu=$(MCU)
CFLAGS      += -DF_CPU=$(F_CPU)
CFLAGS      += -Os
CFLAGS      += -Wall -Wextra -Werror
CFLAGS      += -std=c99
CFLAGS      += -I./include
CFLAGS      += -funsigned-char
CFLAGS      += -funsigned-bitfields
CFLAGS      += -fpack-struct
CFLAGS      += -fshort-enums

LDFLAGS      = -mmcu=$(MCU)

#------------------------------------------------------------------------------
# Source Files
#------------------------------------------------------------------------------
SRC_DIR      = src
INCLUDE_DIR  = include
EXAMPLES_DIR = examples
BUILD_DIR    = build

# Core library sources
LIB_SRCS     = $(SRC_DIR)/adc.c \
               $(SRC_DIR)/lcd.c \
               $(SRC_DIR)/joystick.c

LIB_OBJS     = $(LIB_SRCS:%.c=$(BUILD_DIR)/%.o)

#------------------------------------------------------------------------------
# Example Targets
#------------------------------------------------------------------------------
EXAMPLES     = digital_input adc_reading direction_display xy_display

#------------------------------------------------------------------------------
# Default Target
#------------------------------------------------------------------------------
.PHONY: all clean flash help examples $(EXAMPLES)

all: $(BUILD_DIR) lib
	@echo "Build complete. Use 'make <example>' to build an example."
	@echo "Available examples: $(EXAMPLES)"

help:
	@echo "AVR-ATmega16-Joystick Build System"
	@echo "=================================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all              - Build core library"
	@echo "  lib              - Build library objects only"
	@echo "  <example>        - Build specific example"
	@echo "  examples         - Build all examples"
	@echo "  flash-<example>  - Flash example to MCU"
	@echo "  clean            - Remove build artifacts"
	@echo "  size-<example>   - Show memory usage for example"
	@echo ""
	@echo "Available examples:"
	@echo "  digital_input    - Digital joystick input"
	@echo "  adc_reading      - Basic ADC reading"
	@echo "  direction_display - Direction on LCD"
	@echo "  xy_display       - X/Y coordinates on LCD"
	@echo ""
	@echo "Configuration:"
	@echo "  MCU=$(MCU)  F_CPU=$(F_CPU)"

#------------------------------------------------------------------------------
# Build Directory
#------------------------------------------------------------------------------
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)/$(SRC_DIR)
	@mkdir -p $(BUILD_DIR)/$(EXAMPLES_DIR)

#------------------------------------------------------------------------------
# Library Build
#------------------------------------------------------------------------------
lib: $(BUILD_DIR) $(LIB_OBJS)

$(BUILD_DIR)/$(SRC_DIR)/%.o: $(SRC_DIR)/%.c $(INCLUDE_DIR)/*.h
	@echo "CC  $<"
	@$(CC) $(CFLAGS) -c $< -o $@

#------------------------------------------------------------------------------
# Example Builds
#------------------------------------------------------------------------------
examples: $(EXAMPLES)

define EXAMPLE_template
$(1): $(BUILD_DIR) lib $(BUILD_DIR)/$(1).hex
	@echo "Built example: $(1)"

$(BUILD_DIR)/$(1).elf: $(EXAMPLES_DIR)/$(1)/main.c $(LIB_OBJS)
	@echo "LD  $$@"
	@$(CC) $(CFLAGS) $(LDFLAGS) -o $$@ $$^

$(BUILD_DIR)/$(1).hex: $(BUILD_DIR)/$(1).elf
	@echo "HEX $$@"
	@$(OBJCOPY) -O ihex -R .eeprom $$< $$@

flash-$(1): $(BUILD_DIR)/$(1).hex
	@echo "Flashing $(1)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -U flash:w:$$<:i

size-$(1): $(BUILD_DIR)/$(1).elf
	$(SIZE) --mcu=$(MCU) -C $$<
endef

$(foreach example,$(EXAMPLES),$(eval $(call EXAMPLE_template,$(example))))

#------------------------------------------------------------------------------
# Cleanup
#------------------------------------------------------------------------------
clean:
	@echo "Cleaning build directory..."
	@rm -rf $(BUILD_DIR)
	@echo "Clean complete."

#------------------------------------------------------------------------------
# Convenience Targets
#------------------------------------------------------------------------------
.PHONY: flash
flash: flash-direction_display

.PHONY: size
size: size-direction_display
