import cv2
import sys
import numpy as np

def simple_white_balance(img):
    # 分离图像通道
    b, g, r = cv2.split(img)

    # 计算每个通道的平均值
    b_avg = np.mean(b)
    g_avg = np.mean(g)
    r_avg = np.mean(r)

    # 计算缩放因子
    k_r = (g_avg + b_avg) / (2 * r_avg)
    k_b = (g_avg + r_avg) / (2 * b_avg)

    # 缩放R, B通道
    r = cv2.multiply(r, k_r)
    b = cv2.multiply(b, k_b)

    # 合并通道
    result = cv2.merge((b, g, r))
    return result


def estimate_color_temperature(img_path):
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError("Image not found or invalid format")

    # 计算图像的平均色
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    # 将平均色从BGR转换为RGB
    avg_color_rgb = np.flip(avg_color)

    # 计算色温
    r, g, b = avg_color_rgb
    n = (r + g + b) / 3
    color_temperature = (g / n) * 6500

    return color_temperature

if __name__ == "__main__":
    path = sys.argv[1]
    img_path = path
    color_temperature = estimate_color_temperature(img_path)
    print(color_temperature)

    # if(color_temperature > 7100):
    #     img_path = path
    #
    #     img = cv2.imread(img_path)
    #     # 应用简单白平衡
    #     result = simple_white_balance(img)
    #     # 显示和保存结果
    #     cv2.imwrite(img_path, result)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
