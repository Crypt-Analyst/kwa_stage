# Create default avatar placeholder script
from PIL import Image, ImageDraw
import os

def create_default_avatar():
    # Create a 150x150 image with a gray background
    size = (150, 150)
    image = Image.new('RGB', size, color=(108, 117, 125))  # Bootstrap secondary color
    
    draw = ImageDraw.Draw(image)
    
    # Draw a simple person icon
    # Head circle
    head_center = (75, 55)
    head_radius = 20
    draw.ellipse([head_center[0] - head_radius, head_center[1] - head_radius,
                  head_center[0] + head_radius, head_center[1] + head_radius], 
                 fill='white')
    
    # Body shape (simplified)
    body_points = [(55, 85), (95, 85), (110, 120), (110, 150), (40, 150), (40, 120)]
    draw.polygon(body_points, fill='white')
    
    # Save the image
    output_path = 'static/images/default-avatar.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    print(f"Default avatar created at: {output_path}")

if __name__ == '__main__':
    try:
        create_default_avatar()
    except ImportError:
        print("PIL not available. Creating a simple placeholder instead.")
        # Create a simple HTML-based placeholder instead
        with open('static/images/default-avatar.png', 'w') as f:
            f.write("DEFAULT_AVATAR_PLACEHOLDER")

create_default_avatar()
