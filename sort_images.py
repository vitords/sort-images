import os
import os.path
import shutil
import exifread

# Path for sorted files to be stored
# If it doesn't exist, creates a new one
dirs_path = "D:\\Sorted\\"
if not os.path.exists(dirs_path):
	os.mkdir(dirs_path)

# Where images to be organized are located
images_path = "D:\\Recovered\\"

fail_count = 0
success_count = 0

# Recursively walk through all subdirectories and store the path + name of the jpg images
images = []
for root, dirs, files in os.walk(images_path):
	for f in files:
		# I'm only interested in pictures
		if f.endswith(".jpg"):
			images.append(os.path.join(root, f))

# Extracts the date an image was taken and moves it to a folder with the format YYYY.MM.DD
# If the image doesn't have EXIF tags, sends it to a folder named 0000
for img in images:
	with open(img, "rb") as file:
		tags = exifread.process_file(file, details=False, stop_tag="DateTimeOriginal")
		try:
			date_path = str(tags["EXIF DateTimeOriginal"])[:10].replace(":", ".")
			success_count += 1
		except:
			print(str(img) + " does not have EXIF tags.")
			fail_count += 1
			date_path = "0000"
		if not os.path.exists(dirs_path + date_path):
			os.mkdir(dirs_path + date_path)
	# Second parameter is specific to my situation and must be changed...
	# In my case, the image name (including ".jpg") only used the last 12 chars of the string
	shutil.move(img, dirs_path + date_path + "\\" + img[-12:])

print("Sorted " + str(success_count) + " files.") # Images properly sorted by date taken
print("Failed to sort " + str(fail_count) + " files.") # Images sent to 0000
