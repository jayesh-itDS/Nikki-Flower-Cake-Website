"""
Image Management Script for Nikki Flower & Cake
===============================================

This script helps you add and manage product images easily.

USAGE:
    python manage_images.py --add "product-name.jpg" --category "flowers"
    python manage_images.py --list
    python manage_images.py --optimize

AUTHOR: Nikki Flower & Cake Team
"""

import os
import shutil
from pathlib import Path

# Configuration
STATIC_IMAGES_DIR = Path(__file__).parent / 'static' / 'images'
UPLOADS_DIR = Path(__file__).parent / 'uploads'  # Temporary upload folder

def create_uploads_folder():
    """Create uploads folder if it doesn't exist"""
    UPLOADS_DIR.mkdir(exist_ok=True)
    print(f"✓ Uploads folder created: {UPLOADS_DIR}")

def list_current_images():
    """List all images in static/images folder"""
    print("\n" + "="*60)
    print("CURRENT IMAGES IN STATIC/IMAGES")
    print("="*60)
    
    if not STATIC_IMAGES_DIR.exists():
        print(f"❌ Directory not found: {STATIC_IMAGES_DIR}")
        return
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    images = []
    
    for ext in image_extensions:
        images.extend(STATIC_IMAGES_DIR.glob(f'*{ext}'))
    
    if not images:
        print("No images found!")
        return
    
    print(f"\nTotal Images: {len(images)}\n")
    
    # Categorize images
    categories = {
        'Hero': [],
        'Category': [],
        'Product': [],
        'Occasion': [],
        'Feature': [],
        'Other': []
    }
    
    for img in images:
        name = img.name.lower()
        if 'hero' in name:
            categories['Hero'].append(img.name)
        elif 'category' in name:
            categories['Category'].append(img.name)
        elif 'product' in name:
            categories['Product'].append(img.name)
        elif 'occasion' in name:
            categories['Occasion'].append(img.name)
        elif 'feature' in name or 'testimonial' in name or 'about' in name:
            categories['Feature'].append(img.name)
        else:
            categories['Other'].append(img.name)
    
    for category, imgs in categories.items():
        if imgs:
            print(f"\n📁 {category} ({len(imgs)}):")
            for img in imgs:
                size = (STATIC_IMAGES_DIR / img).stat().st_size
                size_kb = size / 1024
                print(f"   • {img} ({size_kb:.1f} KB)")
    
    print("\n" + "="*60)

def get_image_suggestions():
    """Print suggestions for image names"""
    print("\n" + "="*60)
    print("RECOMMENDED IMAGE NAMING CONVENTION")
    print("="*60)
    print("""
🎨 HERO IMAGES (1200x600px):
   - hero-main.jpg
   - hero-flowers.jpg
   - hero-cakes.jpg

📂 CATEGORY IMAGES (600x400px):
   - category-flowers.jpg
   - category-cakes.jpg
   - category-combos.jpg
   - category-occasions.jpg

🛍️ PRODUCT IMAGES (800x800px):
   - product-rose-bouquet.jpg
   - product-chocolate-cake.jpg
   - product-anniversary-special.jpg
   - product-valentine-combo.jpg

🎉 OCCASION IMAGES (400x300px):
   - occasion-valentine.jpg
   - occasion-birthday.jpg
   - occasion-anniversary.jpg
   - occasion-mothers-day.jpg

✨ FEATURE/BADGE IMAGES (300x300px):
   - badge-free-delivery.png
   - badge-fresh-guarantee.png
   - icon-premium-quality.png

💡 TIPS:
   1. Use descriptive names
   2. Keep file sizes under 200KB
   3. Use JPG for photos, PNG for graphics
   4. Maintain consistent aspect ratios
   5. Optimize images before uploading
    """)
    print("="*60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage Nikki Flower & Cake Images')
    parser.add_argument('--list', action='store_true', help='List all current images')
    parser.add_argument('--suggest', action='store_true', help='Show image naming suggestions')
    parser.add_argument('--create-folders', action='store_true', help='Create necessary folders')
    
    args = parser.parse_args()
    
    if args.list:
        list_current_images()
    
    if args.suggest:
        get_image_suggestions()
    
    if args.create_folders:
        create_uploads_folder()
        print("✓ All necessary folders created!")
    
    # If no arguments provided, show help
    if not any([args.list, args.suggest, args.create_folders]):
        print("""
╔══════════════════════════════════════════════════════════╗
║   NIKKI FLOWER & CAKE - IMAGE MANAGEMENT SYSTEM         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Available Commands:                                     ║
║  -----------------                                       ║
║  python manage_images.py --list                          ║
║      Show all current images with sizes                  ║
║                                                          ║
║  python manage_images.py --suggest                       ║
║      Display recommended naming conventions              ║
║                                                          ║
║  python manage_images.py --create-folders                ║
║      Create necessary folder structure                   ║
║                                                          ║
║  QUICK START GUIDE:                                      ║
║  -----------------                                       ║
║  1. Copy your images to: static/images/                  ║
║  2. Follow the naming convention                         ║
║  3. Run: python manage_images.py --list                  ║
║  4. Update template references                           ║
║                                                          ║
║  For more help, visit the documentation                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)

if __name__ == '__main__':
    main()
