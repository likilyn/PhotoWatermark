import piexif
import exifread
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import glob
from util import convertFunction0, convertFunction1, getLocation

# 输出目录
save_dir = "./ImageAppWithDate"


def getImgDetail(picture_path):
    file = open(picture_path, "rb")
    tags = exifread.process_file(file)
    file.close()
    date_time = convertFunction0(tags['Image DateTime'])
    try:
        latitude = convertFunction1(tags['GPS GPSLatitude'])
        longitude = convertFunction1(tags["GPS GPSLongitude"])
        city = getLocation(latitude, longitude)
    except KeyError:
        city = ""
    txt = str(city + " " + date_time)
    img_length = float(tags['Image ImageLength'].printable)
    img_width = float(tags['Image ImageWidth'].printable)
    mi = min(img_width, img_length)
    font_size = int(mi / 30)
    rotate_dict = tags["Image Orientation"].printable.split(" ")

    if len(rotate_dict) == 1 or rotate_dict[0] == 'Horizontal':
        addWaterMark(src=picture_path, text=txt, font_size=font_size, rotateAngle=0)
    elif rotate_dict[0] == "Rotated" and rotate_dict[1] == '90':
        addWaterMark(src=picture_path, text=txt, font_size=font_size, rotateAngle=int(rotate_dict[1]),
                     rotateDirection=str(rotate_dict[2]))
    else:
        addWaterMark(src=picture_path, text=txt, font_size=font_size, rotateAngle=int(rotate_dict[1]))


def addWaterMark(src="./TestDir/IMG_20230522_115836.jpg", text='成都市 2023-6-3 21:54:09', font_size=50, rotateAngle=0,
                 rotateDirection=None):
    img_width = (len(text) - 10) * font_size
    img_height = font_size
    layer = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))
    d = ImageDraw.Draw(layer)
    font = ImageFont.truetype("simsun.ttc", font_size)
    d.text((0, 0), text, fill=(255, 255, 255), font=font)
    img1 = Image.open(src)
    w1, h1 = img1.size
    w2, h2 = layer.size
    pos = (w1 - w2 - int(font_size / 2), h1 - h2 - int(font_size / 2), w1 - int(font_size / 2), h1 - int(font_size / 2))
    if rotateAngle == 90 and rotateDirection == 'CW':
        layer = layer.transpose(Image.Transpose.ROTATE_90)
        pos = (w1 - h2 - int(font_size / 2), int(font_size / 2), w1 - int(font_size / 2), int(font_size / 2) + w2)
        img1.paste(layer, pos, layer)
    elif rotateAngle == 90 and rotateDirection == 'CCW':
        layer = layer.transpose(Image.Transpose.ROTATE_270)
        pos = (int(font_size / 2), h1 - w2 - int(font_size / 2), h2 + int(font_size / 2), h1 - int(font_size / 2))
        img1.paste(layer, pos, layer)
    elif rotateAngle == 180:
        layer = layer.transpose(Image.Transpose.ROTATE_180)
        pos = (int(font_size / 2), int(font_size / 2), w2 + int(font_size / 2), h2 + int(font_size / 2))
        img1.paste(layer, pos, layer)
    else:
        img1.paste(layer, pos, layer)
    exif_bytes = piexif.dump(piexif.load(img1.info['exif']))
    fname = src.split("\\")[-1]
    img1.save(save_dir + "/" + fname, quality=95, exif=exif_bytes)
    img1.close()


if __name__ == '__main__':
    # imgages是输入目录
    for i in glob.glob(".\\imgages\\*.jpg"):
        getImgDetail(i)
