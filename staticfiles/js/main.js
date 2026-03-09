/*
 * Nikki Flower & Cake - Premium E-commerce JavaScript
 * Handles interactive elements, animations, and dynamic functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize premium animations and interactions
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add to cart animation
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Added!';
            
            // Show floating cart animation
            showFloatingCartAnimation();
            
            setTimeout(() => {
                this.innerHTML = originalText;
            }, 2000);
        });
    });

    // Floating cart animation
    function showFloatingCartAnimation() {
        const floatingCart = document.createElement('div');
        floatingCart.innerHTML = '<i class="fas fa-shopping-bag text-xl"></i>';
        floatingCart.className = 'fixed z-50 text-2xl text-purple-600 animate-bounce';
        
        // Position near the button clicked
        floatingCart.style.left = Math.random() * 100 + 'vw';
        floatingCart.style.top = Math.random() * 100 + 'vh';
        
        document.body.appendChild(floatingCart);
        
        // Animate and remove
        setTimeout(() => {
            floatingCart.remove();
        }, 1000);
    }

    // Product card hover effects
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover-lift');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover-lift');
        });
    });

    // Image gallery slider
    const galleryThumbnails = document.querySelectorAll('.gallery-thumbnail');
    const mainImage = document.querySelector('.main-product-image');
    
    galleryThumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            // Remove active class from all thumbnails
            galleryThumbnails.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked thumbnail
            this.classList.add('active');
            
            // Change main image
            if (mainImage) {
                mainImage.src = this.src.replace('-thumb', '');
            }
        });
    });

    // Quantity selector buttons
    document.querySelectorAll('.quantity-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            let value = parseInt(input.value);
            
            if (this.dataset.action === 'increment') {
                value++;
            } else if (this.dataset.action === 'decrement' && value > 1) {
                value--;
            }
            
            input.value = value;
        });
    });

    // Wishlist toggle
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('text-red-500');
            this.classList.toggle('text-gray-500');
            
            const icon = this.querySelector('i');
            if (icon.classList.contains('far')) {
                icon.classList.replace('far', 'fas');
            } else {
                icon.classList.replace('fas', 'far');
            }
        });
    });

    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    
                    // Show error message
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'text-red-500 text-sm mt-1';
                    errorDiv.textContent = 'This field is required';
                    field.parentNode.insertBefore(errorDiv, field.nextSibling);
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });

    // Handle HTMX events
    document.body.addEventListener('htmx:beforeSend', function(evt) {
        console.log('Sending request...');
    });

    document.body.addEventListener('htmx:afterOnLoad', function(evt) {
        console.log('Request completed');
    });

    // Initialize tooltips if present
    if (typeof tippy !== 'undefined') {
        tippy('[data-tippy-content]', {
            theme: 'light-border',
            maxWidth: 300,
        });
    }
});

// Utility functions
const utils = {
    // Format currency
    formatCurrency: function(amount, currency = 'INR') {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Cart functionality
const cart = {
    // Add item to cart
    addItem: function(productId, quantity = 1, variantId = null) {
        // This would typically make an AJAX request
        console.log(`Adding ${quantity} of product ${productId} to cart`);
        
        // Update cart count
        this.updateCartCount();
    },
    
    // Update cart count display
    updateCartCount: function() {
        const cartCountElement = document.querySelector('.cart-count');
        if (cartCountElement) {
            // This would typically fetch the actual cart count from the server
            const currentCount = parseInt(cartCountElement.textContent) || 0;
            cartCountElement.textContent = currentCount + 1;
        }
    },
    
    // Get cart items
    getItems: function() {
        // This would typically fetch from the server
        return [];
    }
};

// Product filtering functionality
const productFilter = {
    // Filter products by category
    filterByCategory: function(categoryId) {
        // This would typically trigger an AJAX request
        console.log(`Filtering by category: ${categoryId}`);
    },
    
    // Filter products by price range
    filterByPrice: function(minPrice, maxPrice) {
        // This would typically trigger an AJAX request
        console.log(`Filtering by price range: ${minPrice} - ${maxPrice}`);
    },
    
    // Sort products
    sortBy: function(sortOption) {
        // This would typically trigger an AJAX request
        console.log(`Sorting by: ${sortOption}`);
    }
};