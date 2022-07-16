import sys
import glob
import cv2 as cv
import img2pdf
import numpy as np
import yaml

with open('./settings.yml') as f:
    settings = yaml.safe_load(f)
BEFORE_DIR = settings['CONVERT']['BEFORE_DIR']
AFTER_DIR = settings['CONVERT']['AFTER_DIR']
BEFORE_EXTENSION = settings['CONVERT']['BEFORE_EXTENSION']
AFTER_EXTENSION = settings['CONVERT']['AFTER_EXTENSION']
SCALE = settings['CONVERT']['SCALE']


def resize_image(img):
    # リサイズ
    size = (round(img.shape[1]*SCALE),
            round(img.shape[0]*SCALE))
    converted_img = cv.resize(img, dsize=size)
    return converted_img


def reduce_color_image(img):
    # 減色（白が灰色になってしまため補正）
    C = 16  # 4ビット分減らす
    B = (255//C)*C  # 白のビット
    A = 255-B  # 実際の白との差分
    converted_img = img // C
    converted_img = converted_img * C
    converted_img = converted_img + np.where(converted_img >= B, A, 0)
    return converted_img


if __name__ == '__main__':
    print("処理開始")

    print("画像書き出し中")
    raw_filenames = sorted(glob.glob(f'{BEFORE_DIR}/*.{BEFORE_EXTENSION}'))
    for index, raw_filename in enumerate(raw_filenames):
        converted_filename = f"{AFTER_DIR}/{index+1:0>4}.{AFTER_EXTENSION}"
        print(converted_filename)

        # 表紙のみカラー
        if index == 0:
            img = cv.imread(raw_filename)
            if img is None:
                sys.exit("Cloud not read the image.")
            converted_img = resize_image(img)
        else:
            img = cv.imread(raw_filename, 0)
            if img is None:
                sys.exit("Cloud not read the image.")
            converted_img = resize_image(img)
            converted_img = reduce_color_image(img)

        cv.imwrite(converted_filename, converted_img)

    print("PDF書き出し中")
    converted_filenames = sorted(
        glob.glob(f'{AFTER_DIR}/*.{AFTER_EXTENSION}'))
    with open('output.pdf', 'wb') as f:
        f.write(img2pdf.convert(
            converted_filenames,
        ))

    print("処理完了")
