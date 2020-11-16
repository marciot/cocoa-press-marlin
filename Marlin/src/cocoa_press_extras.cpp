/******************************
 * cocoa_press_extras.cpp *
 ******************************/

/****************************************************************************
 *   Written By Marcio Teixeira 2020                                        *
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

#include "MarlinCore.h"

#include "cocoa_press_extras.h"

/**************************** EXTRA HEATER CHECK ****************************/

#if ENABLED(COCOA_PRESS_EXTRA_HEATER)

bool extra_heater_installed;

void check_extra_heater() {        
  extra_heater_installed = analogRead(TEMP_2_PIN) < 1010;
}

bool has_extra_heater() {
  return extra_heater_installed;
}
#endif