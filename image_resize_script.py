import sys
import os
from PIL import Image


def file_name(path):  # returns file name without file extension
    path = path.split('.')
    path = path[:-1]
    path = ''.join(path)
    path = path.split('\\')
    return path[-1]



exts = Image.registered_extensions()
avaiable_formats = [ex for ex, f in exts.items() if f in Image.OPEN]
avaiable_conv_types = ['L', '1', 'P', 'RGB', 'RGBA', 'CMYK', 'YCbCr', 'HSV', 'LAB', 'F', 'I', 'I;16', 'I;16B', 'I;16L', 'I;32', 'I;32B', 'I;32L', 'I;16U']  # arguments accepted by .convert() method

if_conv = False  # specifies whether we want to convert image using .convert() method
conv_type = "RGB"  # specifies convert type for .convert()
change_prop = False  # specifies wheather we want to change image proportions or just add margins
margin_color = (0, 0, 0)  # specifies margin color

# checking if arguments are correct

arg_num = len(sys.argv)

if arg_num < 6:
    print("wrong argument number")
    print("specify:  <source folder>  <destination folder>  <target height>  <target width>  <target format>  <additional options>")
    exit()

if sys.argv[3].isnumeric()==False or sys.argv[4].isnumeric()==False:  # checks if width and height are integers
    print("width and height must be integers")
    exit()

tarwidth = int(sys.argv[3])  # target width
tarheight = int(sys.argv[4])  # target height

if tarwidth >= 10000 or tarheight >= 10000:  # checks if target width and height are within reasonable boundaries
    print("width and height shall be less than 10000")
    exit()

if not sys.argv[5].startswith('.'):  # if theres no '.' before extension, adds it
    sys.argv[5] = '.' + sys.argv[5]

if avaiable_formats.count(sys.argv[5]) == 0:  # checks if a format is specified
    str_formats = ", ".join(avaiable_formats)
    print(f"specify one of the following formats: {str_formats}")
    exit()

if os.path.isdir(sys.argv[1]) == False:  # checks if sourse folder exists
    print("source folder doesnt exist")
    exit()

# checking for other options
i = 6
while(i < arg_num):
    if (sys.argv[i][1:] in avaiable_conv_types):
        if_conv = True
        conv_type = sys.argv[i][1:]
    elif (sys.argv[i] in ['-C', '-c', '--Color', '--color']):
        if (i + 3 < arg_num):
            if(sys.argv[i+1].isnumeric() and sys.argv[i+2].isnumeric() and sys.argv[i+3].isnumeric() and 0 <= int(sys.argv[i+1]) <= 255 and 0 <= int(sys.argv[i+2]) <= 255 and 0 <= int(sys.argv[i+3]) <= 255):
                margin_color = (int(sys.argv[i+1]), int(sys.argv[i+2]), int(sys.argv[i+3]))
                i += 3
            else:
                print("margin color shall be represented as 3 integers from 0 to 255")
                exit()
        else:
            print("margin color shall be represented as 3 integers from 0 to 255")
            exit()
    elif(sys.argv[i] in ['-P', '-p', '--Proportions', '--proportions']):
        change_prop = True
    else:
        print(f"unknown option {sys.argv[i]}")
        exit()
    i += 1



#

if os.path.isdir(sys.argv[2]) == False:  # if target folder doesnt exist, creates it
    os.mkdir(sys.argv[2])
    print(f"created folder: {sys.argv[2]}")

files = os.listdir(sys.argv[1])  # files in folder

i = 0  # counter of changed images
for file in files:
    path = sys.argv[1] + '\\' + file  # path to file

    # try opening, if opening cant be done (likely cause its not an image file) continue with next file
    try:
        image = Image.open(path)
    except:
        continue

    # changing image size
    width, height = image.size
    newwidth = 0  # new width
    newheight = 0  # new height
    top = 0  # top margin
    left = 0  # left marhin

    # calculating margins
    if width * tarheight > height * tarwidth:
        newwidth = tarwidth
        newheight = round((tarwidth/width)*height)
        top = round((tarheight - newheight)/2)
    else:
        newheight = tarheight
        newwidth = round((tarheight / height) * width)
        left = round((tarwidth - newwidth)/2)

    newpath = sys.argv[2] + '\\' + file_name(file) + sys.argv[5]  # path to resized file

    if (top == 0 and left == 0) or change_prop:  # when there are no margins (ariginal and new sizes have thse same width/height ratio or change_prop == True)
        image = image.resize((tarwidth, tarheight))
        if if_conv == True:
            image = image.convert("L")
        image.save(newpath)
        image.close()
        i += 1
        continue

    else:  # when there are margins
        image = image.resize((newwidth, newheight))
        result = Image.new(mode='RGB', size=(tarwidth, tarheight), color=margin_color)
        result.paste(image, (left, top))
        if if_conv == True:
            result = result.convert("L")
        result.save(newpath)
        image.close()
        result.close()
        i += 1

print(f"succesfouly converted {i} images")



