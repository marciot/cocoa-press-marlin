![alt text][logo]

# *Cocoa Press* Marlin: UNDER DEVELOPMENT

This firmware is currently under development on a contract from [Cocoa Press] and is alpha level software.

Please do not attempt to use it on any printer (or do so at your own risk).

## How do I compile from source?

**Windows 10:** If you are using Windows 10, one of the easiest ways to build the firmware is using *Windows Subsystem for Linux (WSL)*. Simply follow [this guide] to set up WSL and get yourself an Ubuntu shell, then proceed with the steps for Linux.

**Linux:** Open a shell and execute the following commands one at a time:

```
sudo apt-get update
sudo apt-get install python git make rename
sudo apt-get install gcc-avr avr-libc
sudo apt-get install gcc-arm-none-eabi bossac-cli
sudo ln -s "/mnt/c/Users/YOUR_WINDOWS_USER_DIR/Documents" Documents
cd Documents
git clone https://github.com/marcio-cp/cocoa-press-marlin.git marlin
cd marlin
./build-configs.sh
./build-firmware.sh
```

Once this process is complete, the firmware files will be in the `build` directory of your Documents folder.

**Arduino IDE:** In order to use the Arduino IDE, you will need download and extract the zip file from the [GitHub repo].

The, go into the unpacked folder and replace the "Configuration.h" and "Configuration_adv.h" files in the "Marlin" subdirectory with one of the example configuration files from "config/examples/CocoaPress".

Open the "Marlin.ino" file from the "Marlin" subdirectory in the Arduino IDE.

Choose "Preferences" from the "File" menu and add "https://raw.githubusercontent.com/ultimachine/ArduinoAddons/master/package_ultimachine_index.json" to the "Additional Boards Manager URLs".

In the "Boards Manager":
    - If using Archim 2.0: Search for "Archim" and install "Archim by UltiMachine"
    - For all others: Search for "RAMBo" and install "RepRap Arduino-compatible Mother Board (RAMBo) by UltiMachine"

Choose the board corresponding to your printer from the "Board" submenu menu of the "Tools" menu.

To compile and upload the firmware to your printer, select "Upload" from the "Sketch" menu.

# Wiring notes:

On Einsy Retro:

| Feature          | Pin                 |
|------------------|---------------------|
| NeoPixel         | Pin 9 on header P1  |
| Extruder Control | N/A                 |
| Cooling Control  | N/A                 |
  
On Archim 2.0:

| Feature                | Port  | Arduino Pin | Archim Pin |
|------------------------|-------|-------------|------------|
| Nozzle Heater          | PC24  | 6           | HTR1       |
| Body Heater            | PC23  | 7           | HTR2       |
| Extra Heater           | PC22  | 8           | HTR3       |
| Case Light Control     | PC21  | 9           | HTBD       |
| Snapshot Control       | PB5   | 94          | J20 Pin 5  |
| Cooling Control        | PB3   | 103         | J20 Pin 7  |
| FIL_RUNOUT_PIN         | PB15  | 66          | J20 Pin 15 |
| FIL_RUNOUT2_PIN        | PB16  | 67          | J20 Pin 16 |
| Chocolate Level        | PB13  | 21          | J20 Pin 19 |
| SERVO0_PIN (BLTouch)   | PB12  | 20          | J20 Pin 20 |

# Using the chocolate fill sensor

A linear potentiometer may be used to adjust the chocolate level graphics on the status screen. Do implement this feature, connect a linear potentiometer
across pins 19, 23 and 24.

| GND                    | J20 Pin 23 |
| Chocolate Level        | J20 Pin 19 |
| 3.3V                   | J20 Pin 24 |

# Using the snapshot pin

Connect camera output to J20 Pin 5 and trigger using the following commands:

```
M42 S255 P94 ;Trigger
G4 P200      ;Wait for 200ms
M42 S0 P94   ;Untrigger
G4 P500      ;Wait for 500ms
```

Reference: https://blog.prusaprinters.org/how-to-make-3d-print-time-lapses-with-your-smartphone-camera_29790/

# Sending Messages to the User to Set The Pressure Regulator from the GCODE:

Use [M0], as follows:

```
M0 Set the pressure to 29.92 inches of mercury
```

# Using Unified Bed Leveling

This build of Marlin enables [Unified Bed Leveling]. The bed leveling routine can be triggered by the user from the LCD menu. The mesh is then saved to the EEPROM for use in the next print. In the start GCODE for prints, the following commands should be used instead of `G29`:

```
G28 ; home all axes
G29 L1 ; load leveling matrix slot 1
G29 A ; ensure mesh is enabled
```

# License (from Marlin)

Marlin is published under the [GPL license](/LICENSE) because we believe in open development. The GPL comes with both rights and obligations. Whether you use Marlin firmware as the driver for your open or closed-source product, you must keep Marlin open, and you must provide your compatible Marlin source code to end users upon request. The most straightforward way to comply with the Marlin license is to make a fork of Marlin on Github, perform your modifications, and direct users to your modified fork.

While we can't prevent the use of this code in products (3D printers, CNC, etc.) that are closed source or crippled by a patent, we would prefer that you choose another firmware or, better yet, make your own.

[logo]: https://github.com/marcio-cp/cocoa-press-marlin/raw/master/artwork/cp-logo-small.jpg "Cocoa Press Logo"
[Cocoa Press]: https://www.cocoapress.com
[this guide]: https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/
[GitHub repo]: https://github.com/marcio-cp/cocoa-press-marlin
[M1]:http://marlinfw.org/docs/gcode/M000-M001.html
[Unified Bed Leveling]:https://marlinfw.org/docs/features/unified_bed_leveling.html
