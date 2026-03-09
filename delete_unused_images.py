"""
Delete Unused Images from static/images/
Safely removes images that are not referenced in any templates
"""

import os
from pathlib import Path
import shutil

# List of unused images (identified from template analysis)
UNUSED_IMAGES = [
    'about-hero.jpg',
    'cake-black-forest.jpg',
    'cake-butterscotch.jpg',
    'category-cakes.jpg',  # Very large file (605.9 KB)
    'category-combo.jpg',
    'category-flowers.jpg',
    'category-occasions.jpg',
    'contact-hero.jpg',
    'feature-1.jpg',
    'feature-2.jpg',
    'feature-3.jpg',
    'feature-4.jpg',
    'flowers-orchid-luxury.jpg',
    'flowers-sunflower-joy.jpg',
    'gift-message-card.jpg',
    'occasion-anniversary-special.jpg',
    'occasion-anniversary.jpg',
    'occasion-birthday-bash.jpg',
    'occasion-birthday.jpg',
    'occasion-christmas.jpg',
    'occasion-diwali.jpg',
    'occasion-graduation.jpg',
    'occasion-mothers-day.jpg',
    'occasion-valentine.jpg',
    'occasion-wedding-bliss.jpg',
    'product-1.jpg',
    'product-2.jpg',  # Very large file (3.4 MB!)
    'product-3.jpg',
    'product-4.jpg',
    'testimonial-bg.jpg',
]

def main():
    image_dir = Path('static/images')
    
    print('='*70)
    print('🗑️  DELETE UNUSED IMAGES')
    print('='*70)
    print()
    
    deleted_count = 0
    total_size_saved = 0
    
    for img_name in UNUSED_IMAGES:
        img_path = image_dir / img_name
        
        if img_path.exists():
            size_kb = img_path.stat().st_size / 1024
            try:
                img_path.unlink()
                print(f'✅ Deleted: {img_name} ({size_kb:.1f} KB)')
                deleted_count += 1
                total_size_saved += size_kb
            except Exception as e:
                print(f'❌ Error deleting {img_name}: {e}')
        else:
            print(f'⚠️  Not found: {img_name}')
    
    print()
    print('='*70)
    print(f'Deletion Summary:')
    print(f'  Files deleted: {deleted_count}')
    print(f'  Space recovered: {total_size_saved:.1f} KB ({total_size_saved/1024:.2f} MB)')
    print('='*70)
    print()
    
    if deleted_count > 0:
        print('✅ SUCCESS! Unused images removed.')
        print()
        print('💡 Remaining images in use:')
        print('   - hero-floral.jpg')
        print('   - flowers-rose-bouquet.jpg')
        print('   - cake-chocolate-delight.jpg')
        print('   - flowers-mixed-bouquet.jpg')
        print('   - occasion-valentine-love.jpg')
        print('   - flowers-tulip-spring.jpg')
        print('   - cake-vanilla-berry.jpg')
        print('   - flowers-lily-elegance.jpg')
        print('   - cake-red-velvet.jpg')
        print('   - placeholder-product.jpg')
        print('   - favicon.ico')
    else:
        print('ℹ️  No unused images found (already deleted?)')
    
    print('='*70)

if __name__ == '__main__':
    main()

