import sys
from PIL import Image

path = "/Users/jiangdeming/.gemini/antigravity/brain/22183e7a-fbc7-4b81-b674-1cb386406874/xibo_logo_lobster_white_shirt_1774874418197.png"
img = Image.open(path).convert('RGB')
width, height = img.size

# Make a purely 0/255 mask for bounding box calculations
def get_foreground_bbox(sub_img):
    mask = sub_img.point(lambda p: 255 if p > 20 else 0).convert("L")
    return mask.getbbox()

# 1. Main Logo (left side, width up to 750px)
left_side = img.crop((0, 0, 760, height))
main_bbox = get_foreground_bbox(left_side)
if main_bbox:
    # main_bbox gives (left, upper, right, lower) RELATIVE to the crop
    x1, y1, x2, y2 = main_bbox
    # Add padding
    pad = 10
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(760, x2 + pad)
    y2 = min(height, y2 + pad)
    
    main_crop = left_side.crop((x1, y1, x2, y2)).convert("RGBA")
    data = main_crop.getdata()
    new_data = []
    for item in data:
        if item[0] < 20 and item[1] < 20 and item[2] < 20: # Make bg transparent
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    main_crop.putdata(new_data)
    main_crop.save('logo.png')
    print("Main logo saved.")

# 2. Favicon Icon (right side region)
right_side = img.crop((760, 0, width, height))
icon_bbox = get_foreground_bbox(right_side)
if icon_bbox:
    x1, y1, x2, y2 = icon_bbox
    # crop it exactly with no padding
    icon_crop = right_side.crop((x1, y1, x2, y2)).convert("RGBA")
    
    # Make background outside the square transparent
    data = icon_crop.getdata()
    new_data = []
    for item in data:
        if item[0] < 20 and item[1] < 20 and item[2] < 20:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    icon_crop.putdata(new_data)
    
    # Resize
    icon_64 = icon_crop.resize((64, 64), Image.LANCZOS)
    icon_64.save('favicon-64.png')
    
    # Optional: Opaque version for standard ICO compatibility
    bg = Image.new('RGBA', (64, 64), (9, 9, 11, 255))
    bg.paste(icon_64, (0, 0), icon_64)
    bg.save('favicon.ico', format='ICO', sizes=[(64,64),(32,32)])
    print("Favicon saved.")

