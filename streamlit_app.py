import streamlit as st
from PIL import Image
import piexif
import os
import tempfile
import re

def convert_to_dms(value):
    """Convert decimal coordinates to degrees, minutes, and seconds format required by EXIF."""
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = round((value - degrees - minutes / 60) * 3600, 5)
    return ((degrees, 1), (minutes, 1), (int(seconds * 100), 100))

def parse_coordinates(coord):
    """
    Parses latitude and longitude from user input.
    Supports decimal, DMS (Degrees, Minutes, Seconds), and N/S/E/W notation.
    """
    coord = coord.strip().upper()

    # Handle DMS format with N/S/E/W (e.g., "18°27'50.1\" N")
    match = re.match(r"(\d+)°(\d+)'([\d\.]+)\"\s*([NSEW])", coord)
    if match:
        degrees, minutes, seconds, direction = match.groups()
        decimal = int(degrees) + int(minutes) / 60 + float(seconds) / 3600
        if direction in ["S", "W"]:
            decimal *= -1
        return decimal

    # Handle simple decimal format (e.g., "18.463916")
    try:
        return float(coord)
    except ValueError:
        return None

def add_geotag(exif_dict, latitude, longitude):
    """Adds latitude and longitude to EXIF metadata."""
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: "N" if latitude >= 0 else "S",
        piexif.GPSIFD.GPSLatitude: convert_to_dms(abs(latitude)),
        piexif.GPSIFD.GPSLongitudeRef: "E" if longitude >= 0 else "W",
        piexif.GPSIFD.GPSLongitude: convert_to_dms(abs(longitude)),
    }
    exif_dict["GPS"] = gps_ifd
    return exif_dict

def compress_image(input_img, latitude, longitude, max_size_mb=2, quality=85):
    """Compress image while retaining metadata and adding geotag."""
    img = Image.open(input_img)

    # Extract existing EXIF data
    exif_data = piexif.load(img.info.get("exif", b""))
    st.write("Existing EXIF Data:", exif_data)

    # Modify EXIF to include geotagging
    exif_data = add_geotag(exif_data, latitude, longitude)
    exif_bytes = piexif.dump(exif_data)

    # Save the compressed image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_path = temp_file.name

    img_format = img.format if img.format else "JPEG"
    while True:
        img.save(temp_path, format=img_format, quality=quality, exif=exif_bytes)
        file_size_mb = os.path.getsize(temp_path) / (1024 * 1024)
        if file_size_mb < max_size_mb:
            break
        quality -= 5
        if quality < 20:
            break

    return temp_path

# Streamlit UI
st.title("📸 Image Compressor & Geotagger")
st.markdown("Upload an image, enter coordinates, and download the geotagged, compressed version.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg"])

latitude_input = st.text_input("Enter Latitude (Decimal or DMS format with N/S)", "18.463916")
longitude_input = st.text_input("Enter Longitude (Decimal or DMS format with E/W)", "73.835866")

if uploaded_file:
    # Convert coordinates
    lat = parse_coordinates(latitude_input)
    lon = parse_coordinates(longitude_input)

    if lat is None or lon is None:
        st.error("Invalid coordinates. Please enter in decimal or DMS format (e.g., '18.463916' or '18°27'50.1\" N').")
    else:
        st.success(f"Parsed Coordinates: Latitude {lat}, Longitude {lon}")
        
        if st.button("Compress & Add Geotag"):
            output_path = compress_image(uploaded_file, lat, lon)
            
            with open(output_path, "rb") as file:
                st.download_button(
                    label="📥 Download Compressed Image",
                    data=file,
                    file_name="compressed_geotagged.jpg",
                    mime="image/jpeg"
                )
