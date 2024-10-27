# Image Resizing and Format Conversion Script
Many datasets contain images of varying sizes, which can be inconvenient for preprocessing. This Python script addresses that issue by resizing images to a specified target size and converting their file format.

# Usage
To run the script, use the following command in the command line:
`python <path_to_script> <source_folder> <destination_folder> <target_width> <target_height> <target_extension> <additional options>`

If the destination folder does not exist, the script will create it. If an image with the same name already exists in the destination folder, it will be overwritten.

# Additional options

- **Color mode** - changes color mode of the image to one of the supported by PIL `.convert()` method. All options: `-L`, `-1`, `-P`, `-RGB`, `-RGBA`, `-CMYK`, `-YCbCr`, `-HSV`, `-LAB`, `-F`, `-I`, `-I;16`, `-I;16B`, `-I;16L`, `-I;32`, `-I;32B`, `-I;32L`, `-I;16U`.
- `-C`, `--color` -  sets a custom background color by specifying three RGB integers (0–255) following the option. Example: `-C 255 0 0` - changes bacground color to red.
- `-P`, `--proportions` -  resizes the image by changing its proportions directly instead of adding a background.








