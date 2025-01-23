import qrcode
from PIL import Image

def create_qr_code(url, output_file='qr_code.png'):
    """
    将URL转换为二维码图片
    
    参数:
        url: 要转换的URL
        output_file: 输出的图片文件名
    """
    # 创建QR码实例
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # 添加数据
    qr.add_data(url)
    qr.make(fit=True)

    # 创建图像
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # 保存图像
    qr_image.save(output_file)
    print(f"二维码已生成并保存为: {output_file}")

if __name__ == "__main__":
    # 获取用户输入的URL
    url = input("请输入要转换成二维码的URL: ")
    
    # 获取用户输入的输出文件名（可选）
    output_file = input("请输入输出文件名（直接回车默认为'qr_code.png'）: ").strip()
    if not output_file:
        output_file = 'qr_code.png'
    
    # 确保文件名以.png结尾
    if not output_file.lower().endswith('.png'):
        output_file += '.png'
    
    # 生成二维码
    create_qr_code(url, output_file)
