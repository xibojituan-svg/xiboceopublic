import sys
from PIL import Image
import numpy as np
import cv2

path = "/Users/jiangdeming/.gemini/antigravity/brain/22183e7a-fbc7-4b81-b674-1cb386406874/xibo_logo_lobster_white_shirt_1774874418197.png"
img = Image.open(path).convert('RGB')
img_arr = np.array(img)

# Create a binary mask (pixels brighter than mostly dark)
# We can just threshold based on sum of RGB
mask = (np.sum(img_arr, axis=2) > 60).astype(np.uint8) * 255

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

bounding_boxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w * h > 500: # Filter out noise
        bounding_boxes.append((x, y, w, h))

print("Detected components:")
for idx, (x, y, w, h) in enumerate(bounding_boxes):
    print(f"{idx}: {x, y, w, h} (Area {w*h})")

icon_box = None
main_box = None

# Look for the small square bounding box on the right
for (x, y, w, h) in bounding_boxes:
    # Typical DALL-E/Midjourney small icon is around 100-200px wide, square-ish, often on right side
    if 100 < w < 300 and 100 < h < 300 and 0.8 < w/h < 1.3 and x > 600:
        icon_box = (x, y, w, h)
        break

if icon_box:
    main_xs, main_ys, main_xmax, main_ymax = [], [], [], []
    for (x, y, w, h) in bounding_boxes:
        # ignore icon box and very small boxes, or text that might be far right
        # but wait, text might be connected. We just consider all boxes EXCEPT the icon box.
        if (x, y, w, h) == icon_box:
            continue
        # Also ignore tiny noisy boxes far away
        if w * h > 100:
            main_xs.append(x)
            main_ys.append(y)
            main_xmax.append(x + w)
            main_ymax.append(y + h)
    
    if main_xs:
        main_x = min(main_xs)
        main_y = min(main_ys)
        main_w = max(main_xmax) - main_x
        main_h = max(main_ymax) - main_y
        main_box = (main_x, main_y, main_w, main_h)

print(f"Main Box: {main_box}")
print(f"Icon Box: {icon_box}")

# Add padding
padding = 20
if main_box:
    x, y, w, h = main_box
    # Make sure text is fully included
    nx1 = max(0, x - padding)
    ny1 = max(0, y - padding)
    nx2 = min(img.width, x + w + padding)
    ny2 = min(img.height, y + h + padding)
    
    # Crop it. Also make it transparent instead of black!
    main_crop = Image.open(path).convert("RGBA").crop((nx1, ny1, nx2, ny2))
    
    # Process transparency: replace near-black pixels with transparent
    data = main_crop.getdata()
    new_data = []
    for item in data:
        # If it's very dark gray/black (bg is around 9,9,11 or completely black)
        # Background threshold ~ RGB < 25
        if item[0] < 20 and item[1] < 20 and item[2] < 20:
            new_data.append((0, 0, 0, 0)) # transparent
        else:
            # Let's add slight anti-aliasing near edges? Just plain threshold for now
            new_data.append(item)
    main_crop.putdata(new_data)
    main_crop.save('logo.png')

if icon_box:
    x, y, w, h = icon_box
    # For icon, crop exactly the object box.
    icon_crop = Image.open(path).convert("RGBA").crop((x, y, x+w, y+h))
    
    # Also transparent background
    data = icon_crop.getdata()
    new_data = []
    for item in data:
        # If the background outside the square is black
        if item[0] < 20 and item[1] < 20 and item[2] < 20:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    icon_crop.putdata(new_data)
    
    # Resize
    icon_img_resized = icon_crop.resize((64, 64), Image.LANCZOS)
    
    # Make a background-filled version for ICO (favicons often need solid background or transparent)
    # The current logo square already has a white/rounded bg usually? 
    # Whatever it is, saving RGBA works for modern favicons.
    
    # Make an opaque version for ICO just in case
    bg = Image.new('RGB', (64, 64), (9, 9, 11))
    bg.paste(icon_img_resized, (0, 0), icon_img_resized)
    bg.save('favicon.ico', format='ICO', sizes=[(64,64)])
    
    icon_img_resized.save('favicon-64.png')
    
print("Extraction complete.")
