# to run: pyExt <file_name>

from PIL import Image


# ---------------- Python Functions ----------------
def heat_map(folder_in, folder_out, img_name):
    """
    Applies a simple heat-map filter to a JPEG image.

    Input:
    - folder_in: directory containing the original images
    - folder_out: directory where the processed images are saved
    - img_name: image filename

    The filter recolors each pixel based on its intensity:
    - dark pixels    -> blue
    - medium pixels  -> yellow
    - bright pixels  -> red

    Returns:
    - image width
    - image height
    """

    file_in = folder_in + img_name[1:]
    file_out = folder_out + img_name[1:]

    img = Image.open(file_in).convert("RGB")
    
    pixels = img.load()

    for y in range(img.height):

        for x in range(img.width):

            r, g, b = pixels[x, y]

            intensity = (r + g + b) // 3

            if intensity < 80:
                new_pixel = (0, 0, 255)        # blue

            elif intensity < 160:
                new_pixel = (255, 255, 0)      # yellow

            else:
                new_pixel = (255, 0, 0)        # red

            pixels[x, y] = new_pixel

    img.save(file_out)

    return img.width, img.height


# ---------------- START CODING FROM HERE; DO NOT CHANGE THE CODE ABOVE THIS LINE ----------------


# TODO 1: create a new directory called filtered_images (FS)

mkdir "filtered_images"


# TODO 2: set working directory to images folder (FS)

cd "./images"


# TODO 3: find all the files that end with .jpg in the images folder
# and store it in a python variable called images (it should be a list).
# Similarly store a list of all the files in the directory in a python variable called all_files.
# (FS)
#
# Example file path:
# ./images/example.jpg

images = find "." -name '*.jpg'
print(images)
all_files = ls
print(all_files)
# TODO 4: iterate through the list of filenames and apply the heat_map
# filter to each image.
#
# Also keep track of:
# - total image widths
# - total image heights
# - number of image files processed (FS)

folder_images_path = pwd

folder_images_path = folder_images_path.replace(
    "\n",
    ""
)

folder_filtered_images_path = "./filtered_images"

imgs_height_sum = 0
imgs_width_sum = 0

num_img_files_processed = 0

for img_file in images:

    img_width, img_height = heat_map(
        folder_images_path,
        folder_filtered_images_path,
        img_file
    )

    if(img_width != 0 and img_height != 0):
        num_img_files_processed += 1
        imgs_width_sum += img_width
        imgs_height_sum += img_height

# To apply the heat-map filter to a single image:
#
# img_width, img_height = heat_map(
#     folder_images_path,
#     folder_filtered_images_path,
#     <file_path>
# )


# ---------------- Report Generation ----------------


# TODO 5: Calculate the total number of files in the images folder
# and then write report_str to the file report.txt.
#
# The file report.txt should be located outside the images folder
# and should be directly under the Coding_task_images folder. (FS)

tot_files = len(all_files)

skipped = tot_files - num_img_files_processed

if num_img_files_processed != 0:

    avg_height = (
        imgs_height_sum /
        num_img_files_processed
    )

    avg_width = (
        imgs_width_sum /
        num_img_files_processed
    )

else:

    avg_height = 0
    avg_width = 0


report_str = (
    "'Image Processing Report \n"
    "==========================\n"
    "Total files found: %d \n"
    "Image files processed: %d \n"
    "Files skipped: %d \n"
    "Average image width: %.2f \n"
    "Average image height: %.2f\n'"
) % (
    tot_files,
    num_img_files_processed,
    skipped,
    avg_width,
    avg_height,
)

cd ".."
echo report_str $> "report.txt"