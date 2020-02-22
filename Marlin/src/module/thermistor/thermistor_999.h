/**
 * Marlin 3D Printer Firmware
 * Copyright (c) 2019 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * Based on Sprinter and grbl.
 * Copyright (c) 2011 Camiel Gubbels / Erik van der Zalm
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

// R25 = 100 kOhm, beta25/50 = 4250 K, 71.5 kOhm pull-up, bed thermistor

//https://www.digikey.com/product-detail/en/murata-electronics-north-america/NXFT15WF104FA1B025/490-11856-ND/5333691
//https://www.digikey.com/product-detail/en/murata-electronics/NXRT15WF104FA1B040/490-7169-ND/3900396


// Custom Cocoa Press thermistor table, based on thermistor table 1
//multiplied by 10 for 10th degree accuracy
const short temptable_999[][2] PROGMEM = {

  {OV(76),   1000},
  {OV(101),   900},
  {OV(135),   800},
  {OV(182),   700},
  {OV(244),   600},
  {OV(325),   500},
  {OV(372),    450},
  {OV(424),   400},
  {OV(435),   390},
  {OV(446),   380},
  {OV(457),   370},
  {OV(468),   360},
  {OV(480),   350},
  {OV(491),   340},
  {OV(503),   330},
  {OV(514),   320},
  {OV(526),     310},
  {OV(538),     300},
  {OV(550),     290},
  {OV(561),     280},
  {OV(573),     270},
  {OV(585),     260},
  {OV(597),     250},
  {OV(656),     200},
  {OV(713),     150},
  {OV(766),     100},
  {OV(858),     0},
  {OV(925),     -100}};

// {OV(302),   1000},
// {OV(403),   900},
// {OV(540),   800},
// {OV(727),   700},
// {OV(976),   600},
// {OV(1299),   500},
// {OV(1489),    450},
// {OV(1696),   400},
// {OV(1739),   390},
// {OV(1783),   380},
// {OV(1828),   370},
// {OV(1873),   360},
// {OV(1918),   350},
// {OV(1964),   340},
// {OV(2010),   330},
// {OV(2057),   320},
// {OV(2104),     310},
// {OV(2151),     300},
// {OV(2198),     290},
// {OV(2245),     280},
// {OV(2293),     270},
// {OV(2341),     260},
// {OV(2388),     250},
// {OV(2624),     200},
// {OV(2852),     150},
// {OV(3066),     100},
// {OV(3431),     0},
// {OV(3699),     -100}};


// { OV(2),   2750},
// {OV(11),   1750},
// {OV(21),   1450},
// {OV(31),   1300},
// {OV(40),   1200},
// {OV(60),   1050},
// {OV(93),    900},
// {OV(145),   750},
// {OV(305),   500},
// {OV(351),   450},
// {OV(402),   400},
// {OV(515),   300},
// {OV(575),   250},
// {OV(635),   200},
// {OV(693),   150},
// {OV(749),   100},
// {OV(799),     5},
// {OV(845),     0},
// {OV(1024),   -5}};
