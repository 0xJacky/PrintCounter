import numpy as np


# 算法 https://www.cnblogs.com/zwq-zju/p/9721613.html
def is_color_image(img, threshold=15):
    if len(img.getbands()) == 1:
        return True

    img1 = np.asarray(img.getchannel(channel=0), dtype=np.int16)
    img2 = np.asarray(img.getchannel(channel=1), dtype=np.int16)
    img3 = np.asarray(img.getchannel(channel=2), dtype=np.int16)
    diff1 = (img1 - img2).var()
    diff2 = (img2 - img3).var()
    diff3 = (img3 - img1).var()
    diff_sum = (diff1 + diff2 + diff3) / 3.0
    return diff_sum > threshold
