import sys
import os

raw_input = open(os.path.join(sys.path[0], 'input')).read()

width = 25
height = 6
pixels_in_layer = (width * height)

pixels = list(raw_input)
pixels_by_layer = [pixels[layer_start:layer_start + pixels_in_layer] for layer_start in range(0, len(pixels), pixels_in_layer)]

def get_first_not_transparent_pixel_value(pixel_index):
    for layer in pixels_by_layer:
        if layer[pixel_index] != '2':
            return layer[pixel_index]

composit_layer = [2 for _ in range(pixels_in_layer)]
for pixel_index in range(pixels_in_layer):
    composit_layer[pixel_index] = get_first_not_transparent_pixel_value(pixel_index)

composit_flattened_image = ''.join(composit_layer)

print(composit_flattened_image)

for row in range(height):
    offset = row * width
    print(composit_flattened_image[offset : offset + width])