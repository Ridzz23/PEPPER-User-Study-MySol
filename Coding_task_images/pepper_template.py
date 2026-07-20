#to run: pyExt <file_name>


from PIL import Image

def heat_map(folder_in, folder_out, img_name):
    if img_name == "": #to get rid of last extra newline
        return 0,0
    file_in = folder_in + img_name[1::]
    file_out = folder_out + img_name[1::]
    img = Image.open(file_in).convert("RGB")
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
            img.save(file_out)
    
    return img.width, img.height



#------------------------------ START CODING FROM HERE; DO NOT CHANGE THE CODE ABOVE THIS LINE ------------------------------



#TODO 1: create a new directory called filtered_images (FS)

#TODO 2: enter into the existing images folder (FS)

#TODO 3: find all the files that end with .jpg in the images folder and create a python list of all the file names (DATA)


folder_images_path = pwd
folder_images_path = folder_images_path.replace("\n", "")

folder_filtered_images_path = "./filtered_images"


#TODO 4: iterate through the list of filenames and for each image apply the heat_map filter. also keep track of the running sum of img widths and heights and num_img_files_processed. (DATA)
imgs_height_sum = 0
imgs_width_sum = 0
num_img_files_processed = 0

# TO USE THE HEATMAP FUNCTION - given the file name, this calls the function for that 1 image and returns its height and width:
# img_width, img_height = heat_map(folder_images_path, folder_filtered_images_path, img_file)



#------------------------------ REPORT GENERATION ------------------------------

#TODO 5: calculate the total number of files in the images folder and the average width of all jpg image files. (DATA)
tot_files = 0 #TODO
skipped = tot_files - num_img_files_processed
if(num_img_files_processed != 0):
    avg_height = imgs_height_sum / num_img_files_processed
    avg_width = 0 #TODO
else:
    avg_height = 0
    avg_width = 0

report_str = "'Image Processing Report \n ==========================\n Total files found: %d \n Image files processed: %d \n files skipped: %d \n Average image width: %.2f  \n Average image height: %.2f\n'" % (tot_files, num_img_files_processed, skipped, avg_width, avg_height)

#TODO 6: Write report_str to the file report.txt. The file report.txt should be located outside the images folder and should be directly under the Coding_task_images folder. (FS)






