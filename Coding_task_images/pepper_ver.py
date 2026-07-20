#to run: /Users/ridhisrikanth/Documents/GitHub/python-shell-DSL/python.exe
# Given a folder of images, find all images with .jpg ending
# apply the heat map on them and save to output dir
# write a report at the end and save to the file

#PEPPER work here: reading folders and files, filtering out some files, creating new folders and files and writing to new files

from PIL import Image

def heat_map(img):
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            intensity = (r + g + b) // 3

            if intensity < 80:
                new_pixel = (0, 0, 255)       # blue
            elif intensity < 160:
                new_pixel = (255, 255, 0)     # yellow
            else:
                new_pixel = (255, 0, 0)       # red

            pixels[x, y] = new_pixel

#CODE HERE

#fill in 1: create a new directory called filtered_images
mkdir "filtered_images"
#1

#2: enter into the existing images folder
cd "./images"

#2

#3: find all the files that end with .jpg in the images folder and create a python list of all the file names
jpgs_list = find "." -name '*.jpg'
print(jpgs_list)

directory_list = ls

images = jpgs_list.split("\n") 
all_files = directory_list.split("\n")

#3

folder_path = pwd
folder_path = folder_path.replace("\n", "")

imgs_width_sum = 0
imgs_height_sum = 0
img_files_processed = 0
for img_name in images:
    if img_name == "": #to get rid of last extra newline
        continue
    #make some of this stuff a function to make it easier
    #4: create the complete read file path and out file path as a string 
    file_path = folder_path + img_name[1::]
    print(file_path)
    img = Image.open(file_path).convert("RGB")
    heat_map(img)
    imgs_width_sum += img.width
    imgs_height_sum += img.height
    out_path = "./filtered_images" + img_name[1::]
    print(out_path)
    #4

    img.save(out_path)
    img_files_processed += 1


tot_files = len(all_files)
skipped = tot_files - img_files_processed
avg_width = imgs_width_sum / img_files_processed
avg_height = imgs_height_sum / img_files_processed

report_str = "'Image Processing Report \n ==========================\n Total files found: %d \n Image files processed: %d \n files skipped: %d \n Average image width: %.2f  \n Average image height: %.2f\n'" % (tot_files, img_files_processed, skipped, avg_width, avg_height)
print(report_str)


cd ".."

#5: write a report to the file report.txt

echo report_str $> "report.txt"






