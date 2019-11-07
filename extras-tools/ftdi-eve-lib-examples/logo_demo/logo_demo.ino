/*****************
 * logo_demo.ino *
 *****************/

/****************************************************************************
 *   Written By Marcio Teixeira 2019 - Aleph Objects, Inc.                  *
 *                                                                          *
 *   This program is free software: you can redistribute it and/or modify   *
 *   it under the terms of the GNU General Public License as published by   *
 *   the Free Software Foundation, either version 3 of the License, or      *
 *   (at your option) any later version.                                    *
 *                                                                          *
 *   This program is distributed in the hope that it will be useful,        *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
 *   GNU General Public License for more details.                           *
 *                                                                          *
 *   To view a copy of the GNU General Public License, go to the following  *
 *   location: <http://www.gnu.org/licenses/>.                              *
 ****************************************************************************/

// Edit configuration in "src/config.h"

#include "src/ftdi_eve_lib/ftdi_eve_lib.h"
#include "src/ftdi_eve_lib/extras/poly_ui.h"
#include "src/Cocoa_Press_Logo_Landscape.h"

using namespace FTDI;

/***************** SCREEN DEFINITIONS *****************/

class LogoScreen : public UIScreen, public UncachedScreen {
  public:

    static void onRedraw(draw_mode_t what) {
      CommandProcessor cmd;
      cmd.cmd(CLEAR_COLOR_RGB(LOGO_BACKGROUND));
      cmd.cmd(CLEAR(true,true,true));

      #define POLY(A) PolyUI::poly_reader_t(A, sizeof(A)/sizeof(A[0]))
      #define LOGO_PAINT_PATH(rgb, path) cmd.cmd(COLOR_RGB(rgb)); ui.fill(POLY(path));
      PolyUI ui(cmd);
      
      LOGO_PAINT_PATHS
    }
};

/***************** LIST OF SCREENS *****************/

SCREEN_TABLE {
  DECL_SCREEN(LogoScreen),
};
SCREEN_TABLE_POST

/***************** MAIN PROGRAM *****************/

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
  EventLoop::setup();
  CLCD::turn_on_backlight();
  SoundPlayer::set_volume(255);
}

void loop() {
  EventLoop::loop();
}
