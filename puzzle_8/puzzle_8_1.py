import sys
import os


raw_input = open(os.path.join(sys.path[0], 'input')).read()

width = 25
height = 6
pixels_in_layer = (width * height)

pixels = list(raw_input)
pixels_by_layer = [pixels[layer_start:layer_start + pixels_in_layer] for layer_start in range(0, len(pixels), pixels_in_layer)]

layer_with_least_zeros = min(pixels_by_layer, key=lambda p: p.count('0'))

ones_in_control_layer = layer_with_least_zeros.count('1')
twos_in_control_layer = layer_with_least_zeros.count('2')

print(ones_in_control_layer * twos_in_control_layer)