#!/bin/sh

####
# Portions copyright (C) 2019, Cocoa Press.
# Portions copyright (C) 2019, AlephObjects, Inc.
# Portions copyright (C) 2019, Marcio Teixeira
#
#
# The bash script in this page is free software: you can
# redistribute it and/or modify it under the terms of the GNU Affero
# General Public License (GNU AGPL) as published by the Free Software
# Foundation, either version 3 of the License, or (at your option)
# any later version.  The code is distributed WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU AGPL for more details.
#

build_config() {
  printer_name=$1
  toolhead_name=$2

  case "$printer_name" in
  *_Experimental)
    PREFIX=EXPERIMENTAL/
    ;;
  *)
    PREFIX=
    ;;
  esac

  ./build-config.py $1 $2 -D ${PREFIX}${printer_name}/${toolhead_name} --summary
}

build_config CocoaPress_Einsy                   CocoaPress_SingleExtruder
build_config CocoaPress_Archim                  CocoaPress_SingleExtruder
build_config CocoaPress_TouchDemo               CocoaPress_SingleExtruder