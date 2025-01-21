# 📸 Image Compressor & Geotagger

This is a **Streamlit web app** that allows users to **compress an image to under 2MB** while **retaining EXIF metadata** and **adding GPS coordinates** (latitude & longitude).

## 🚀 Features  
✅ Upload a **JPEG image**  
✅ Enter **latitude & longitude** in multiple formats  
✅ Preserve **EXIF metadata**  
✅ **Geotag the image** by adding GPS coordinates  
✅ **Compress** the image while maintaining quality  
✅ **Download** the optimized, geotagged image  

## 🛠️ Installation  

1. **Clone the repository**  
   ```sh
   git clone https://github.com/your-username/Image-Geotagger.git
   cd Image-Geotagger
   ```

2. **Create a virtual environment** (optional but recommended)  
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

## ▶️ Run the Application  
Start the Streamlit app with:  
```sh
streamlit run app.py
```
The app will open in your web browser.

## 📍 How to Use  

1️⃣ **Upload an image** (JPEG format)  
2️⃣ **Enter latitude & longitude** in any format:  
   - Decimal (**e.g.,** `18.463916`)  
   - Degrees, minutes, seconds (**e.g.,** `18°27'50.1"N, 73°50'9.1"E`)  
3️⃣ Click **Compress and Geotag**  
4️⃣ Download the optimized image with geotagging  

## 📚 Technologies Used  
- Python 3.x  
- Streamlit  
- Pillow (PIL)  
- Piexif  

## ✨ License  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
