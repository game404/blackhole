# -*- coding:utf-8 -*-
"""
                                _  _     ___   _  _
  __ _   __ _  _ __ ___    ___ | || |   / _ \ | || |
 / _` | / _` || '_ ` _ \  / _ \| || |_ | | | || || |_
| (_| || (_| || | | | | ||  __/|__   _|| |_| ||__   _|
 \__, | \__,_||_| |_| |_| \___|   |_|   \___/    |_|
 |___/

black hole 图片生成
"""

from PIL import Image, ImageDraw, ImageFont
import pinyin
import shutil
import os
import struct

# 微信标准图片大小
WIDTH, HEIGHT = (900, 500)


def clean_folder(directory):
    """清理临时目录"""
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def _is_chinese(word):
    """判断汉字"""
    for ch in word:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def _optimize_length(word):
    """总长度控制10个字符"""
    return word if len(word) <= 10 else word[:7] + "..."


def _adjust_font_size(width, height, word, font_name):
    """根据字体和文字长度自动调整字体大小"""
    # 初始大小
    font_size = 100
    # 文字占比
    font_fraction = 0.80
    font = ImageFont.truetype(font_name, font_size)
    while font.getsize(word)[0] < font_fraction * width and font.getsize(word)[1] < font_fraction * height:
        font_size += 20
        font = ImageFont.truetype(font_name, font_size)
    return font


def _pinyin(chinese_word):
    """汉字转拼音"""
    return pinyin.get(chinese_word, format="strip")


def hex2rgb(hex_str):
    """RGB元素范围(0-255)"""
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str[1:]))
    return tuple([val for val in int_tuple])


def _pixelizator(word, image, filename):
    """继续像素化：缩小放大自动临近补齐"""
    # 字长需要变小，默认8
    pixel_size = 6 if len(word) >= 6 else 8
    downscaled_image = image.resize((int(image.size[0] / pixel_size),
                                     int(image.size[1] / pixel_size)),
                                    Image.NEAREST)
    upscaled_image = downscaled_image.resize((downscaled_image.size[0] * pixel_size,
                                              downscaled_image.size[1] * pixel_size),
                                             Image.NEAREST)
    upscaled_image.save("output/{}_pixel.png".format(filename))


def generator(word, background_color="white", font_color="", font_name=None):
    """
    图片生成
    默认白底，docker蓝(36,150,237)/#2496ed
    支持自定义字体
    """
    # 文字校验
    if not word:
        word = "balckhole"
    else:
        word = str(word)
    font_color = hex2rgb(font_color)
    # 清理输出目录
    clean_folder("output")
    # 强迫症，首字大写
    word = word.title()
    # 处理长度
    word = _optimize_length(word)
    if font_name:
        # 自定义字体后就只使用自定义字体
        fonts = [font_name]
    else:
        # 默认字体
        if _is_chinese(word):
            # 中文字体
            fonts = ["msyhbd.ttc", "simkai.ttf"]
            filename = _pinyin(word)
        else:
            # 英文字体
            fonts = ["Boron.ttf", "Candcu.ttf", "ennobled.ttf", "StarmapTruetype.ttf", "Verdana.ttf"]
            filename = word
        fonts = ["fonts/{}".format(font) for font in fonts]

    for idx, font_name in enumerate(fonts):
        image = Image.new("RGBA", (WIDTH, HEIGHT), background_color)
        draw = ImageDraw.Draw(image)
        font = _adjust_font_size(WIDTH, HEIGHT, word, font_name)
        w, h = font.getsize(word)
        # 文字垂直和水平居中
        draw.text(((WIDTH - w) / 2, (HEIGHT - h) / 2), word, fill=font_color, font=font)
        image.save("output/{}_{}.png".format(filename, idx, "png"))
        _pixelizator(word, image, "{}_{}".format(filename, idx))


if __name__ == '__main__':
    generator("游戏不存在")
