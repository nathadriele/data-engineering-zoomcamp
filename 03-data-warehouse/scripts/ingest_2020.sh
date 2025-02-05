#!/usr/bin/env bash

args=""
for ((month = 1; month <= 12; month++)); do
  args+="--month $month "
done

for ((year = 2019; year <= 2021; year++)); do
  args+="--year $year "
done

for color in "green" "yellow"; do
  args+="--color $color "
done
