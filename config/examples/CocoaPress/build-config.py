#!/usr/bin/python

# Portions (c) 2019, Cocoa Press.
# Portions (c) 2019 Aleph Objects, Inc.
# Portions (c) 2019 Marcio Teixeira
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License, go to the following
# location: <http://www.gnu.org/licenses/>.

from __future__ import print_function
import argparse, re, sys, os

PRINTER_CHOICES = [
    "CocoaPress_Einsy",
    "CocoaPress_Archim",
    "CocoaPress_TouchDemo"
]

TOOLHEAD_CHOICES = [
    "CocoaPress_SingleExtruder"
]

usage = (
'''This script modifies Marlin's "Configuration.h" and "Configuration_adv.h" for
LulzBot printers.'''
+ "   \n\n    Printer  Choices:\n      " + "\n      ".join(PRINTER_CHOICES)
+ "   \n\n    Toolhead Choices:\n      " + "\n      ".join(TOOLHEAD_CHOICES)
)

############################ START OF CONFIGURATION ###########################

# Table of Contents:
# ------------------
#
#   1. PRINTER MODEL CHARACTERISTICS
#   2. GENERAL CONFIGURATION
#   3. EXPERIMENTAL FEATURES
#   4. NEOPIXEL SUPPORT
#   5. MOTHERBOARD AND PIN CONFIGURATION
#   6. ENDSTOP CONFIGURATION
#   7. HOMING & AXIS DIRECTIONS
#   8. PROBING OPTIONS
#   9. COCOA PRESS TOOLHEADS
#  10. TEMPERATURE SETTINGS
#  11. COOLING FAN CONFIGURATION
#  12. AXIS TRAVEL LIMITS
#  13. AUTOLEVELING / BED PROBE
#  14. FILAMENT CONFIGURATION
#  15. MOTOR DRIVER TYPE
#  16. TRINAMIC DRIVER CONFIGURATION
#  17. TRINAMIC SENSORLESS HOMING
#  18. MOTOR CURRENTS
#  19. ACCELERATION, FEEDRATES AND XYZ MOTOR STEPS
#  20. LCD OPTIONS

def C_STRING(str):
    return '"' + str.strip().replace('\n','\\n') + '"'

def make_config(PRINTER, TOOLHEAD):
    MARLIN = {}

    def ENABLED(str):
        return str in MARLIN and MARLIN[str]

################################## DEFAULTS ###################################

    USE_EINSY_RETRO                                      = False
    USE_ARCHIM2                                          = False
    USE_AUTOLEVELING                                     = False
    USE_TOUCH_UI                                         = True

    MARLIN["SDSUPPORT"]                                  = False
    MARLIN["BLTOUCH"]                                    = False

######################## PRINTER MODEL CHARACTERISTICS ########################

    if PRINTER == "CocoaPress_Einsy":
        USE_EINSY_RETRO                                  = True
        MARLIN["SDSUPPORT"]                              = True
        MARLIN["CUSTOM_MACHINE_NAME"]                    = C_STRING("Cocoa Press")

    if PRINTER == "CocoaPress_Archim":
        USE_ARCHIM2                                      = True
        MARLIN["USB_FLASH_DRIVE_SUPPORT"]                = True
        MARLIN["SENSORLESS_HOMING"]                      = True
        MARLIN["BLTOUCH"]                                = True
        MARLIN["FILAMENT_RUNOUT_SENSOR"]                 = True
        MARLIN["CUSTOM_MACHINE_NAME"]                    = C_STRING("Cocoa Press")

    if PRINTER == "CocoaPress_TouchDemo":
        USE_EINSY_RETRO                                  = True
        MARLIN["CUSTOM_MACHINE_NAME"]                    = C_STRING("TouchDemo")
        MARLIN["USB_FLASH_DRIVE_SUPPORT"]                = False

############################ GENERAL CONFIGURATION ############################

    MARLIN["STRING_CONFIG_H_AUTHOR"]                     = C_STRING("(Cocoa Press Marlin)")
    MARLIN["EEPROM_SETTINGS"]                            = True # EW - Enabled
    MARLIN["PRINTCOUNTER"]                               = True # EW - Enabled
    MARLIN["CUSTOM_MACHINE_NAME"]                        = C_STRING("Cocoa Press")
    MARLIN["MACHINE_UUID"]                               = C_STRING("c51664e3-50b4-40fb-9bd0-63a8cd30df18")

