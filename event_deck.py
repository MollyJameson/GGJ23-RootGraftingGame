from PIL import Image, ImageDraw, ImageFont
import csv

def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        #w, h = font.getsize(' '.join(text_line))
        w = font.getlength(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return text_lines

# Open the CSV file and read its contents into a list of dictionaries
with open("event_deck.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)
img_width_px = 4096
img_height_px = 4096
cards_per_row = 10
cards_per_col = 7
card_w_px = int(img_width_px/cards_per_row)
card_h_px = int(img_height_px/cards_per_col)
# Create a blank image with a white background
img = Image.new("RGBA", (img_width_px, img_height_px), color="white")

# Create a drawing context for the image
draw = ImageDraw.Draw(img)

font_size = 24
font = ImageFont.truetype("arial.ttf", font_size)
name_font = ImageFont.truetype("arial.ttf", 32)
#not sure if this workds
font_bold = ImageFont.truetype("arialbd.ttf", font_size)

# Iterate over each row of the data
for i, row in enumerate(data):
    # Draw a rectangle to represent the section of the image
    #draw.rectangle((0, i * 100, 500, (i + 1) * 100), fill="lightgray")
    card_row = int(i / cards_per_row)
    card_col = int(i % cards_per_row)
    xy_pos = (card_col * card_w_px, card_row * card_h_px)
    bottom_right_card_pos_px = (xy_pos[0] + card_w_px, xy_pos[1] + card_h_px)
    # [(x0, y0), (x1, y1)]
    card_position_on_sheet = [xy_pos, bottom_right_card_pos_px]
    # Whole card bg, useful for showing when we don't have an image
    draw.rectangle(card_position_on_sheet, fill="lightgray")

    stat_overlay_size = (int(card_w_px),int(card_h_px/3))
    bottom_overlay = [(xy_pos[0], xy_pos[1] + card_h_px - stat_overlay_size[1]), bottom_right_card_pos_px]

    try:
        card_img = Image.open(row["imgpath"])
        # small squre, offset to below the top rectangle
        card_img = card_img.resize((card_w_px,card_w_px))
        img.paste(card_img, xy_pos)
    except FileNotFoundError:
        print(f"Error: The file ${row['imgpath']} could not be found.")

    text_col_buffer_px = 10
    text_stroke_width = 0
    
    # draw overlays
    overlay_color = "gray"
    draw.rectangle(bottom_overlay, fill=overlay_color)
    # draw name
    name_buffer_x = 5
    name_buffer_y = 5
    name_position = (xy_pos[0] + text_col_buffer_px, xy_pos[1] + 20)
    bbox = draw.textbbox(name_position, row["name"], font=name_font)
    # the bounding box is really tight, so add a buffer around each size.
    draw.rectangle([bbox[0] - name_buffer_x,bbox[1] - name_buffer_y,bbox[2] + name_buffer_x,bbox[3]+name_buffer_y], fill=(0, 0, 0, 100))
    draw.text(name_position, row["name"], font=name_font, fill="white",stroke_fill="white",stroke_width=0)
    #draw flavor text
    y_text = bottom_overlay[0][1]
    wrap_width_px = stat_overlay_size[0] - (text_col_buffer_px * 2)
    multiline_wrapped_list = wrap_text(row["functionalText"],wrap_width_px,font_bold)
    for line in multiline_wrapped_list:
        draw.text((xy_pos[0] + text_col_buffer_px, y_text), line, font=font_bold, fill=(255, 255, 255, 255))
        y_text += font_size + 2

    multiline_wrapped_list = wrap_text(row["flavorText"],wrap_width_px,font)
    for line in multiline_wrapped_list:
        draw.text((xy_pos[0] + text_col_buffer_px, y_text), line, font=font, fill=(0, 0, 0, 255))
        y_text += font_size
    #draw.multiline_text((bottom_overlay[0][0] + text_col_buffer_px, bottom_overlay[0][1] + text_col_buffer_px), row["flavorText"], font=font, fill="white", spacing=10, align='left', width=text_stroke_width)


# Save the image to disk
img.save("event_deck.png")