/**
 * Marlin 3D Printer Firmware
 * Copyright (C) 2019 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * Based on Sprinter and grbl.
 * Copyright (C) 2011 Camiel Gubbels / Erik van der Zalm
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
#pragma once

// R25 = 100 kOhm, beta25 = 4092 K, 4.7 kOhm pull-up, bed thermistor

// Custom Cocoa Press thermistor table, based on thermistor table 1
//multiplied by 10 for 10th degree accuracy
const short temptable_999[][2] PROGMEM = {
{ OV(2),   2750},
{OV(11),   1750},
{OV(21),   1450},
{OV(31),   1300},
{OV(40),   1200},
{OV(60),   1050},
{OV(93),    900},
{OV(145),   750},
{OV(305),   500},
{OV(351),   450},
{OV(402),   400},
{OV(515),   300},
{OV(575),   250},
{OV(635),   200},
{OV(693),   150},
{OV(749),   100},
{OV(799),     5},
{OV(845),     0},
{OV(1024),   -5}};
