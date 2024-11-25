# import json
# import requests
#
# if __name__ == '__main__':
#     # response = requests.get("http://127.0.0.1:7860/ShoppingItemsGet").content.decode("utf-8")
#     # response = json.loads(response)
#     # print(response, type(response[0]))
#
#     response = requests.get("http://127.0.0.1:7860/ShoppingItemsGet?cover=Black-Myth-Wukong.jpg")
#
import requests

# 假设这是获取图像的接口
image_url = 'http://127.0.0.1:7860/ShoppingDataGet?cover=Black-Myth-Wukong.jpg'  # 替换为实际的图片 URL

# 获取字节流
response = requests.get(image_url).content

# 保存图片到本地
with open('image.jpg', 'wb') as f:  # 根据图片格式调整文件名和扩展名
    f.write(response)
print("图片已保存为 image.jpg")

