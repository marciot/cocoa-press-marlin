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

fetch_default_config() {
    CONF_URL=https://raw.githubusercontent.com/MarlinFirmware/Configurations/bugfix-2.0.x/config/default
    CONF_DIR=../../default
    (wget $CONF_URL/Configuration.h -O $CONF_DIR/Configuration.h &&
    wget $CONF_URL/Configuration_adv.h -O $CONF_DIR/Configuration_adv.h &&
    cat  $CONF_DIR/Configuration_CocoaPress.h >> $CONF_DIR/Configuration.h) ||
    exit 1
}

build_config() {
  group=$1
  printer_name=$2
  toolhead_name=$3

  echo ${group}/${printer_name}/${toolhead_name}
  ./build-config.py $printer_name $toolhead_name -D ${group}/${printer_name}/${toolhead_name} --summary
}

if [ "$1" = "upgrade" ]; then
  fetch_default_config || (echo Unable to retrieve new configuration files; exit 1)
else
  echo
  echo
  echo Using pre-existing config files. To update, use "./build-configs.sh upgrade"
  echo
  echo
fi

build_config standard CocoaPress_Archim                  CocoaPress_SingleExtruder