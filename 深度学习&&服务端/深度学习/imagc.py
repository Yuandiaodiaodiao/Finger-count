import os
from PIL import Image
import cv2

ax=0
for (root, dirs, files) in os.walk("."):
    for filename in files:
        ax+=1
        if "py" not in filename:
        #     os.remove(os.path.join(root,filename))
        # else:
        #     os.rename(os.path.join(root,filename), os.path.join(root,"b"+filename))

        # print(os.path.join(root,filename))
        #     os.rename(os.path.join(root, filename), os.path.join(root, str(ax)))
            imc=cv2.imread(os.path.join(root,filename))
            cv2.imwrite(os.path.join(root,filename),imc)
            im=Image.open(os.path.join(root,filename))
            # print("h=",im.height,"w=",im.width)

            maxx = min(im.height, im.width)
            # box = (0, 0, maxx, maxx)
            # im = im.crop(box)
            if maxx>450:

                # im=im.resize((800,int(800/(im.width/im.height))),Image.BICUBIC)
                im=im.resize((450,int(450/(im.width/im.height))),Image.ANTIALIAS)
                im.save(os.path.join(root,filename),"JPEG",quality = 100)
# im=Image.open("color_5_0002.png")
# maxx=max(im.height,im.width)
# box=(0,0,max,max)
# im=im.crop(box)
#
# im.save("color_5_0002.png")