############################ NEOPIXEL SUPPORT ############################

    MARLIN["CASE_LIGHT_ENABLE"]                          = True
    MARLIN["CASE_LIGHT_USE_NEOPIXEL"]                    = True

    MARLIN["NEOPIXEL_LED"]                               = True
    MARLIN["NEOPIXEL_PIXELS"]                            = 16
    if USE_ARCHIM2:
      MARLIN["NEOPIXEL_PIN"]                             = 94 # GPIO_PB1_J20_5
    else:
      MARLIN["NEOPIXEL_PIN"]                             = 9
    #MARLIN["NEOPIXEL_STARTUP_TEST"]                      = True

###################### MOTHERBOARD AND PIN CONFIGURATION ######################

    MARLIN["CONTROLLER_FAN_PIN"]                         = 'FAN1_PIN' # Digital pin 6
        
    if USE_ARCHIM2:
        MARLIN["MOTHERBOARD"]                            = 'BOARD_ARCHIM2'
        MARLIN["SERIAL_PORT"]                            = -1

        # The host MMC bridge is impractically slow and should not be used
        if ENABLED("SDSUPPORT") or ENABLED("USB_FLASH_DRIVE_SUPPORT"):
            MARLIN["DISABLE_DUE_SD_MMC"]                 = True

    elif USE_EINSY_RETRO:
        MARLIN["MOTHERBOARD"]                            = 'BOARD_EINSY_RETRO'
        MARLIN["SERIAL_PORT"]                            = 0

    if ENABLED("USB_FLASH_DRIVE_SUPPORT"):
        MARLIN["USB_INTR_PIN"]                           = 'SD_DETECT_PIN'

############################ ENDSTOP CONFIGURATION ############################

    MARLIN["Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN"]         = True

    MARLIN["USE_XMIN_PLUG"]                              = True
    MARLIN["USE_YMIN_PLUG"]                              = False
    MARLIN["USE_ZMIN_PLUG"]                              = True

    MARLIN["USE_XMAX_PLUG"]                              = False
    MARLIN["USE_YMAX_PLUG"]                              = True # EW - eventually use this one? gives compiling errors
    MARLIN["USE_ZMAX_PLUG"]                              = False
    
    MARLIN["X_MIN_ENDSTOP_INVERTING"]                    = 'false'
    MARLIN["Z_MIN_ENDSTOP_INVERTING"]                    = 'false' # EW - set back to false set to true (https://www.youtube.com/watch?v=G-TwWfUzXpc) set to true to invert the logic of the endstop.

    MARLIN["SD_ABORT_ON_ENDSTOP_HIT"]                    = ENABLED("SDSUPPORT")

########################## HOMING & AXIS DIRECTIONS ###########################

    MARLIN["COREXY"]                                     = True
    MARLIN["INVERT_X_DIR"]                               = 'false'
    MARLIN["INVERT_Y_DIR"]                               = 'true'
    MARLIN["INVERT_Z_DIR"]                               = 'true'
    MARLIN["INVERT_E0_DIR"]                              = 'false'
    MARLIN["INVERT_E1_DIR"]                              = 'false'

    MARLIN["X_HOME_DIR"]                                 = -1
    MARLIN["Y_HOME_DIR"]                                 =  1
    MARLIN["Z_HOME_DIR"]                                 = -1
    
    MARLIN["Z_SAFE_HOMING"]                              = True # EW - Enabled to zero z in the middle of the bed
    MARLIN["HOMING_FEEDRATE_Z"]                          = 5*60 # EW - changed from 4 to 6
    
################################ COCOA PRESS TOOLHEADS ###############################

    if TOOLHEAD in ["CocoaPress_SingleExtruder"]:
        MARLIN["EXTRUDERS"]                              = 1
        MARLIN["HOTENDS"]                                = 3 if USE_ARCHIM2 else 1
        MARLIN["E0_CURRENT"]                             = 960 # mA

