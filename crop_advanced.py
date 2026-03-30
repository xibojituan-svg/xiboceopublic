import sys
from PIL import Image

path = "/Users/jiangdeming/.gemini/antigravity/brain/22183e7a-fbc7-4b81-b674-1cb386406874/xibo_logo_lobster_white_shirt_1774874418197.png"
img = Image.open(path).convert('RGB')
width, height = img.size

pixels = img.load()

# Create connected components to isolate the square favicon box precisely
# We'll use a simple Flood Fill to find contiguous bright regions.

visited = [[False]*height for _ in range(width)]

def is_fg(x, y):
    r, g, b = pixels[x, y]
    # More strict: dark bg is ~10,10,10. Foreground is anything brighter
    return (r > 20 or g > 20 or b > 20)

components = []

for y in range(0, height, 5): # Stride to speed up finding seeds
    for x in range(0, width, 5):
        if is_fg(x, y) and not visited[x][y]:
            # Flood fill
            stack = [(x, y)]
            comp = []
            while stack:
                px, py = stack.pop()
                if 0 <= px < width and 0 <= py < height:
                    if not visited[px][py] and is_fg(px, py):
                        visited[px][py] = True
                        comp.append((px, py))
                        stack.append((px+1, py))
                        stack.append((px-1, py))
                        stack.append((px, py+1))
                        stack.append((px, py-1))
                        # Diagonal for continuous text
                        stack.append((px+1, py+1))
                        stack.append((px-1, py-1))
                        stack.append((px+1, py-1))
                        stack.append((px-1, py+1))
                        
            if len(comp) > 200:
                components.append(comp)

# Find bounding boxes for each component
bboxes = []
for comp in components:
    min_x = min(p[0] for p in comp)
    max_x = max(p[0] for p in comp)
    min_y = min(p[1] for p in comp)
    max_y = max(p[1] for p in comp)
    bboxes.append((min_x, min_y, max_x, max_y, comp))

icon_box = None
icon_comp = None

for min_x, min_y, max_x, max_y, comp in bboxes:
    w = max_x - min_x
    h = max_y - min_y
    # The icon is typically a square on the right side
    if 100 < w < 250 and 100 < h < 250 and 0.8 < w/h < 1.25 and min_x > 600:
        icon_box = (min_x, min_y, max_x, max_y)
        icon_comp = comp
        break

if not icon_box:
    # fallback to manual coordinates
    icon_box = (788, 436, 920, 568)

# Everything else is the main logo
main_min_x = min(b[0] for b in bboxes if b[0:4] != icon_box)
main_min_y = min(b[1] for b in bboxes if b[0:4] != icon_box)
main_max_x = max(b[2] for b in bboxes if b[0:4] != icon_box)
main_max_y = max(b[3] for b in bboxes if b[0:4] != icon_box)

main_box = (main_min_x, main_min_y, main_max_x, main_max_y)

print(f"Main Box: {main_box}")
print(f"Icon Box: {icon_box}")

# Extraction functions
def make_transparent(crop_img, bg_thresh=20):
    data = crop_img.getdata()
    new_data = []
    for item in data:
        if item[0] <= bg_thresh and item[1] <= bg_thresh and item[2] <= bg_thresh:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    crop_img.putdata(new_data)
    return crop_img

# Add padding and crop main
pad = 20
mx1, my1, mx2, my2 = main_box
mx1 = max(0, mx1 - pad)
my1 = max(0, my1 - pad)
mx2 = min(width, mx2 + pad)
my2 = min(height, my2 + pad)

main_crop = Image.open(path).convert("RGBA").crop((mx1, my1, mx2, my2))
main_crop = make_transparent(main_crop)
main_crop.save('logo.png')

# Crop icon precisely (without transparency inside the colored box)
ix1, iy1, ix2, iy2 = icon_box
icon_crop = Image.open(path).convert("RGBA").crop((ix1, iy1, ix2, iy2))
icon_crop = make_transparent(icon_crop)

icon_64 = icon_crop.resize((64, 64), Image.LANCZOS)
icon_64.save('favicon-64.png')

bg = Image.new('RGB', (64, 64), (9, 9, 11))
bg_rgba = Image.new('RGBA', (64, 64), (9, 9, 11, 255))
bg_rgba.paste(icon_64, (0, 0), icon_64)
bg_rgba.convert('RGB').save('favicon.ico', format='ICO', sizes=[(64,64),(32,32)])

print("Extraction complete.")
