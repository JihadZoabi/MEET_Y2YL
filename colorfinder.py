import cv2 as cv
import numpy as np
import webcolors


def rgb2hex(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    return "{:02x}{:02x}{:02x}".format(r, g, b)


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    return tuple(reversed(tuple(colors[count.argmax()])))


def color_pic(pic):
    tpl = unique_count_app(pic)
    actual_name, closest_name = get_colour_name(tpl)
    if actual_name:
        return actual_name, rgb2hex(tpl)
    return closest_name, rgb2hex(tpl)
