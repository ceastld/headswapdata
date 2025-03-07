mkdir -p hanhai22/body_track
for id in 9 13 28; do
    cp "output/HSID${id}/gaussian/body_track/smplx_track.pth" "hanhai22/body_track/HSID${id}.pth"
done
