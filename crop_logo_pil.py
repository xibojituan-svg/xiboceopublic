import sys
from PIL import Image

path = "/Users/jiangdeming/.gemini/antigravity/brain/22183e7a-fbc7-4b81-b674-1cb386406874/xibo_logo_lobster_white_shirt_1774874418197.png"
img = Image.open(path).convert('RGB')
width, height = img.size

pixels = img.load()

# Find foreground pixels
fg_pixels = []
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        # Any pixel not extremely dark is foreground
        if r > 20 or g > 20 or b > 20:
            fg_pixels.append((x, y))

if not fg_pixels:
    print("Error: No foreground found!")
    sys.exit(1)

# The icon is on the right. Let's find a separation gap vertically.
# We'll project x coordinates.
xs = [p[0] for p in fg_pixels]
x_counts = [0] * width
for x in xs:
    x_counts[x] += 1

# Find a gap of size > 20 pixels between x=300 and x=800
gap_start = 0
gap_end = 0
in_gap = False
for x in range(300, 800):
    if x_counts[x] == 0:
        if not in_gap:
            gap_start = x
            in_gap = True
    else:
        if in_gap:
            gap_end = x
            if gap_end - gap_start > 20: # found a significant gap!
                break
            in_gap = False

split_x = gap_end if gap_end > 0 else 700
print(f"Splitting image at x = {split_x}")

main_pixels = [p for p in fg_pixels if p[0] < split_x]
icon_pixels = [p for p in fg_pixels if p[0] >= split_x]

def get_bbox(points):
    if not points: return None
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    return (min_x, min_y, max_x, max_y)

main_bbox = get_bbox(main_pixels)
icon_bbox = get_bbox(icon_pixels)

print(f"Main BBox: {main_bbox}")
print(f"Icon BBox: {icon_bbox}")

# Add padding
padding = 20
if main_bbox:
    x1, y1, x2, y2 = main_bbox
    nx1 = max(0, x1 - padding)
    ny1 = max(0, y1 - padding)
    nx2 = min(width, x2 + padding)
    ny2 = min(height, y2 + padding)
    
    main_crop = Image.open(path).convert("RGBA").crop((nx1, ny1, nx2, ny2))
    
    data = main_crop.getdata()
    new_data = []
    for item in data:
        if item[0] < 20 and item[1] < 20 and item[2] < 20:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    main_crop.putdata(new_data)
    main_crop.save('logo.png')

if icon_bbox:
    x1, y1, x2, y2 = icon_bbox
    icon_crop = Image.open(path).convert("RGBA").crop((x1, y1, x2, y2))
    
    data = icon_crop.getdata()
    new_data = []
    for item in data:
        if item[0] < 20 and item[1] < 20 and item[2] < 20:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    icon_crop.putdata(new_data)
    
    icon_img_resized = icon_crop.resize((64, 64), Image.LANCZOS)
    
    bg = Image.new('RGB', (64, 64), (9, 9, 11))
    bg.paste(icon_img_resized, (0, 0), icon_img_resized)
    bg.save('favicon.ico', format='ICO', sizes=[(64,64)])
    
    icon_img_resized.save('favicon-64.png')
    
print("Extraction complete.")
