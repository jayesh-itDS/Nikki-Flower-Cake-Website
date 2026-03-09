"""
Generate Premium Images for Nikki Flower & Cake
Creates professional placeholder images for:
- Cakes (various types)
- Flowers (different arrangements)
- Occasions (celebrations, events)
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient_background(width, height, color_start, color_end):
    """Create a gradient background"""
    img = Image.new('RGB', (width, height), color=color_start)
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            ratio = y / height
            r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
            g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
            b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
            pixels[x, y] = (r, g, b)
    
    return img

def add_decorative_elements(draw, width, height, color=(255, 255, 255, 100)):
    """Add decorative circles and patterns"""
    # Add corner decorations
    corner_size = 80
    # Top-left
    draw.pieslice([(0, 0), (corner_size, corner_size)], 0, 360, fill=color)
    # Top-right
    draw.pieslice([(width-corner_size, 0), (width, corner_size)], 0, 360, fill=color)
    # Bottom-left
    draw.pieslice([(0, height-corner_size), (corner_size, height)], 0, 360, fill=color)
    # Bottom-right
    draw.pieslice([(width-corner_size, height-corner_size), (width, height)], 0, 360, fill=color)
    
    # Add some floating circles
    draw.ellipse([(width//4, height//6), (width//4+40, height//6+40)], fill=(255, 255, 255, 50))
    draw.ellipse([(3*width//4, height//3), (3*width//4+30, height//3+30)], fill=(255, 255, 255, 50))
    draw.ellipse([(width//3, 2*height//3), (width//3+25, 2*height//3+25)], fill=(255, 255, 255, 50))

def create_cake_image(filename, title, subtitle, size=(800, 800)):
    """Create a premium cake product image"""
    img = create_gradient_background(
        size[0], size[1],
        (255, 182, 193),  # Light pink
        (255, 105, 180)   # Hot pink
    )
    draw = ImageDraw.Draw(img)
    
    # Add decorative elements
    add_decorative_elements(draw, size[0], size[1])
    
    # Draw cake illustration (simplified)
    # Cake base
    cake_width = size[0] * 0.6
    cake_height = size[1] * 0.4
    cake_x = (size[0] - cake_width) / 2
    cake_y = (size[1] - cake_height) / 2
    
    # Bottom layer
    draw.rectangle(
        [cake_x, cake_y + cake_height/3, cake_x + cake_width, cake_y + cake_height],
        fill=(139, 69, 19),  # Chocolate brown
        outline=(255, 255, 255),
        width=3
    )
    
    # Middle layer
    draw.rectangle(
        [cake_x + cake_width*0.1, cake_y + cake_height/6, 
         cake_x + cake_width*0.9, cake_y + cake_height/3],
        fill=(255, 182, 193),  # Pink frosting
        outline=(255, 255, 255),
        width=3
    )
    
    # Top layer
    draw.rectangle(
        [cake_x + cake_width*0.2, cake_y, cake_x + cake_width*0.8, cake_y + cake_height/6],
        fill=(255, 255, 255),  # White cream
        outline=(255, 255, 255),
        width=3
    )
    
    # Add candles
    candle_width = 15
    candle_height = 50
    num_candles = 5
    spacing = cake_width * 0.6 / num_candles
    
    for i in range(num_candles):
        candle_x = cake_x + cake_width*0.2 + i * spacing + spacing/2 - candle_width/2
        candle_y = cake_y - candle_height
        
        # Candle body
        draw.rectangle(
            [candle_x, candle_y, candle_x + candle_width, candle_y + candle_height],
            fill=(255, 215, 0),  # Gold
            outline=(255, 255, 255)
        )
        
        # Flame
        flame_radius = 8
        flame_center_x = candle_x + candle_width/2
        flame_center_y = candle_y - 10
        draw.ellipse(
            [flame_center_x - flame_radius, flame_center_y - flame_radius,
             flame_center_x + flame_radius, flame_center_y + flame_radius],
            fill=(255, 140, 0)  # Orange flame
        )
    
    # Add text
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_medium = ImageFont.truetype("arial.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Title text with shadow
    text = title
    text_bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size[0] - text_width) / 2
    text_y = size[1] - 180
    
    # Shadow
    draw.text((text_x+3, text_y+3), text, fill=(0, 0, 0, 100), font=font_large)
    # Main text
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font_large)
    
    # Subtitle
    if subtitle:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (size[0] - sub_width) / 2
        draw.text((sub_x, text_y + 60), subtitle, fill=(255, 255, 255, 200), font=font_medium)
    
    # Save
    img.save(filename, 'JPEG', quality=95, optimize=True)
    print(f"✓ Created cake image: {filename}")

def create_flower_image(filename, title, subtitle, flower_type='rose', size=(800, 800)):
    """Create a premium flower arrangement image"""
    # Different color schemes for different flower types
    colors = {
        'rose': ((220, 20, 60), (255, 182, 193)),      # Red to pink
        'tulip': ((255, 105, 180), (255, 192, 203)),   # Pink gradient
        'lily': ((255, 255, 255), (255, 182, 193)),    # White to pink
        'sunflower': ((255, 215, 0), (255, 140, 0)),   # Yellow to orange
        'orchid': ((148, 0, 211), (221, 160, 221)),    # Purple gradient
        'mixed': ((255, 105, 180), (255, 215, 0))      # Pink to yellow
    }
    
    color_start, color_end = colors.get(flower_type, colors['rose'])
    
    img = create_gradient_background(size[0], size[1], color_start, color_end)
    draw = ImageDraw.Draw(img)
    
    # Add decorative sparkles
    import random
    random.seed(42)  # Consistent pattern
    for _ in range(50):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        radius = random.randint(2, 5)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=(255, 255, 255, 150))
    
    # Draw flower bouquet (abstract representation)
    center_x = size[0] // 2
    center_y = size[1] // 2
    
    # Draw multiple flowers in a bouquet pattern
    num_flowers = 7
    bouquet_radius = min(size[0], size[1]) * 0.35
    
    for i in range(num_flowers):
        angle = (i / num_flowers) * 2 * 3.14159
        flower_x = center_x + int(bouquet_radius * 0.5 * (i % 3) * (1 if i % 2 == 0 else -1))
        flower_y = center_y + int(bouquet_radius * 0.3 * (i // 3))
        
        # Petal size
        petal_size = 40
        
        # Draw petals
        for j in range(5):
            petal_angle = (j / 5) * 2 * 3.14159
            petal_x = flower_x + int(petal_size * 0.5 * (1 if j % 2 == 0 else -1))
            petal_y = flower_y + int(petal_size * 0.5 * (1 if j % 2 == 0 else -1))
            
            draw.ellipse(
                [petal_x - petal_size//2, petal_y - petal_size//2,
                 petal_x + petal_size//2, petal_y + petal_size//2],
                fill=(255, 255, 255, 200)
            )
        
        # Draw center
        draw.ellipse(
            [flower_x - 15, flower_y - 15, flower_x + 15, flower_y + 15],
            fill=(255, 215, 0)  # Golden center
        )
    
    # Add ribbon/bow at bottom
    ribbon_width = size[0] * 0.4
    ribbon_height = 60
    ribbon_x = (size[0] - ribbon_width) / 2
    ribbon_y = center_y + bouquet_radius * 0.8
    
    # Ribbon loops
    draw.ellipse([ribbon_x, ribbon_y, ribbon_x + ribbon_height, ribbon_y + ribbon_height], 
                 fill=(255, 0, 0, 150))
    draw.ellipse([ribbon_x + ribbon_width - ribbon_height, ribbon_y, 
                  ribbon_x + ribbon_width, ribbon_y + ribbon_height], 
                 fill=(255, 0, 0, 150))
    
    # Add text
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_medium = ImageFont.truetype("arial.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    text = title
    text_bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size[0] - text_width) / 2
    text_y = size[1] - 180
    
    draw.text((text_x+3, text_y+3), text, fill=(0, 0, 0, 100), font=font_large)
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font_large)
    
    if subtitle:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (size[0] - sub_width) / 2
        draw.text((sub_x, text_y + 60), subtitle, fill=(255, 255, 255, 200), font=font_medium)
    
    img.save(filename, 'JPEG', quality=95, optimize=True)
    print(f"✓ Created flower image: {filename}")

def create_occasion_image(filename, title, subtitle, occasion_type='birthday', size=(600, 400)):
    """Create an occasion/event banner image"""
    # Color schemes for different occasions
    colors = {
        'birthday': ((255, 182, 193), (255, 105, 180), (255, 215, 0)),    # Pink to gold
        'anniversary': ((255, 192, 203), (220, 20, 60), (255, 255, 255)), # Rose to red
        'valentine': ((255, 105, 180), (220, 20, 60), (255, 255, 255)),   # Hot pink to red
        'mothers_day': ((255, 182, 193), (255, 105, 180), (255, 255, 255)),# Light to hot pink
        'wedding': ((255, 255, 255), (255, 192, 203), (255, 215, 0)),     # White to gold
        'graduation': ((148, 0, 211), (221, 160, 221), (255, 215, 0)),    # Purple to gold
        'christmas': ((220, 20, 60), (34, 139, 34), (255, 215, 0)),       # Red to green to gold
        'diwali': ((255, 140, 0), (255, 69, 0), (255, 215, 0))            # Orange to gold
    }
    
    color_start, color_mid, color_end = colors.get(occasion_type, colors['birthday'])
    
    # Create three-color gradient
    img = Image.new('RGB', size, color=color_start)
    pixels = img.load()
    
    for y in range(size[1]):
        for x in range(size[0]):
            ratio = x / size[0]
            if ratio < 0.5:
                r = int(color_start[0] * (1 - ratio*2) + color_mid[0] * (ratio*2))
                g = int(color_start[1] * (1 - ratio*2) + color_mid[1] * (ratio*2))
                b = int(color_start[2] * (1 - ratio*2) + color_mid[2] * (ratio*2))
            else:
                r = int(color_mid[0] * (2 - ratio*2) + color_end[0] * (ratio*2 - 1))
                g = int(color_mid[1] * (2 - ratio*2) + color_end[1] * (ratio*2 - 1))
                b = int(color_mid[2] * (2 - ratio*2) + color_end[2] * (ratio*2 - 1))
            pixels[x, y] = (r, g, b)
    
    draw = ImageDraw.Draw(img)
    
    # Add decorative elements based on occasion
    if occasion_type == 'birthday':
        # Balloons
        balloon_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        for i in range(5):
            bx = 50 + i * 120
            by = 80 + (i % 2) * 30
            color = balloon_colors[i % len(balloon_colors)]
            draw.ellipse([bx, by, bx+60, by+80], fill=color)
            # String
            draw.line([(bx+30, by+80), (bx+30, by+120)], fill=(255, 255, 255), width=2)
    
    elif occasion_type == 'anniversary':
        # Hearts
        heart_positions = [(100, 100), (300, 80), (500, 100), (200, 150), (400, 150)]
        for hx, hy in heart_positions:
            # Simple heart shape
            draw.polygon([
                (hx, hy), (hx+20, hy-20), (hx+40, hy), (hx+40, hy+30),
                (hx+20, hy+50), (hx, hy+50), (hx-20, hy+30), (hx-20, hy)
            ], fill=(255, 255, 255, 200))
    
    elif occasion_type == 'valentine':
        # Multiple hearts
        for i in range(8):
            hx = 50 + i * 75
            hy = 60 + (i % 3) * 40
            size_heart = 30 + (i % 2) * 20
            draw.ellipse([hx, hy, hx+size_heart, hy+size_heart*1.2], 
                        fill=(255, 255, 255, 180))
    
    else:
        # Generic confetti/sparkles
        import random
        random.seed(42)
        for _ in range(100):
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            radius = random.randint(3, 8)
            color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Add text
    try:
        font_large = ImageFont.truetype("arial.ttf", 42)
        font_medium = ImageFont.truetype("arial.ttf", 28)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Title with shadow
    text = title
    text_bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size[0] - text_width) / 2
    text_y = (size[1] - 100) // 2
    
    # Shadow
    draw.text((text_x+2, text_y+2), text, fill=(0, 0, 0, 100), font=font_large)
    # Main text
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font_large, stroke_width=2, stroke_fill=(0, 0, 0))
    
    # Subtitle
    if subtitle:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (size[0] - sub_width) / 2
        draw.text((sub_x, text_y + 50), subtitle, fill=(255, 255, 255, 230), font=font_medium)
    
    img.save(filename, 'JPEG', quality=95, optimize=True)
    print(f"✓ Created occasion image: {filename}")

def main():
    """Generate all images"""
    output_dir = "static/images"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n🎂 Creating Cake Images...")
    print("="*60)
    create_cake_image(f"{output_dir}/cake-chocolate-delight.jpg", "Chocolate Delight", "Rich & Decadent", size=(800, 800))
    create_cake_image(f"{output_dir}/cake-vanilla-berry.jpg", "Vanilla Berry", "Fresh & Creamy", size=(800, 800))
    create_cake_image(f"{output_dir}/cake-red-velvet.jpg", "Red Velvet", "Classic Elegance", size=(800, 800))
    create_cake_image(f"{output_dir}/cake-black-forest.jpg", "Black Forest", "German Classic", size=(800, 800))
    create_cake_image(f"{output_dir}/cake-butterscotch.jpg", "Butterscotch Bliss", "Sweet & Smooth", size=(800, 800))
    
    print("\n💐 Creating Flower Images...")
    print("="*60)
    create_flower_image(f"{output_dir}/flowers-rose-bouquet.jpg", "Rose Bouquet", "Classic Romance", flower_type='rose', size=(800, 800))
    create_flower_image(f"{output_dir}/flowers-tulip-spring.jpg", "Tulip Garden", "Spring Vibes", flower_type='tulip', size=(800, 800))
    create_flower_image(f"{output_dir}/flowers-lily-elegance.jpg", "Lily Elegance", "Pure Beauty", flower_type='lily', size=(800, 800))
    create_flower_image(f"{output_dir}/flowers-sunflower-joy.jpg", "Sunflower Joy", "Bright & Cheerful", flower_type='sunflower', size=(800, 800))
    create_flower_image(f"{output_dir}/flowers-orchid-luxury.jpg", "Orchid Luxury", "Exotic Beauty", flower_type='orchid', size=(800, 800))
    create_flower_image(f"{output_dir}/flowers-mixed-bouquet.jpg", "Mixed Bouquet", "Best of All", flower_type='mixed', size=(800, 800))
    
    print("\n🎉 Creating Occasion Images...")
    print("="*60)
    create_occasion_image(f"{output_dir}/occasion-birthday-bash.jpg", "Birthday Bash", "Celebrate in Style", occasion_type='birthday', size=(600, 400))
    create_occasion_image(f"{output_dir}/occasion-anniversary-special.jpg", "Anniversary Special", "Love Forever", occasion_type='anniversary', size=(600, 400))
    create_occasion_image(f"{output_dir}/occasion-valentine-love.jpg", "Valentine's Love", "For Your Special One", occasion_type='valentine', size=(600, 400))
    create_occasion_image(f"{output_dir}/occasion-mothers-day.jpg", "Mother's Day", "Thank You Mom", occasion_type='mothers_day', size=(600, 400))
    create_occasion_image(f"{output_dir}/occasion-wedding-bliss.jpg", "Wedding Bliss", "Perfect Beginnings", occasion_type='wedding', size=(600, 400))
    create_occasion_image(f"{output_dir}/occasion-graduation.jpg", "Graduation", "Congratulations!", occasion_type='graduation', size=(600, 400))
    create_occasion_image(f"{output_dir}/occasion-diwali.jpg", "Diwali Celebration", "Festival of Lights", occasion_type='diwali', size=(600, 400))
    create_occasion_image(f"{output_dir}/occasion-christmas.jpg", "Christmas Joy", "Merry & Bright", occasion_type='christmas', size=(600, 400))
    
    print("\n" + "="*60)
    print("✅ ALL IMAGES CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   🎂 Cake Images: 5 created")
    print(f"   💐 Flower Images: 6 created")
    print(f"   🎉 Occasion Images: 8 created")
    print(f"   📦 Total: 19 new images")
    print(f"\n📁 Location: {output_dir}/")
    print("\n💡 Next Steps:")
    print("   1. Run: python manage_images.py --list")
    print("   2. Update templates to use new images")
    print("   3. Refresh browser to see changes")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
