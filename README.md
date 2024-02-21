# Random Image Rumble

## Overview

Welcome to the Random Image Rumble! This simple Python program provides a unique gamified approach to rating your images by presenting you with a canvas of between 2-4 images randomly chosen from your picture stash (edit the variable `images_directory` to point it to the desired location), where you then rank them against each other and the program automatically adjusts their rating metadata behind the scenes to reflect how they've fared in their matchups.


## Peculiarities (DEFINITELY READ THIS BEFORE TRYING TO USE!)

**TL;DR essentials for getting started:** This program only looks for **JPEG-XL** files in the directory (and any subdirectories) specified with the `images_directory` variable, and these JXL files should have filenames that are at least 32 characters in length (not counting the file extension)... ideally without any non-alphanumeric characters. Requires `libjxl` and `exiftool`, linked here:
https://github.com/libjxl/libjxl
https://www.exiftool.org

- Expects to be pointed to a directory containing JPEG-XL files and/or subdirectories containing JPEG-XL files.
- Utilizes `djxl` (expects it to be installed) to create temporary JPEG copies of the JPEG-XL files to be loaded for the current round.
- Terminating the program without using the QUIT button will result in the current round's temporary JPEG files not being cleaned up.
- Expects image filenames to be *at least* 32 characters long (not counting the file extension).
- ~~Does NOT read/write EXIF metadata, sad but true.~~ Uses `exiftool` to write the ratings to the image's metadata (and sidecar, if present). It also writes the rating value to the 4th character (index 3) of the filename, and this is also where the program reads the rating from.
- In cases of filename conflicts, it tries randomly changing characters in index positions 29-31 until it finds a unique name.
- Treats filename character index range 4-9 as a Base-36 counter for the number of other images that the image has been rated against over the course of its matches. No checks are performed for non-alphanumeric characters in these positions.
- The code is a *very* hot mess, as my only Python experience outside of this 2-day ChatGPT-assisted project was a high school game design class back in 2008. It seems to work fine in my testing on both Windows and Mac, but clearly it's heavily tuned to my specific whims. Use at your own risk, lmao

## Usage

1. Make sure to edit the `images_directory` variable to point to your desired image location. You may also edit the width and height of the window to best suit your display.
2. Run the program: `python Random_Image_Rumble.py`
3. Enter the image numbers into the text field in order from best to worst without any spaces, e.g. `1342`, then click Submit (you can also press Enter/Return or Tab to submit your rankings.) to confirm and advance to the next round with a new random selection of images.
4. Use the QUIT button or the Escape key to terminate the program and clean up temporary files.

Enjoy the Random Image Rumble!
