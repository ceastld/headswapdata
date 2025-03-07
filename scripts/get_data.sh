#!/bin/bash

id="$1"

mkdir -p hanhai22/$id

cp -r output/$id/gaussian/seg_masks hanhai22/$id
cp -r output/$id/gaussian/head_mask hanhai22/$id
cp -r output/$id/gaussian/skin_mask hanhai22/$id
cp output/$id/gaussian/debug/face_crop.mp4 hanhai22/$id
