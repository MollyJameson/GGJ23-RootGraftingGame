from PIL import Image, ImageDraw, ImageFont
import csv

# Open the CSV file and read its contents into a list of dictionaries
with open("plant_deck.csv", "r") as file:
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

# Define the font and font size to use for text
font_size = 22
font = ImageFont.truetype("arial.ttf", font_size)
name_font = ImageFont.truetype("arial.ttf", 32)

curr_card_index = 0
# Iterate over each row of the data
for i, row in enumerate(data):
    # Draw a rectangle to represent the section of the image
    #draw.rectangle((0, i * 100, 500, (i + 1) * 100), fill="lightgray")
    number_of_this_card_to_print = int(row["num cards"])
    for j in range(number_of_this_card_to_print):
        card_row = int(curr_card_index / cards_per_row)
        card_col = int(curr_card_index % cards_per_row)
        curr_card_index = curr_card_index + 1
        xy_pos = (card_col * card_w_px, card_row * card_h_px)
        bottom_right_card_pos_px = (xy_pos[0] + card_w_px, xy_pos[1] + card_h_px)
        # [(x0, y0), (x1, y1)]
        card_position_on_sheet = [xy_pos, bottom_right_card_pos_px]
        # Whole card bg, useful for showing when we don't have an image
        draw.rectangle(card_position_on_sheet, fill="lightgray")


        # top overlay
        stat_overlay_size = (int(card_w_px),int(card_h_px/6))
        top_overlay = [xy_pos, (xy_pos[0] + stat_overlay_size[0], xy_pos[1] + stat_overlay_size[1])]
        bottom_overlay = [(xy_pos[0], xy_pos[1] + card_h_px - stat_overlay_size[1]), bottom_right_card_pos_px]

    
        # draw background image
        try:
            card_img = Image.open(row["imgpath"])
            # small squre, offset to below the top rectangle
            card_img = card_img.resize((card_w_px,card_w_px))
            img.paste(card_img, (xy_pos[0], xy_pos[1]+ stat_overlay_size[1]))
        except FileNotFoundError:
            print(f"Error: The file ${row['imgpath']} could not be found.")

        # draw overlays
        top_overlay_color = "ForestGreen"
        bottom_overlay_color = "Peru"
        type_color = "gray"
        border_width = 10

        if row["type (perennial or annual)"] == "A":
            type_color = "Yellow"
        elif row["type (perennial or annual)"] == "B":
            type_color = "MediumPurple"
        draw.rectangle(top_overlay, fill=top_overlay_color)
        draw.rectangle(bottom_overlay, fill=bottom_overlay_color)
        text_col_buffer_px = 15
        text_stroke_width = 0
        text_y_spacing = font_size + 5
        column2_px_offset = 230
        bottom_buffer_px = 5

        # Write the contents of each column of the row into the image
        value = row["name"]
        name_buffer_x = 5
        name_buffer_y = 5
        name_position = (xy_pos[0] + text_col_buffer_px + 5, xy_pos[1] + stat_overlay_size[1] + 5)
        bbox = draw.textbbox(name_position, value, font=name_font)
        # the bounding box is really tight, so add a buffer around each size.
        draw.rectangle([bbox[0] - name_buffer_x,bbox[1] - name_buffer_y,bbox[2] + name_buffer_x,bbox[3]+name_buffer_y], fill=(255, 255, 255, 100))
        draw.text(name_position, value, font=name_font, fill="black",stroke_fill="white",stroke_width=0)
        
        value = row["top statA (pest)"]
        draw.text((top_overlay[0][0] + text_col_buffer_px, xy_pos[1] + text_col_buffer_px + 0 * text_y_spacing), "pest: " + value, font=font, fill="black",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["top statB (heat)"]
        draw.text((top_overlay[0][0] + text_col_buffer_px, xy_pos[1] + text_col_buffer_px + 1 * text_y_spacing), "heat: " + value, font=font, fill="black",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["top statC (drought)"]
        draw.text((top_overlay[0][0] + text_col_buffer_px, xy_pos[1] + text_col_buffer_px + 2 * text_y_spacing), "water: " + value, font=font, fill="black",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["top statD (food)"]
        draw.text((top_overlay[0][0] + text_col_buffer_px + column2_px_offset, xy_pos[1] + text_col_buffer_px + 0 * text_y_spacing), "Food: " + value, font=name_font, fill="blue",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["bottom statA (pest)"]
        draw.text((bottom_overlay[0][0] + text_col_buffer_px, bottom_overlay[0][1] + bottom_buffer_px + 0 * text_y_spacing), "pest: " + value, font=font, fill="black",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["bottom statB (heat)"]
        draw.text((bottom_overlay[0][0] + text_col_buffer_px, bottom_overlay[0][1] + bottom_buffer_px + 1 * text_y_spacing), "heat: " + value, font=font, fill="black",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["bottom statC (drought)"]
        draw.text((bottom_overlay[0][0] + text_col_buffer_px, bottom_overlay[0][1] + bottom_buffer_px + 2 * text_y_spacing), "water: " + value, font=font, fill="black",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["bottom statD (food)"]
        draw.text((bottom_overlay[0][0] + text_col_buffer_px + column2_px_offset, bottom_overlay[0][1] + bottom_buffer_px + 0 * text_y_spacing), "Food: " + value, font=name_font, fill="blue",stroke_fill="white",stroke_width=text_stroke_width)
        value = row["bottom statE (root depth)"]
        draw.text((bottom_overlay[0][0] + text_col_buffer_px + column2_px_offset, bottom_overlay[0][1] + bottom_buffer_px + 2 * text_y_spacing), "Root Depth: " + value, font=font, fill="black",stroke_fill="white",stroke_width=text_stroke_width)

         # draw a frame around the whole thing
        draw.rectangle(card_position_on_sheet,width=border_width,outline=type_color)

# Save the image to disk
img.save("plant_deck.png")
