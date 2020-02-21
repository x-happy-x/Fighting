from PIL import Image
import cv2, os, shutil

def getFrame(video):
    vidcap = cv2.VideoCapture(video)
    outpath = video.split('.')[0]
    count = 0
    if os.path.isdir(outpath):
        shutil.rmtree(outpath)
    os.mkdir(outpath)
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            cv2.imwrite(os.path.join(outpath, '%d.png') % count, image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()
def Image_Crop(size, width, alpha=0):
    path = 'Characters/NewCreated'
    for file in os.listdir(path):
        name, action, num = file.split('_')
        num = int(num.split('.')[0])
        im = Image.open(os.path.join(path,file)).convert('RGBA')
        w,h = im.size
        if alpha:
            bg = im.getpixel((2,2))
            imdata_old = im.getdata()
            imdata_new = []
            for item in imdata_old:
                if item == bg:
                    imdata_new.append((255,255,255,0))
                else:
                    imdata_new.append(item)
            im.putdata(imdata_new)
        im = im.crop((0, 0, width, h))
        w,h = im.size
        im = im.resize((int(size*(w/h)),int(size)), Image.ANTIALIAS)
        if not os.path.isdir(os.path.join('Characters',name,action)):
            if not os.path.isdir(os.path.join('Characters', name)):
                os.mkdir(os.path.join('Characters', name))
            os.mkdir(os.path.join('Characters',name,action))
        im.save(os.path.join('Characters',name,action,str(num-1)+'.png'),'PNG',quality=100)
#getFrame('vid.mp4')
Image_Crop(270, 1000)