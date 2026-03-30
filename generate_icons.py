from PIL import Image

def generate_icons(input_path):
    try:
        img = Image.open(input_path)
        
        # 强制转换为RGBA模式，保留透明度
        img = img.convert('RGBA')
        
        # 生成 favicon.ico (包含多个尺寸)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save('favicon.ico', format='ICO', sizes=icon_sizes)
        print("✅ 成功生成 favicon.ico")
        
        # 生成 apple-touch-icon.png (180x180)
        apple_icon = img.resize((180, 180), Image.Resampling.LANCZOS)
        
        # 苹果图标通常需要不透明背景，这里将透明背景替换为白色
        background = Image.new('RGB', apple_icon.size, (255, 255, 255))
        if apple_icon.mode in ('RGBA', 'LA') or (apple_icon.mode == 'P' and 'transparency' in apple_icon.info):
            background.paste(apple_icon, mask=apple_icon.split()[3]) # 将图像粘贴到带白色背景的层上使用 alpha 通道作为 mask
        else:
            background = apple_icon.convert('RGB')
            
        background.save('apple-touch-icon.png', format='PNG')
        print("✅ 成功生成 apple-touch-icon.png (180x180)")

    except Exception as e:
        print(f"❌ 生成图标失败: {e}")

if __name__ == '__main__':
    generate_icons('logo.png')
