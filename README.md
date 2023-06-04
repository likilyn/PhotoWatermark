# PhotoWatermark
这是一个根据图片EXIF信息提取图片拍摄时间和拍摄地点并将其作为图片水印的项目。
## 使用教程
将需要添加水印的图片（图片需要是拍摄的原图，即包含EXIF信息）放在imgages文件夹下，运行main.py即可，添加好水印的图片会存储在ImageAppWithDate中。imgages和ImageAppWithDate需要提前创建好。
## 类似研究
GitHub上现有的为图片添加水印的项目不是特别多（可能大家觉得这个没挑战性），我参考的两个项目没有办法完全满足我的需求——要么只有时间没有日期，要么不支持旋转过的图片。
## 实现方式

实现的流程其实很简单。

* 拿到图片的EXIF信息，包括拍摄时间和拍摄的经纬度。
* 拍摄时间不需要特别处理，只需要根据个人喜好进行稍稍格式化即可；EXIF存储的拍摄经纬度是以度分秒的形式存储的，需要通过简单的计算转换成十进制，以便获得拍摄地点。
* 将拍摄时间和地点绘制在一张PNG图片中（这张图片还需要根据原图片的旋转角度和方向进行一定角度的旋转），使用PIL.Image.paste()进行两张图片的合并（这里使用图片合并而不是直接在图片上打印文字主要是考虑到文字旋转不便，这样就不好在旋转后的图片上打印文字）。
* 计算上述图片应该出现在原图片的哪个位置——这个位置应该要随着原图片的旋转角度和方向变化。
* 合并两张图片，把原图的EXIF信息赋值给处理后的图片。

## 实现效果

原图：

![IMG_20230522_144557](https://raw.githubusercontent.com/likilyn/PicStorage/main/Img/202306042034741.jpg)

处理后的图片：

![IMG_20230522_144557](https://raw.githubusercontent.com/likilyn/PicStorage/main/Img/202306042035109.jpg)

## 改进方向

* 水印的图片颜色为固定值，有时候会和背景混淆，如果改成根据图片自适应改变颜色就会好很多。
* 程序处理的时候没有用户反馈，用户无法把握处理的进度，加个进度条用户体验会好很多。

## 参考项目/文章

* https://github.com/lemodd/photo_watermark
* https://github.com/shudal/add_date_to_photo
* https://www.qiniu.com/qfans/qnso-245447
* https://cloud.tencent.com/developer/article/1702764
