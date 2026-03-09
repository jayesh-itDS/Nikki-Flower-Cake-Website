# 🖼️ Current Image Locations in Your Website

## 📋 How to Change Any Image

### **Quick Reference:**

| Section | Current Image File | What It Shows | Line in Template |
|---------|-------------------|---------------|------------------|
| **Hero Banner** | `hero-floral.jpg` | Main homepage banner | Line ~35 |
| **Category 1** | `flowers-rose-bouquet.jpg` | Flowers category card | Line 148 |
| **Category 2** | `cake-chocolate-delight.jpg` | Cakes category card | Line 163 |
| **Category 3** | `flowers-mixed-bouquet.jpg` | Combos category card | Line 178 |
| **Category 4** | `occasion-valentine-love.jpg` | Occasions category card | Line 193 |
| **Product 1** | `flowers-rose-bouquet.jpg` | Premium Rose Bouquet | Line 221 |
| **Product 2** | `cake-chocolate-delight.jpg` | Chocolate Truffle Cake | Line 259 |
| **Product 3** | `flowers-tulip-spring.jpg` | Mixed Floral Arrangement | Line 293 |
| **Product 4** | `cake-vanilla-berry.jpg` | Anniversary Combo | Line 327 |
| **Best Seller 1** | `flowers-rose-bouquet.jpg` | #1 Best Seller | Line 424 |
| **Best Seller 2** | `cake-chocolate-delight.jpg` | Hot Pick | Line 469 |
| **Best Seller 3** | `flowers-lily-elegance.jpg` | Trending | Line 505 |
| **Best Seller 4** | `cake-red-velvet.jpg` | Premium Choice | Line 544 |
| **Recently Viewed 1** | `flowers-rose-bouquet.jpg` | Rose Bouquet thumbnail | Line 593 |
| **Recently Viewed 2** | `cake-chocolate-delight.jpg` | Truffle Cake thumbnail | Line 599 |
| **Recently Viewed 3** | `flowers-tulip-spring.jpg` | Floral Arrangement thumbnail | Line 605 |
| **Recently Viewed 4** | `cake-vanilla-berry.jpg` | Anniversary Combo thumbnail | Line 611 |

---

## ✏️ Step-by-Step: Change an Image

### **Example: Change the Chocolate Cake Image**

#### **Current Setup:**
- **File:** `static/images/cake-chocolate-delight.jpg`
- **Used in:** Category 2, Product 2, Best Seller 2, Recently Viewed 2
- **Template Line:** 163 (category section)

#### **To Replace:**

**Option A: Replace the File**
1. Take/photo your new chocolate cake
2. Resize to 800x800px
3. Name it: `cake-chocolate-delight.jpg` (same name)
4. Copy to: `D:\Projects\static\images\`
5. Overwrite the existing file
6. Refresh browser: Ctrl + Shift + R

**Option B: Use a Different Image**
1. Add your new image: `my-awesome-cake.jpg`
2. Open: `templates/pages/home.html`
3. Find line 163 (search for "cake-chocolate-delight")
4. Replace with: `{% static 'images/my-awesome-cake.jpg' %}`
5. Save file
6. Refresh browser: Ctrl + Shift + R

---

## 🎨 Recommended Image Sizes

| Image Type | Dimensions | Max File Size | Format |
|------------|-----------|---------------|--------|
| **Hero Banner** | 1200×600px | 200KB | JPG |
| **Category Cards** | 600×400px | 100KB | JPG |
| **Product Cards** | 800×800px | 150KB | JPG |
| **Thumbnails** | 400×400px | 50KB | JPG |
| **Occasion Banners** | 600×400px | 100KB | JPG |

---

## 🛠️ Quick Edit Guide

### **Find and Replace Pattern:**

**Search for:**
```django
{% static 'images/OLD-IMAGE-NAME.jpg' %}
```

**Replace with:**
```django
{% static 'images/NEW-IMAGE-NAME.jpg' %}
```

### **Example Changes:**

#### **Change Flower Category Image:**
```django
<!-- BEFORE -->
<img src="{% static 'images/flowers-rose-bouquet.jpg' %}" alt="Flowers">

<!-- AFTER -->
<img src="{% static 'images/my-beautiful-tulips.jpg' %}" alt="Flowers">
```

#### **Change Cake Product Image:**
```django
<!-- BEFORE -->
<img src="{% static 'images/cake-chocolate-delight.jpg' %}" alt="Chocolate Truffle Cake">

<!-- AFTER -->
<img src="{% static 'images/delicious-black-forest.jpg' %}" alt="Chocolate Truffle Cake">
```

---

## 💡 Pro Tips

1. **Keep Original Filenames** - If replacing existing images, use the same filename to avoid editing templates
2. **Optimize Images First** - Use TinyPNG.com or Squoosh.app to compress images
3. **Descriptive Names** - Use names like `valentine-rose-bouquet.jpg` instead of `IMG_1234.jpg`
4. **Test on Mobile** - Check how images look on phone screens
5. **Consistent Style** - Keep similar backgrounds and lighting across all product photos

---

## 🔄 Batch Update All Images

If you want to replace ALL images at once:

1. Create a folder: `D:\Projects\new-images\`
2. Add all your new images there
3. Use this naming pattern:
   ```
   category-flowers.jpg
   category-cakes.jpg
   category-combos.jpg
   category-occasions.jpg
   product-1.jpg
   product-2.jpg
   product-3.jpg
   product-4.jpg
   ```
4. Copy all files to: `D:\Projects\static\images\`
5. Allow overwrite when prompted
6. Refresh browser

---

## ❓ Need Help?

**To see which images are currently used:**
```bash
python manage_images.py --list
```

**To get naming suggestions:**
```bash
python manage_images.py --suggest
```

**To regenerate placeholder images:**
```bash
python generate_product_images.py
```

---

**Last Updated:** March 3, 2026  
**Total Images:** 40  
**Template File:** `templates/pages/home.html`
