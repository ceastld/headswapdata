ffmpeg -i test8.mp4 -i seg/HSID8/removed_w_mask_15.mp4 -filter_complex "hstack" test8_seg.mp4