############################# TEMPERATURE SETTINGS ############################

    MARLIN["PIDTEMP"]                                    = True # EW - skipping this section for now
    
    MARLIN["THERMAL_PROTECTION_HOTENDS"]                 = False # EW - TEMP DISABLED
    MARLIN["PREVENT_COLD_EXTRUSION"]                     = False # EW - Turning off so we can use solenoid even when chocolate is cold
    MARLIN["EXTRUDE_MINTEMP"]                            = 10 # EW - changed from 175 to 10

    # 999 is the custom CocoaPress thermistor profile
    MARLIN["TEMP_SENSOR_0"]                              = 999
    if MARLIN["HOTENDS"] > 1:
      MARLIN["TEMP_SENSOR_1"]                            = 999
      MARLIN["TEMP_SENSOR_2"]                            = 999
    MARLIN["TEMP_SENSOR_CHAMBER"]                        = 999
        
    MARLIN["TOUCH_UI_LCD_TEMP_SCALING"]                  = 10 # Scale all UI temperatures by 10
    
    # These values are scaled by 10
    MARLIN["HEATER_0_MAXTEMP"]                           = 500
    MARLIN["HEATER_1_MAXTEMP"]                           = 500
    MARLIN["HEATER_2_MAXTEMP"]                           = 500
    MARLIN["HEATER_3_MAXTEMP"]                           = 500
    MARLIN["HEATER_4_MAXTEMP"]                           = 500
    MARLIN["HEATER_5_MAXTEMP"]                           = 500
    MARLIN["CHAMBER_MAXTEMP"]                            = 500
    
    MARLIN["HEATER_0_MINTEMP"]                           = -10
    MARLIN["HEATER_1_MINTEMP"]                           = -10
    MARLIN["HEATER_2_MINTEMP"]                           = -10
    MARLIN["HEATER_3_MINTEMP"]                           = -10
    MARLIN["HEATER_4_MINTEMP"]                           = -10
    MARLIN["HEATER_5_MINTEMP"]                           = -10
    MARLIN["CHAMBER_MINTEMP"]                            = -10
    
    MARLIN["THERMAL_PROTECTION_HYSTERESIS"]              = 1 # EW - changed from 4 to 1
    MARLIN["HEATER_CHAMBER_INVERTING"]                   = 'true' # Activate cooler when temperature is above threshold
    MARLIN["THERMAL_PROTECTION_CHAMBER"]                 = False
    
    # Preheat options for chocolate
    
    MARLIN["PREHEAT_1_LABEL"]                            = C_STRING("Cocoa")
    MARLIN["COCOA_PRESS_PREHEAT_SECONDS"]                = 30*60
    MARLIN["COCOA_PRESS_PREHEAT_SCRIPT"]                 = C_STRING("M104 S300 T0")
    
########################## COOLING FAN CONFIGURATION ##########################

    # Set fan speed to 122Hz for compatibility with some fans.

    if USE_ARCHIM2:
        # On the Archim, it is necessary to use soft PWM to get the
        # frequency down in the kilohertz
        MARLIN["FAN_SOFT_PWM"]                           = True
    else:
        # By default, FAST_PWM_FAN_FREQUENCY sets PWM to ~31kHz,
        # but we want to lower this to 122 Hz.
        MARLIN["FAST_PWM_FAN"]                           = True
        MARLIN["FAST_PWM_FAN_FREQUENCY"]                 = 122

    MARLIN["FAN_KICKSTART_TIME"]                         = 100
    MARLIN["FAN_MIN_PWM"]                                = 70
    MARLIN["SOFT_PWM_SCALE"]                             = 4

    MARLIN["USE_CONTROLLER_FAN"]                         = True
    if USE_EINSY_RETRO:
        # The TMC drivers need a bit more cooling
        MARLIN["CONTROLLERFAN_SPEED"]                    = 255
        MARLIN["CONTROLLERFAN_SPEED_Z_ONLY"]             = 120

############################### AXIS TRAVEL LIMITS ###############################

    MARLIN["X_MIN_POS"]                                  = 0
    MARLIN["Y_MIN_POS"]                                  = 0
    MARLIN["Z_MAX_POS"]                                  = 155
                                                       
    MARLIN["X_BED_SIZE"]                                 = 230
    MARLIN["Y_BED_SIZE"]                                 = 170

########################## AUTOLEVELING / BED PROBE ###########################

    if USE_AUTOLEVELING:
      MARLIN["FIX_MOUNTED_PROBE"]                        = False # EW - inductive sensor
      MARLIN["NOZZLE_TO_PROBE_OFFSET"]                   = [-20.7, 47.05, .5] # EW - as of 3/24/19 3pm
      MARLIN["XY_PROBE_SPEED"]                           = 8000 # EW - 3000 to stop binding
      MARLIN["Z_MIN_PROBE_REPEATABILITY_TEST"]           = True # EW - enabled
      MARLIN["AUTO_BED_LEVELING_BILINEAR"]               = True
            
      MARLIN["MESH_TEST_HOTEND_TEMP"]                    = 32 # EW - changed to 32 (celsius) Default nozzle temperature for the G26 Mesh Validation Tool.
      
      if MARLIN["BLTOUCH"]:
        MARLIN["Z_CLEARANCE_DEPLOY_PROBE"]               = 15
        MARLIN["Z_CLEARANCE_DEPLOY_PROBE"]               = 15
        MARLIN["MIN_PROBE_EDGE"]                         = 22

