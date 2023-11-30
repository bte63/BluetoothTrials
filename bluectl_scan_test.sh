#!/bin/bash

readOutput() {
    echo "$(cat $TEMP/bluetoothctl.out | sed 's/\x1B\[[0-9;]\{1,\}[A-Za-z]//g'"
}

executeCommandInExistingProcess() {
  if [ -z "$(pidof bluetoothctl)" ]
  then
    exit -1
  else
    echo "$1" >&/proc/$(pidof bluetoothctl)/fd/0
  fi
}

startParallelProcess() {
  output="$TEMP/bluetoothctl.out"
  
  if [ ! -z "$(pidof bluetoothctl)" ]
  then
    echo "Bluetooth process is running..."
    exit -1
  fi
  
  if [ -f "$output" ]
  then
    rm $output
  fi

  coproc bctl { bluetoothctl > $output; }
  [ "$#" -ge 1 -a ! -z "$1" ] && executeCommandInExistingProcess "$1"

  sleep 30

  if [ ! -z $(pidof bluetoothctl) ]
  then
    [ "$#" -ge 2 -a ! -z "$2" ] && executeCommandInExistingProcess "$2"
    executeCommandInExistingProcess "quit"
  fi
}