import os
import subprocess

# Path to pngcrush (assuming it's in the same folder as your script)
pngcrush_path = "pngcrush.exe"

# Process images from 1.png to 32.png
for i in range(1, 33):
    image_name = f"assets/maps/forest/{i}.png"
    
    # Check if the image exists
    if os.path.exists(image_name):
        print(f"Processing {image_name}...")
        
        # Run pngcrush to remove the ICC profile
        subprocess.run([pngcrush_path, "-ow", "-rem", "allb", image_name], shell=True)

print("All images processed successfully!")