############################# FILAMENT SETTINGS ############################

    MARLIN["RETRACT_LENGTH"]                           = 0 # EW - changed retract to 0

    if ENABLED("FILAMENT_RUNOUT_SENSOR"):
        MARLIN["NUM_RUNOUT_SENSORS"]                     = 1
        MARLIN["FILAMENT_RUNOUT_SCRIPT"]                 = C_STRING("M25\nM0 I'm hungry, feed me more chocolate.")
        MARLIN["FILAMENT_RUNOUT_DISTANCE_MM"]            = 50
    
############################## MOTOR DRIVER TYPE ##############################

    if USE_EINSY_RETRO or USE_ARCHIM2:
        DRIVER_TYPE                                      = 'TMC2130'
    else:
        DRIVER_TYPE                                      = 'A4988'

    # Workaround for E stepper not working on Archim 2.0
    #   https://github.com/MarlinFirmware/Marlin/issues/13040
    if USE_EINSY_RETRO:
        # On AVR, it is okay to use the default (0) for TRINAMICS
        MARLIN["MINIMUM_STEPPER_PULSE"]                  = 0
    else:
        # For the Archim, setting this to the default (0) for TRINAMICS causes
        # the E stepper not to advance when LIN_ADVANCE is enabled, so force
        # the stepper pulse to 1 to match the other drivers.
        MARLIN["MINIMUM_STEPPER_PULSE"]                  = 1

    MARLIN["X_DRIVER_TYPE"]                              =  DRIVER_TYPE
    MARLIN["Y_DRIVER_TYPE"]                              =  DRIVER_TYPE
    MARLIN["Z_DRIVER_TYPE"]                              =  DRIVER_TYPE
    MARLIN["E0_DRIVER_TYPE"]                             =  DRIVER_TYPE
    if MARLIN["EXTRUDERS"] > 1:
        MARLIN["E1_DRIVER_TYPE"]                         =  DRIVER_TYPE

######################## TRINAMIC DRIVER CONFIGURATION ########################

    if USE_EINSY_RETRO or USE_ARCHIM2:
        RSENSE                                           = 0.12

        MARLIN["TMC_DEBUG"]                              = True
        MARLIN["MONITOR_DRIVER_STATUS"]                  = True
        MARLIN["HOLD_MULTIPLIER"]                        = 0.5
        
        MARLIN["X_RSENSE"]                               = RSENSE
        MARLIN["Y_RSENSE"]                               = RSENSE
        MARLIN["Z_RSENSE"]                               = RSENSE
        MARLIN["E0_RSENSE"]                              = RSENSE
        if MARLIN["EXTRUDERS"] > 1:
            MARLIN["E1_RSENSE"]                          = RSENSE

        MARLIN["TMC_USE_SW_SPI"]                         = USE_ARCHIM2
        
########################## TRINAMIC SENSORLESS HOMING ##########################

    if ENABLED("SENSORLESS_HOMING"):
        #MARLIN["X_STALL_SENSITIVITY"]                   = 4
        #MARLIN["Y_STALL_SENSITIVITY"]                   = 4

        MARLIN["USE_XMIN_PLUG"]                          = True # Uses Stallguard
        MARLIN["USE_YMAX_PLUG"]                          = True # Uses Stallguard
        
        MARLIN["X_MIN_ENDSTOP_INVERTING"]                = 1
        MARLIN["Y_MAX_ENDSTOP_INVERTING"]                = 1

        # Quickhome does not work with sensorless homing
        MARLIN["QUICK_HOME"]                             = False

        MARLIN["X_HOME_BUMP_MM"]                         = 0
        MARLIN["Y_HOME_BUMP_MM"]                         = 0
        
        # Leaving the toolhead resting on the endstops with sensorless homing
        # will likely cause chatter if the machine is immediately re-homed, so
        # don't leave the head sitting on the endstops after homing.
        MARLIN["HOMING_BACKOFF_MM"]                      = [5, 5, 2]

