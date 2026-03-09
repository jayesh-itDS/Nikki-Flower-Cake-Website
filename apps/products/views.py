from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Product, Category, Occasion


def home(request):
    """
    Home page view showing featured products and categories.
    """
    featured_products = Product.objects.filter(
        is_featured=True, 
        is_available=True
    ).select_related('category')[:8]
    
    categories = Category.objects.filter(is_active=True)[:4]
    trending_products = Product.objects.filter(
        is_trending=True, 
        is_available=True
    ).select_related('category')[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'trending_products': trending_products,
    }
    return render(request, 'pages/home.html', context)


def product_list(request):
    """
    Product listing page with filtering and sorting capabilities.
    """
    products = Product.objects.filter(is_available=True).select_related('category')
    
    # Filtering
    category_slug = request.GET.get('category')
    occasion_slug = request.GET.get('occasion')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('q')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if occasion_slug:
        products = products.filter(occasions__slug=occasion_slug)
    if min_price:
        try:
            products = products.filter(base_price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(base_price__lte=float(max_price))
        except ValueError:
            pass
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Sorting
    sort = request.GET.get('sort', 'created_at')
    if sort == 'price_low':
        products = products.order_by('base_price')
    elif sort == 'price_high':
        products = products.order_by('-base_price')
    elif sort == 'rating':
        # Defaulting to created_at for rating since reviews aren't fully implemented
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products.distinct(), 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    occasions = Occasion.objects.filter(is_active=True)
    
    # Determine if request is HTMX for partial rendering
    if request.headers.get('HX-Request'):
        template = 'components/product_grid.html'
    else:
        template = 'pages/products/list.html'
    
    context = {
        'products': page_obj,
        'categories': categories,
        'occasions': occasions,
        'current_category': category_slug,
        'current_occasion': occasion_slug,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_sort': sort,
        'search_query': search_query,
    }
    return render(request, template, context)


def product_detail(request, slug):
    """
    Product detail page showing full product information.
    """
    product = get_object_or_404(
        Product.objects.prefetch_related('variants', 'occasions', 'reviews'),
        slug=slug,
        is_available=True
    )
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'pages/products/detail.html', context)


@require_http_methods(["GET"])
def get_variant_price(request, variant_id):
    """
    HTMX endpoint to get updated price when product variant changes.
    """
    from .models import ProductVariant
    variant = get_object_or_404(ProductVariant, id=variant_id, is_active=True)
    
    # In a real implementation, we would calculate prices based on addons, etc.
    context = {
        'variant': variant,
        'final_price': variant.final_price
    }
    return render(request, 'components/variant_price.html', context)