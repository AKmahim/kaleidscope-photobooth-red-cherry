import sys
import os, glob
import subprocess
import datetime 

# C:\Users\USER\Pictures\digiCamControl\Session1

# function for finding the latest image path
def get_latest_image_path():
    list_of_files = glob.glob('C:/Users/USER/Pictures/digiCamControl/Session1/*.JPG') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file.replace("\\", "/")

def func_TakeNikonPicture(input_filename="image.JPG"):
    camera_command = 'C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe'
    camera_command_details = 'C:/Users/USER/Desktop/mahim/kaleidscope-photobooth/removeBg_api_python/images/' + input_filename + ' /capture /iso 500 /shutter 1/30 /aperture 1.8'
    print('camera details = ',camera_command_details)
    full_command=camera_command + ' ' + camera_command_details
    p = subprocess.Popen(full_command, stdout=subprocess.PIPE, universal_newlines=True, shell=False)
    (output, err) = p.communicate()  

    #This makes the wait possible
    p_status = p.wait(1)
    # print(p.stdout.readline())

    #This will give you the output of the command being executed
    print('Command output: ' + str(output))
    print('Command err: ' + str(err))

    print('done')

    return get_latest_image_path()


# if(len(sys.argv) < 2):
#     rawimagename = 'test.jpg'
# else:   
#     # sys.argv[0] is the program name, sys.argv[1] is the first file, etc.
#     # need to shift this over
#     files = sys.argv[1:len(sys.argv)]
#     # Read the image
#     rawimagename = files[0]
#     if(os.path.isfile(rawimagename) is True):
#         print("File exists...not overwriting.")
#         sys.exit()

# # Store date/time for file uniqueness
# current_dt=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# print("Current date time = " + current_dt)
# rawimagename=current_dt + '_' + rawimagename

# print('Name of raw image will be: ', rawimagename)

# # take picture
# func_TakeNikonPicture(rawimagename)

# if __name__ == "__main__":
#     print(get_latest_image_path())