################################ MOTOR CURRENTS ###############################

    # These values specify the maximum current, but actual
    # currents may be lower when used with COOLCONF
            
    if USE_EINSY_RETRO:
        MARLIN["X_CURRENT"]                              = 920 # mA
        MARLIN["Y_CURRENT"]                              = 920 # mA
        MARLIN["Z_CURRENT"]                              = 960 # mA
                                                     
    elif USE_ARCHIM2:                                
        MARLIN["X_CURRENT"]                              = 975 # mA
        MARLIN["Y_CURRENT"]                              = 975 # mA
        MARLIN["Z_CURRENT"]                              = 975 # mA

################# ACCELERATION, FEEDRATES AND XYZ MOTOR STEPS #################

    MARLIN["DEFAULT_AXIS_STEPS_PER_UNIT"]                = [80, 80, 400, 500]
    # EW - 1600 for IGUS Z changed from default of 4000
    # Z-axis leadscrew https://www.amazon.com/Witbot-Pillow-Bearing-Coupler-Printer/dp/B074Z4Q23M/ref=sr_1_4?ie=UTF8&qid=1549046242&sr=8-4&keywords=lead%20screw
    
    MARLIN["DEFAULT_MAX_FEEDRATE"]                       = [300, 300, 100, 25] # EW - slowed X and Y by a factor of 10
    
    # A 32-bit board can handle more segments
    MARLIN["MIN_STEPS_PER_SEGMENT"]                      = 1 if USE_ARCHIM2 else 6

################################## LCD OPTIONS ##################################

    # Slow down SPI speed when using unshielded ribbon cables.
    MARLIN["SPI_SPEED"]                                  = 'SPI_SIXTEENTH_SPEED'
    
    MARLIN["LCD_TIMEOUT_TO_STATUS"]                      = 600000 # Ten Minutes     
    MARLIN["TOUCH_UI_FTDI_EVE"]                           = True
    MARLIN["TOUCH_UI_COCOA_PRESS"]                       = True
    MARLIN["LCD_ALEPHOBJECTS_CLCD_UI"]                   = True
    MARLIN["TOUCH_UI_800x480"]                           = True
    if USE_ARCHIM2:
      MARLIN["AO_EXP2_PINMAP"]                           = True
    else:
      MARLIN["AO_EXP1_PINMAP"]                           = True
    MARLIN["TOUCH_UI_USE_UTF8"]                          = True
    MARLIN["TOUCH_UI_UTF8_COPYRIGHT"]                    = True
    MARLIN["TOUCH_UI_UTF8_SUPERSCRIPTS"]                 = True
    MARLIN["SD_DETECT_INVERTED"]                         = False
    MARLIN["SCROLL_LONG_FILENAMES"]                      = True
    MARLIN["TOUCH_UI_DEVELOPER_MENU"]                    = True
    MARLIN["TOUCH_UI_DEBUG"]                             = False
                                                         
    # Virtual joystick functionality                     
    MARLIN["JOYSTICK"]                                   = True
    MARLIN["JOY_X_PIN"]                                  = -1
    MARLIN["JOY_Y_PIN"]                                  = -1
    MARLIN["JOY_Z_PIN"]                                  = -1
    MARLIN["JOY_EN_PIN"]                                 = -1
    MARLIN["JOY_X_LIMITS"]                               = False
    MARLIN["JOY_Y_LIMITS"]                               = False
    MARLIN["JOY_Z_LIMITS"]                               = False
                                                         
    if ENABLED("USB_FLASH_DRIVE_SUPPORT"):               
      MARLIN["SDSUPPORT"]                                = True
      MARLIN["USE_UHS3_USB"]                             = USE_ARCHIM2
                                                         
    if USE_ARCHIM2:                                      
      MARLIN["ARCHIM2_SPI_FLASH_EEPROM_BACKUP_SIZE"]     = 1000
                                                         
    MARLIN["SHOW_CUSTOM_BOOTSCREEN"]                     = True
    MARLIN["BABYSTEPPING"]                               = False
    MARLIN["BABYSTEP_XY"]                                = False
                                                         
    if USE_AUTOLEVELING:                                 
      MARLIN["BABYSTEP_ZPROBE_OFFSET"]                   = False
      MARLIN["BABYSTEP_HOTEND_Z_OFFSET"]                 = False

#################################### CLEAN UP ###################################

    return MARLIN

############################## END OF CONFIGURATION #############################

def format_list(list):
    """Formats a list in C style, i.e. {0, 1, 2}"""
    return "{" + ", ".join(['{}'.format(x) for x in list]) + "}"

