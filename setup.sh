#!/usr/bin/env bash

if ! [[ -r "$1" ]] ; then
  echo "Please provide a path to a valid manual apworld"
  exit 1
fi

if [[ -d manual_mio_samwell ]] ; then
  rm -r manual_mio_samwell
fi

unzip -q $1 -d tempTEMPtemp
mv tempTEMPtemp/* ./manual_mio_samwell
rm -r tempTEMPtemp
