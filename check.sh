#!/bin/bash

yelp-check ids gnome-help/C | \
grep . && echo 'yelp-check ids: FAIL' && exit 1 || \
echo 'yelp-check ids: PASS'

yelp-check validate gnome-help/C | \
grep . && echo 'yelp-check validate: FAIL' && exit 1 || \
echo 'yelp-check validate: PASS'
