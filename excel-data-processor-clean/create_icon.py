#!/usr/bin/env python3
"""
创建应用程序图标
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_simple_icon():
    """创建一个简单的图标"""
    if not PIL_AVAILABLE:
        print("PIL/Pillow 未安装，跳过图标创建")
        print("如需图标，请安装: pip install Pillow")
        return False
    
    # 创建256x256的图像
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆形
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=4)
    
    # 绘制Excel表格图标
    cell_size = 30
    start_x = size // 2 - cell_size * 1.5
    start_y = size // 2 - cell_size * 1.5
    
    # 绘制3x3网格
    for i in range(3):
        for j in range(3):
            x = start_x + j * cell_size
            y = start_y + i * cell_size
            
            # 交替颜色
            if (i + j) % 2 == 0:
                color = (255, 255, 255, 255)
            else:
                color = (236, 240, 241, 255)
            
            draw.rectangle([x, y, x + cell_size - 2, y + cell_size - 2], 
                         fill=color, outline=(149, 165, 166, 255), width=1)
    
    # 保存为ICO文件
    try:
        # 创建多个尺寸的图标
        sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
        icons = []
        
        for icon_size in sizes:
            resized = img.resize(icon_size, Image.Resampling.LANCZOS)
            icons.append(resized)
        
        # 保存为ICO文件
        icons[0].save('icon.ico', format='ICO', sizes=[(icon.width, icon.height) for icon in icons])
        print("✅ 图标创建成功: icon.ico")
        return True
        
    except Exception as e:
        print(f"保存图标失败: {e}")
        return False

def create_text_icon():
    """创建基于文本的简单图标"""
    if not PIL_AVAILABLE:
        return False
    
    size = 256
    img = Image.new('RGBA', (size, size), (52, 152, 219, 255))
    draw = ImageDraw.Draw(img)
    
    # 尝试使用系统字体
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 80)
        except:
            font = ImageFont.load_default()
    
    # 绘制文本
    text = "EDP"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # 保存
    try:
        img.save('icon.ico', format='ICO')
        print("✅ 文本图标创建成功: icon.ico")
        return True
    except Exception as e:
        print(f"保存文本图标失败: {e}")
        return False

if __name__ == "__main__":
    print("创建应用程序图标...")
    
    if create_simple_icon():
        print("图标创建完成")
    elif create_text_icon():
        print("文本图标创建完成")
    else:
        print("图标创建失败，将使用默认图标")