def do_substitions(config, counts, line):
    """Perform substitutions on a #define line from the config"""

    line = line.rstrip()

    # Separate line into line and comment
    fields  = re.split('\s*//(?!#define)', line)
    if len(fields) == 2:
        command = fields[0]
        comment = fields[1]
    else:
        command = line
        comment = ""

    m = re.match('(\s*)(?://)?(#define\s*)(\w+)((?:\(\))?\s*)(.*)', command)
    if m:
        var = m.group(3)
        separator = m.group(4)
        if len(separator) == 0:
            separator = " "
        if var in config:
            val = config[var]
            if type(val) == bool and val == True:
                new_command = m.group(1) + m.group(2) + var
            elif type(val) == bool and val == False:
                new_command = m.group(1) + "//" + m.group(2) + var + separator + m.group(5)
            else:
                if type(val) == list:
                    new_val = format_list(val)
                elif type(val) == str:
                    new_val = val
                else:
                    new_val = '{}'.format(val)

                new_command = m.group(1) + m.group(2) + var + separator + new_val

            if new_command != command:
              line = new_command + " // <-- changed" + ((": " + comment) if comment else "")

            counts[var] += 1

    return line

def dump_variables(config, out_filename):
    """Dump all the variables in the config in sorted order"""
    outfile = open(out_filename, "w")
    for key in sorted(config.keys()):
        val = config[key]
        if type(val) == bool and val == True:
            print("#define", key, file = outfile)
        elif type(val) == bool and val == False:
            print("//#define", key, file = outfile)
        else:
            if type(val) == list:
                val = format_list(val)
            print("#define", key, val, file = outfile)
    outfile.close()

def process_config(config, counts, in_filename, out_filename):
    """Perform substitutions on an entire file"""
    if out_filename == in_filename:
        # Handle special case of in-place substitutions
        os.rename(in_filename, in_filename + ".saved")
        in_filename = in_filename + ".saved"
    outfile = open(out_filename, "w")
    infile  = open(in_filename, "r")
    with infile as f:
        for line in f:
            line = do_substitions(config, counts, line)
            print(line, file = outfile)
    outfile.close()
    infile.close()

def init_counters(config):
    counts = {}
    for k in config:
        counts[k] = 0
    return counts

def dump_counters(config, counts):
    for k in counts:
        if counts[k] == 0:
            print("Warning:", k, "not found in any of the configuration files.", file=sys.stderr)

def invalid_printer(str):
    parser.error(str + "\n\nPrinter must be one of:\n\n   " + "\n   ".join(PRINTER_CHOICES) + "\n")

def invalid_toolhead(str):
    parser.error(str + "\n\nToolhead must be one of:\n\n   " + "\n   ".join(TOOLHEAD_CHOICES) + "\n")

def match_selection(str, list):
    matches = [x for x in list if re.search(str, x, re.IGNORECASE)]
    if len(matches) > 1:
      # Try narrowing down the choices
      matches2 = [x for x in list if re.search("(\\b|_)" + str + "(\\b|_)", x, re.IGNORECASE)]
      if len(matches2) > 0:
        matches = matches2
    if len(matches) > 1:
        parser.error("Selection is ambiguous, must be one of:\n\n   " + "\n   ".join(matches) + "\n")
    if len(matches) == 0:
        parser.error("Invalid selection, must be one of:\n\n   " + "\n   ".join(list) + "\n")
    return matches[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('printer', help='printer type', nargs='?')
    parser.add_argument('toolhead', help='toolhead type', nargs='?')
    parser.add_argument('-D', '--directory', help="directory to save modified files")
    parser.add_argument('-i', '--input', help='input file', action="append")
    parser.add_argument('-s', '--summary', action='store_true', help='summarize configuration')
    args = parser.parse_args()

    if not args.printer:
        invalid_printer("Must specify a printer type.")

    if not args.toolhead:
        invalid_toolhead("Must specify a toolhead type.")

    args.printer  = match_selection(args.printer,  PRINTER_CHOICES)
    args.toolhead = match_selection(args.toolhead, TOOLHEAD_CHOICES)

    if not args.input:
        args.input = [
            "../../default/Configuration.h",
            "../../default/Configuration_adv.h"
        ]

    if not args.directory:
        args.directory = "."

    config = make_config(args.printer, args.toolhead)

    if args.directory:
        if not os.path.exists(args.directory):
            os.makedirs(args.directory)
        counts = init_counters(config)
        for i in args.input:
            process_config(config, counts, i, args.directory + "/" + os.path.basename(i))
        dump_counters(config, counts)

        if args.summary:
            dump_variables(config, args.directory + "/Configuration_summary.txt")