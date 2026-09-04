#!/usr/bin/env bash

if ! [[ -d manual_mio_samwell ]] ; then
  echo "directory manual_mio_samwell does not exist. Did you run the setup script?"
  exit 1
fi

if [[ -d manual_mio_samwell/data ]] ; then
  rm -r manual_mio_samwell/data
fi
mkdir manual_mio_samwell/data

python tomo.py world.json manual_mio_samwell/data
cp fixed_data/* manual_mio_samwell/data/

if [[ -f manual_mio_samwell.apworld ]] ; then
  rm manual_mio_samwell.apworld
fi
zip -rq manual_mio_samwell.apworld manual_mio_samwell/*

if [[ -n "$1" ]] ; then
  echo "Installing to $1"
  cp manual_mio_samwell.apworld "$1"
fi
