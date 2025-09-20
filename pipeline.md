INPUT: image, RED_SQUARE_SIDE_CM

# 1) normalize & deskew card
img ← load(image)
img ← denoise_lightly(img)                     # bilateral/median
img ← white_balance_grayworld(img)             # or PlantCV: rgb2gray + balance
card_mask ← find_largest_light_rectangle(img)  # threshold on L channel; keep rectangular contour
img ← crop_to_mask(img, card_mask, pad=2%)

# 2) detect red control square + scale
hsv ← toHSV(img)
red_mask ← inRange(hsv, red_low1..red_high1) ∪ inRange(hsv, red_low2..red_high2)
red_mask ← morphology_close_then_open(red_mask, k=3–5)
red_contours ← find_contours(red_mask)
red_sq ← choose_contour_by: area largest & aspect≈1 & solidity>0.95
if not found → FAIL("no red square")

# optional perspective rectification using the square
corners_px ← minAreaRectCorners(red_sq)
H ← homography_map_quad_to_square(corners_px, size=nominal_px)
img ← warpPerspective(img, H)                  # fronto-parallel
recompute hsv, red_mask, red_sq on rectified img (cheap redo)

# pixel scale
side_px ← mean_side_length(minAreaRect(red_sq))
px_per_cm ← side_px / RED_SQUARE_SIDE_CM
px_per_cm2 ← px_per_cm^2

# 3) mask nuisances (square + label strip)
nuisance_mask ← dilate(mask_of(red_sq), k=7)   # exclude the red square region
label_roi ← horizontal_strip(top=0%, height=15–20%)  # where handwriting sits
nuisance_mask ← nuisance_mask ∪ label_roi

# 4) leaf segmentation (color-index + adaptive backup)
# A) vegetation index path (works for green-ish material)
exg ← 2*G - R - B                              # or PlantCV: color_correction + vegetation_index
veg_mask ← threshold_otsu(exg)                 # high values = leaf
# B) reflectance-invariant backup
lab ← toLab(img)
a_chan ← lab.a                                 # green↔red axis
leaf_mask2 ← adaptive_threshold(a_chan, block=51, C=−2)  # select greener than bg
leaf_mask ← (veg_mask ∩ leaf_mask2) \ nuisance_mask

# 5) mask cleanup & choose object
leaf_mask ← fill_holes(leaf_mask)
leaf_mask ← morphology_open_then_close(leaf_mask, k=5)
leaf_mask ← remove_small_particles(leaf_mask, min_area=0.002 * image_area)
roi_above_square ← rectangle_above(red_sq, margin=5% image height)
leaf_mask ← leaf_mask ∩ roi_above_square       # avoids grabbing the square, tape, shadows
leaf_objs ← connected_components(leaf_mask)
leaf ← pick_component(leaf_objs) by:
        - largest area
        - centroid y above red_sq.center.y
        - elongation < 10 (reject hairlines/tape)

if none → FAIL("no leaf object")

# 6) compute area
area_px ← pixel_count(leaf)
area_cm2 ← area_px / px_per_cm2

# 7) QC & outputs
qc.aspect_square ← min(side_px)/max(side_px)   # ~1 if square was good
qc.border_touch ← fraction_of_leaf_touching_image_border(leaf)  # should be ~0
qc.blob_solidity ← solidity(leaf)              # very low may indicate holes/glare
if any qc outside thresholds → FLAG("review")

save_overlay ← draw_outlines(img, [leaf, red_sq])
OUTPUT: area_cm2, px_per_cm, qc, overlay_image
