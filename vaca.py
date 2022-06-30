from pickletools import optimize
from PIL import Image, ImageDraw, ImageOps
from font import fit_text
import os

CANVAS_SIZE = (1280, 720)
LOGO_PATH = os.path.join("Thumbnail Generator Assets", "Design Elements", "Can'tv Logo.png")
VS_PATH = os.path.join("Thumbnail Generator Assets", "Design Elements", "VS Text.png")
TOP_BAR_PATH = os.path.join("Thumbnail Generator Assets", "Design Elements", "Top Bar-04.png")
BOTTOM_BAR_PATH = os.path.join("Thumbnail Generator Assets", "Design Elements", "Bottom Bar-03.png")
FONT_PATH = os.path.join("Thumbnail Generator Assets", "Design Elements", "NovelSansPro_ExtraBold.otf")
STOCK_ICONS_PATH = os.path.join("Thumbnail Generator Assets", "Stock Icons")

def generate_thumbnail(data):
    canvas = Image.new(mode="RGBA", size=(1280, 720))
    draw = ImageDraw.Draw(canvas)

    left_name = data["left_player"]["character"]["name"]
    left_color = data["left_player"]["character"]["color"]
    left_pose = data["left_player"]["character"]["pose"]
    LEFT_PATH = os.path.join("Thumbnail Generator Assets", left_name, f"{left_name} {left_color} Pose {left_pose}.png")
    right_name = data["right_player"]["character"]["name"]
    right_color = data["right_player"]["character"]["color"]
    right_pose = data["right_player"]["character"]["pose"]
    RIGHT_PATH = os.path.join("Thumbnail Generator Assets", right_name, f"{right_name} {right_color} Pose {right_pose}.png")
    MAIN_COLORS = data["colors"]

    # Left Square
    shape = [(0, 0), (CANVAS_SIZE[0]//2, CANVAS_SIZE[1])]
    draw.rectangle(shape, fill=MAIN_COLORS[0])

    # Right Square
    shape = [(CANVAS_SIZE[0]//2, 0), (CANVAS_SIZE[0], CANVAS_SIZE[1])]
    draw.rectangle(shape, fill=MAIN_COLORS[1])

    # Renders
    renders_path = [LEFT_PATH, RIGHT_PATH]
    renders_size = [(448, 448), (448, 448)]
    renders_position = [(74, 215), (757, 215)]
    renders_shadow_color = [MAIN_COLORS[1], MAIN_COLORS[0]]
    renders_shadow_offset = [(-0.05, -0.05), (0.05, -0.05)]
    renders_flip = [data["left_player"]["character"]["flip"], data["right_player"]["character"]["flip"]]
    for i in range(len(renders_path)):
        render = Image.open(renders_path[i])
        if renders_flip[i]:
            render = ImageOps.mirror(render)
        w, h = render.size
        if w >= h:
            new_width = renders_size[i][0]
            new_height = int(h*(new_width/w))
            x_offset = 0
            y_offset = (renders_size[i][1]-new_height)//2
        else:
            new_height = renders_size[i][1]
            new_width = int(w*(new_height/h))
            x_offset = (renders_size[i][0]-new_width)//2
            y_offset = 0
        render = render.resize((new_width, new_height))
        x, y = renders_position[i]
        x += x_offset
        y += y_offset

        # Shadow
        temp_canvas = shadow = Image.new('RGBA', CANVAS_SIZE)
        shadow_x = x + int(renders_shadow_offset[i][0]*renders_size[i][0])
        shadow_y = y + int(renders_shadow_offset[i][1]*renders_size[i][1])
        shadow_xy = (shadow_x, shadow_y)
        temp_canvas.paste(render.convert("RGB"), shadow_xy, mask=render.split()[-1])
        shadow = Image.new('RGBA', CANVAS_SIZE, renders_shadow_color[i])
        # Using the original portrait as transparency mask
        canvas.paste(shadow, (0,0), mask=temp_canvas.split()[-1])

        canvas.paste(render.convert("RGB"), (x, y), mask=render.split()[-1])

    # Icons
    icons = [data["left_player"]["secondaries"], data["right_player"]["secondaries"]]
    icons_position = [[(12, 536), (74, 536)], [(1216, 536), (1154, 536)]]
    for i in range(len(icons)):
        for j in range(len(icons[i])):
            icon_path = os.path.join(STOCK_ICONS_PATH, f"{icons[i][j]} Stock Icon.png")
            icon = Image.open(icon_path).convert("RGBA").resize((52, 52))
            canvas.paste(icon, icons_position[i][j], mask=icon)

    # Design Elements
    items_path = [TOP_BAR_PATH, BOTTOM_BAR_PATH, VS_PATH, LOGO_PATH]
    items_resize = [False, False, False, (199, 174)]
    items_position = [(0, 47), (-40, 601), (344, 59), (524, 22)]

    for i in range(len(items_path)):
        item = Image.open(items_path[i]).convert("RGBA")
        if items_resize[i]:
            item = item.resize(items_resize[i], resample=Image.ANTIALIAS)
        alpha = item.split()[-1]
        canvas.paste(item.convert("RGB"), items_position[i], mask=alpha)

    # Text
    text_content = [data["left_player"]["name"], data["right_player"]["name"], "round", "date"]
    text_bound = [(64, 78, 484, 148), (787, 78, 1207, 148), (367, 635, 893, 697), (1070, 5, 1278, 46)]
    text_max_size = [63, 63, 100, 50]
    text_color = [(0,0,0), (0,0,0), (255, 255, 255), (255, 255, 255)]
    text_align = ["center", "center", "center", "right"]
    text_alignv = ["top", "top", "bottom", "middle"]

    for i in range(len(text_content)):
        fit_text(draw, text_bound[i], text_content[i], FONT_PATH, 
                align=text_align[i], alignv=text_alignv[i], fill=text_color[i], 
                shadow=None, guess=text_max_size[i])
    
    return canvas

if __name__ == "__main__":
    print("vaca")
    data = {
        "left_player": {
            "name": "BLEA GELO",
            "character": {
                "name": "Falco",
                "color": "Green",
                "pose": 1,
                "flip": False
            },
            "secondaries": ["Falcon", "Marth"]
        },
        "right_player": {
            "name": "WEED (L)",
            "character": {
                "name": "Fox",
                "color": "Red",
                "pose": 1,
                "flip": False
            },
            "secondaries": []
        },
        "round": "GRANDFINALS",
        "date": "1/09/2021",
        "colors": ((0, 117, 251), (254, 128, 67))
    }
    generate_thumbnail(data).save("sample.png", optimize=True)
