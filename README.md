# Random Image Rumble

## Overview

Welcome to the Random Image Rumble! This simple Python program presents a canvas of images randomly chosen from your picture stash (edit the variable `images_directory` to point it to the desired location), allowing you to judge and rank them against each other. Simply enter your rankings into the entry box from best to worst then click submit, and the ratings of the images will be swapped to match your ranking order. Images that don't have a rating will be initialized with a random rating to start with.


## Peculiarities (DEFINITELY READ THIS BEFORE TRYING TO USE!)

- Expects to be pointed to a directory containing JPEG-XL files and/or subdirectories containing JPEG-XL files.
- Utilizes `djxl` (expects it to be installed) to create temporary JPEG copies of the JPEG-XL files to be loaded for the current round.
- Terminating the program without using the QUIT button will result in the current round's temporary JPEG files not being cleaned up.
- Expects image filenames to be 32 characters long (not counting the file extension).
- Does NOT read/write EXIF metadata, sad but true. Writes and reads the rating value to/from the 4th character (index 3) of the filename, for some reason!
- In cases of filename conflicts, it tries randomly changing characters in index positions 29-31 until it finds a unique name.
- Treats filename character index range 4-9 as a Base-36 counter for the number of other images that the image has been rated against over the course of its matches. No checks are performed for non-alphanumeric characters in these positions.
- The code is a *very* hot mess, as my only Python experience outside of this 2-day ChatGPT-assisted project was a high school game design class back in 2008. Use at your own risk, lmao

## Niceties

- Checks for the existence of a sidecar file and renames it when renaming image files.
- For fast one-handed rating, the tab key can be used to submit rankings and advance to the next round.

## Usage

1. Make sure to edit the `images_directory` variable to point to your desired image location.
2. Run the program.
3. Judge and rank images in each round.
4. Use the QUIT button or the Escape key to terminate the program and clean up temporary files.

Enjoy the Random Image Rumble!
