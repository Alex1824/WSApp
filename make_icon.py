from PIL import Image, ImageDraw

def create_whatsapp_icon(size=(128, 128)):
    # Create a new image with white background
    icon = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(icon)
    
    # Draw a green circle (WhatsApp style)
    circle_bounds = (size[0] * 0.1, size[1] * 0.1, size[0] * 0.9, size[1] * 0.9)
    draw.ellipse(circle_bounds, fill='#25D366')  # WhatsApp green
    
    # Draw a simple phone/chat bubble shape
    bubble_points = [
        (size[0] * 0.3, size[1] * 0.3),
        (size[0] * 0.7, size[1] * 0.3),
        (size[0] * 0.7, size[1] * 0.6),
        (size[0] * 0.5, size[1] * 0.6),
        (size[0] * 0.4, size[1] * 0.7),
        (size[0] * 0.3, size[1] * 0.6),
    ]
    draw.polygon(bubble_points, fill='white')
    
    # Save the main icon
    icon.save('assets/icons/app_icon.png')
    
    # Create and save adaptive icons for Android
    # Foreground (logo on transparent background)
    foreground = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(foreground)
    draw.polygon(bubble_points, fill='white')
    foreground.save('assets/icons/app_icon_foreground.png')
    
    # Background (just the green circle)
    background = Image.new('RGB', size, '#25D366')
    background.save('assets/icons/app_icon_background.png')
    
    # Save other sizes
    icon.resize((48, 48)).save('assets/icons/app_icon_48.png')
    icon.resize((32, 32)).save('assets/icons/app_icon_32.png')
    icon.resize((16, 16)).save('assets/icons/favicon.ico')

if __name__ == '__main__':
    create_whatsapp_icon()
