import qrcode
from PIL import Image, ImageOps, ImageDraw, ImageFont
import time
import csv

# Specify the CSV file path
csv_file_path = "file.csv"

# Open the CSV file

def create_qr_with_logo_label_and_frame(
    url, logo_path, output_path, qr_size=500, logo_size_ratio=0.2, frame_thickness=10, label="TAG-0012", font_path="arialbd.ttf", font_size=48
):
    """
    Create a QR code with a logo in the middle, a label below surrounded by a black frame, and a black frame around the entire image.

    :param url: The URL to encode in the QR code.
    :param logo_path: Path to the logo image file.
    :param output_path: Path to save the generated QR code image.
    :param qr_size: Size (width and height) of the QR code image in pixels.
    :param logo_size_ratio: The ratio of the logo size relative to the QR code size (default 0.2).
    :param frame_thickness: Thickness of the black frame in pixels (default 20).
    :param label: The text to add below the QR code (default "TAG-0012").
    :param font_path: Path to a .ttf font file (default "arialbd.ttf" for Arial Black).
    :param font_size: Size of the label text (default 14).
    """
    # Create a QR Code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code. Higher number = larger code.
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo.
        box_size=10,  # Size of each box in pixels.
        border=4,  # Width of the border (minimum is 4 for QR codes).
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create the QR Code image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # Open the logo image
    logo = Image.open(logo_path)

    # Calculate the logo size
    logo_size = int(qr_size * logo_size_ratio)
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Calculate position for the logo
    logo_position = (
        (qr_img.width - logo.width) // 2,
        (qr_img.height - logo.height) // 2
    )

    # Paste the logo onto the QR code
    qr_img.paste(logo, logo_position, mask=logo if "A" in logo.mode else None)
    label_height = frame_thickness + font_size + 10  # Extra space for label and padding

    #Expand image hacia abajo
    expanded_height = qr_img.height + 0
    temp_image = Image.new("RGB", (qr_img.width, expanded_height),
                          "white")  # New image with added space at the bottom
    temp_image.paste(qr_img, (0, 0))
    qr_img = temp_image

    # Draw the label with a black frame
    draw = ImageDraw.Draw(qr_img)
    try:
        # Use the specified font
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error loading font: {e}. Falling back to default font.")
        font = ImageFont.load_default()

    # Measure text size
    text_width=128
    text_height=64
    #text_width, text_height = font.getsize(label)

    # Calculate positions
    padding = 2  # Padding around the text within the black frame
    label_x0 = (qr_img.width - text_width - 2 * padding) // 2
    label_y0 = qr_img.height + (label_height - text_height) // 2 - padding
    label_x1 = label_x0 + text_width + 2 * padding
    label_y1 = label_y0 + text_height + 2 * padding

    # Draw black rectangle for the label
    #draw.rectangle([label_x0, label_y0, label_x1, label_y1], fill="black")

    # Draw the text centered within the black rectangle
    text_x = (qr_img.width - text_width) // 2 -20
    text_y = qr_img.height - (label_height - text_height) // 2-46

    #draw.text((text_x, text_y), label, fill="black", font=font)

    #qr_img = Image.new("RGB", (qr_img.width,qr_img.height + 10), "white")  # 0*label_height"

    # Add a black frame around the entire QR code image
    #qr_with_frame = ImageOps.expand(qr_img, border=frame_thickness, fill="black")

    # Add space for the label
    #final_img = Image.new("RGB", (qr_with_frame.width, qr_with_frame.height + 10), "black") #0*label_height"
    #final_img.paste(qr_with_frame, (0, 0))

    # Draw the label with a black frame
    #draw = ImageDraw.Draw(final_img)


    # Save the final image
    qr_img.save(output_path)
    time.sleep(0)
    return  "Terminado"
    print(f"QR Code with logo, label (Arial Black, size 14, framed), and black border saved to {output_path}")


# Example usages
url = "https://sites.google.com/view/qr-aris/qr-wtp/pupe-0013"
logo_path = "Aros _RPCI.jpg"  # Path to your logo image file
label = "PUPE-0013"  # Label text to display below the QR code
font_path = "arialbd.ttf"  # Path to Arial Black font file on your system


with open("TAGS.csv", mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file,delimiter=";")  # Use DictReader to access columns by name

    # Iterate through each row
    for row in reader:
        TAG = row['TAG']  # Access the TAG column
        PREFIX=row['PREFIX']
        LINK = row['LINK']  # Access the Link column
        output_path = f'URLS/{TAG}.png'  # Output file path for the QR code with logo, label, and frame

        create_qr_with_logo_label_and_frame(LINK, logo_path, output_path, label=TAG, font_path=font_path)
