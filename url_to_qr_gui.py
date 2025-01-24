import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import qrcode
from PIL import Image, ImageTk
import os

class QRCodeGenerator:
    def __init__(self):
        # 创建主窗口     第一次增加的    第二次增加了    第三次增加了    第6次
        self.root = ThemedTk(theme="arc")  # 使用现代主题
        self.root.title("URL二维码生成器")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # 创建样式
        self.style = ttk.Style()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # URL输入区域
        self.url_frame = ttk.LabelFrame(self.main_frame, text="输入URL", padding="10")
        self.url_frame.pack(fill=tk.X, pady=(0, 10))

        self.url_entry = ttk.Entry(self.url_frame, width=50)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))

        # 按钮区域
        self.button_frame = ttk.Frame(self.url_frame)
        self.button_frame.pack(fill=tk.X)

        self.generate_button = ttk.Button(
            self.button_frame, 
            text="生成二维码", 
            command=self.generate_qr
        )
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(
            self.button_frame, 
            text="保存二维码", 
            command=self.save_qr,
            state=tk.DISABLED
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        # 预览区域
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="二维码预览", padding="10")
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("请输入URL并点击生成按钮")
        self.status_label = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding=(5, 2)
        )
        self.status_label.pack(fill=tk.X, pady=(10, 0))

        # 存储当前二维码图像
        self.current_qr = None
        self.current_qr_image = None

    def generate_qr(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入有效的URL")
            return

        try:
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
            self.current_qr = qr.make_image(fill_color="black", back_color="white")
            
            # 调整图像大小以适应预览窗口
            preview_size = (400, 400)
            self.current_qr_image = self.current_qr.copy()
            self.current_qr_image.thumbnail(preview_size)
            
            # 转换为PhotoImage以在tkinter中显示
            photo = ImageTk.PhotoImage(self.current_qr_image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # 保持引用
            
            # 启用保存按钮
            self.save_button.configure(state=tk.NORMAL)
            self.status_var.set("二维码生成成功！")

        except Exception as e:
            messagebox.showerror("错误", f"生成二维码时出错：{str(e)}")
            self.status_var.set("生成二维码失败")

    def save_qr(self):
        if self.current_qr is None:
            messagebox.showerror("错误", "请先生成二维码")
            return

        # 打开文件选择对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG文件", "*.png"), ("所有文件", "*.*")],
            initialfile="qr_code.png"
        )

        if file_path:
            try:
                self.current_qr.save(file_path)
                self.status_var.set(f"二维码已保存至：{file_path}")
                messagebox.showinfo("成功", "二维码已成功保存！")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件时出错：{str(e)}")
                self.status_var.set("保存二维码失败")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = QRCodeGenerator()
    app.run()
