from PIL import Image
import subprocess
import os

def heat_map(img):
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            intensity = (r + g + b) // 3

            if intensity < 80:
                new_pixel = (0, 0, 255)
            elif intensity < 160:
                new_pixel = (255, 255, 0)
            else:
                new_pixel = (255, 0, 0)

            pixels[x, y] = new_pixel


print("Task Coding Begins")

# mkdir filtered_images
subprocess.run(["mkdir", "-p", "filtered_images"])

# cd ./images
os.chdir("./images")

# pwd
folder_path = subprocess.run(
    ["pwd"],
    capture_output=True,
    text=True
).stdout.strip()

print(folder_path)

# find . -name "*.jpg"
jpgs_list = subprocess.run(
    ["find", ".", "-name", "*.jpg"],
    capture_output=True,
    text=True
).stdout
# note this step can also be done by doing ls and then just filtering out based on file endings

print(jpgs_list)

# ls
directory_list = subprocess.run(
    ["ls"],
    capture_output=True,
    text=True
).stdout

images = jpgs_list.splitlines()
all_files = directory_list.splitlines()

imgs_width_sum = 0
imgs_height_sum = 0
img_files_processed = 0

for img_name in images:
    file_path = os.path.join(folder_path, img_name[2:])   # remove "./"
    print(file_path)
    img = Image.open(file_path).convert("RGB")
    heat_map(img)
    imgs_width_sum += img.width
    imgs_height_sum += img.height
    out_path = os.path.join("..", "filtered_images", img_name[2:])
    print(out_path)
    img.save(out_path)
    img_files_processed += 1


tot_files = len(all_files)
skipped = tot_files - img_files_processed

avg_width = imgs_width_sum / img_files_processed
avg_height = imgs_height_sum / img_files_processed

report_str = (
    "Image Processing Report\n"
    "==========================\n"
    "Total files found: %d\n"
    "Image files processed: %d\n"
    "Files skipped: %d\n"
    "Average image width: %.2f\n"
    "Average image height: %.2f\n"
) % (
    tot_files,
    img_files_processed,
    skipped,
    avg_width,
    avg_height,
)

print(report_str)

# Back to parent directory
os.chdir("..")

# Write report
with open("report.txt", "w") as f:
    f.write(report_str)