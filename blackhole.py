# -*- coding:utf-8 -*-
#  ____   _               _     _             _
# | __ ) | |  __ _   ___ | | __| |__    ___  | |  ___
# |  _ \ | | / _` | / __|| |/ /| '_ \  / _ \ | | / _ \
# | |_) || || (_| || (__ |   < | | | || (_) || ||  __/
# |____/ |_| \__,_| \___||_|\_\|_| |_| \___/ |_| \___|
#
# black hole 命令行
import click
import word2picture

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--word", prompt="the word",
              help="图片文字")
@click.option("--bcolor", default="white", help="图片背景色，默认白色，支持颜色值['red', 'cyan', 'green', ...]及rgb hex值#ffffff")
@click.option("--fcolor", default="#2496ed",
              help="文字颜色，默认docker蓝，支持颜色值['red', 'cyan', 'green', ...]及rgb hex值#ffffff")
@click.option("--fpath", default=None, help="字体文件路径，默认空，使用预制字体。也许相对路径更合适。")
def generator(word, bcolor, fcolor, fpath):
    """
    黑洞图片生成器，协助生成微信公众号头图。自由不侵权，game404 出品。

    python运行示例:

        python blackhole.py --word docker

        python blackhole.py --word docker --bcolor black --fcolor #ffffff

        python blackhole.py --word docker --fpath some.ttf

    Docker运行示例:

        docker run -it --rm game404/blackhole docker

        ...

    """
    click.echo("start generator {} picture".format(word))
    click.echo("picture background color {} , font color {} and font path {}".format(bcolor, fcolor, fpath))
    # TODO 校验颜色合法性
    word2picture.generator(word, background_color=bcolor, font_color=fcolor, font_name=fpath)
    click.echo("well done , please see picture in output folder! ")


if __name__ == '__main__':
    generator()
