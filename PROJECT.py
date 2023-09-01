from colorthief import ColorThief
import matplotlib.pyplot as plt
#Todo=File Search Algo
image_path = "C:\\Users\\aryan\Downloads\\Quick Share\\20230901_180053.jpg"
#TodoCompression Algo
reselect=0
option=1
#Mode Selection
def change():
    option=int(input('''Enter 1 For Basic Mode
Enter 2 For Advance Mode 
Enter 3 For Suggestion
Your Choice: '''))
    return option
change()
def Basic():
    img= ColorThief(image_path)
    limit=int(input("Enter range of colours to extract info:"))
    palet = img.get_palette(color_count=20)
    hexcode=[]
#Convert RGB to hex(take tuple as arguemnt and using format specifier convert it to hexa form)
    def rgtohex(rgb):
         return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
    for i in range(0,limit):
        hexcode.append(rgtohex(palet[i]))
    print("Hex color palette:",hexcode)
    domi=img.get_color()
    plt.imshow([[palet[i] for i in range (limit)]])
    plt.show()
    
while(option!=0):
    if option==1:
        Basic()
        option=change()
    elif option==2:
        pass
    #def Advance():
        #Open CV to continue
    else:
        print("No Valid Input Exiting The Program")
        option=0
print("End!")


