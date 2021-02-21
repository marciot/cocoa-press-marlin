/************************************
 * cocoa_press_unload_cartridge.cpp *
 ************************************/

/****************************************************************************
 *   Written By Mark Pelletier  2017 - Aleph Objects, Inc.                  *
 *   Written By Marcio Teixeira 2018 - Aleph Objects, Inc.                  *
 *   Written By Marcio Teixeira 2020 - Cocoa Press                          *
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
 *   location: <https://www.gnu.org/licenses/>.                              *
 ****************************************************************************/

#include "../config.h"
#include "screens.h"
#include "screen_data.h"

#ifdef FTDI_COCOA_LOAD_CHOCOLATE_SCREEN

using namespace ExtUI;
using namespace FTDI;
using namespace Theme;

#define GRID_COLS 2
#define GRID_ROWS 7

#define TITLE_POS             BTN_POS(1,1), BTN_SIZE(2,1)
#define DESCRIPTION_POS       BTN_POS(1,2), BTN_SIZE(2,3)
#define CARTRIDGE_OUT_BTN_POS BTN_POS(1,5), BTN_SIZE(1,1)
#define CARTRIDGE_IN_BTN_POS  BTN_POS(2,5), BTN_SIZE(1,1)
#define EXTRUDE_BTN_POS       BTN_POS(1,6), BTN_SIZE(1,1)
#define RETRACT_BTN_POS       BTN_POS(2,6), BTN_SIZE(1,1)
#define BACK_BTN_POS          BTN_POS(1,7), BTN_SIZE(2,1)

void LoadChocolate::onEntry() {
  screen_data.LoadChocolate.repeat_tag = 0;
}

void LoadChocolate::onRedraw(draw_mode_t what) {
  CommandProcessor cmd;

  if (what & BACKGROUND) {
    cmd.cmd(CLEAR_COLOR_RGB(bg_color))
       .cmd(CLEAR(true,true,true))
       .cmd(COLOR_RGB(bg_text_enabled))
       .tag(0)
       .font(font_large)
       .text(TITLE_POS, GET_TEXT_F(MSG_LOAD_CHOCOLATE));
       draw_text_box(cmd, DESCRIPTION_POS, F(
        "Drop your chocolate refill into the cartridge. "
        "Press and hold the Cartridge Out button until "
        "the plunger adapter is visible at the bottom of "
        "the extruder. Securely attach a red plunger to "
        "the plunger adapter and load the cartridge onto "
        "the plunger. Press and hold Cartridge In button "
        "until cartridge is fully loaded into the extruder, "
        "and use the buttons to help follow the locking path "
        "to lock"),
        OPT_CENTERY, font_medium);
  }

  if (what & FOREGROUND) {
    #define TOG_STYLE(A) colors(A ? action_btn : normal_btn)
    const bool tog2 = screen_data.LoadChocolate.repeat_tag == 2;
    const bool tog3 = screen_data.LoadChocolate.repeat_tag == 3;

    cmd.font(font_medium)
       .tag(2).TOG_STYLE(tog3   ).button(CARTRIDGE_OUT_BTN_POS, GET_TEXT_F(MSG_CARTRIDGE_OUT))
       .tag(3).TOG_STYLE(tog2   ).button(CARTRIDGE_IN_BTN_POS,  GET_TEXT_F(MSG_CARTRIDGE_IN))
       .tag(4)                   .button(EXTRUDE_BTN_POS,       GET_TEXT_F(MSG_LOAD_FILAMENT))
       .tag(5).colors(normal_btn).button(RETRACT_BTN_POS,       GET_TEXT_F(MSG_UNLOAD_FILAMENT))

       .tag(1).colors(action_btn).button(BACK_BTN_POS,          GET_TEXT_F(MSG_BACK));
  }
}

bool LoadChocolate::onTouchStart(uint8_t tag) {
    screen_data.LoadChocolate.repeat_tag = 0;
    return true;
}

bool LoadChocolate::onTouchEnd(uint8_t tag) {
  using namespace ExtUI;
  switch (tag) {
    case 2:
      screen_data.LoadChocolate.repeat_tag = (screen_data.LoadChocolate.repeat_tag == 2) ? 0 : 2;
      break;
    case 3:
      screen_data.LoadChocolate.repeat_tag = (screen_data.LoadChocolate.repeat_tag == 3) ? 0 : 3;
      break;
    case 1: GOTO_PREVIOUS(); break;
  }
  return true;
}

bool LoadChocolate::onTouchHeld(uint8_t tag) {
  if (ExtUI::isMoving()) return false; // Don't allow moves to accumulate
  constexpr float increment = 0.25;
  MoveAxisScreen::setManualFeedrate(E0, increment);
  #define UI_INCREMENT_AXIS(axis) UI_INCREMENT(AxisPosition_mm, axis);
  #define UI_DECREMENT_AXIS(axis) UI_DECREMENT(AxisPosition_mm, axis);
  switch (tag) {
    case 2:
        if(get_chocolate_fill_level() < 0.1) {
            screen_data.LoadChocolate.repeat_tag = 0;
            return false;
        }
        UI_INCREMENT_AXIS(E0);
        break;
    case 3:
        if(get_chocolate_fill_level() > 0.9) {
            screen_data.LoadChocolate.repeat_tag = 0;
            return false;
        }
        UI_DECREMENT_AXIS(E0);
        break;
    case 4:
        UI_INCREMENT_AXIS(E0);
        break;
    case 5:
        UI_DECREMENT_AXIS(E0);
        break;
    default: return false;
  }
  #undef UI_DECREMENT_AXIS
  #undef UI_INCREMENT_AXIS
  return false;
}

void LoadChocolate::onIdle() {
  reset_menu_timeout();
  if (screen_data.LoadChocolate.repeat_tag) onTouchHeld(screen_data.LoadChocolate.repeat_tag);
  BaseScreen::onIdle();
}
#endif // FTDI_COCOA_LOAD_CHOCOLATE_SCREEN
