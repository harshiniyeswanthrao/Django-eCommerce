from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from first_app.models import Product, Order, OrderItem
from decimal import Decimal
from django.urls import reverse
from .models import Product, Product_detail
# from .models import Cart, Product
from .models import Product
from decimal import Decimal

# THIS IS MY HOME_OR_SHOP
def home_or_shop(request):
    products = Product.objects.all()
    return render(request, 'homepage.html', {'products': products})

# THIS IS MY PRODUCT_LIST
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# THIS IS MY PRODUCT_DETAILS

# def product_detail(request, id):
#     product = get_object_or_404(Product, id=id)
#     return render(request, 'product_detail.html', {'product': product})

def product_detail(request, id):
    # Get the product or return a 404 if not found
    product = get_object_or_404(Product, id=id)

    # Get the product details or return a 404 if not found
    details = get_object_or_404(Product_detail, product=product)

    # Prepare the context for rendering the template
    context = {
        'product': product,
        'details': details,
    }
    return render(request, 'product_detail.html', context)


# THIS IS MY ADD_TO_CART
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {'products': []})
        product = get_object_or_404(Product, id=product_id)
        found = False
        for item in cart['products']:
            if item['id'] == product.id:
                item['quantity'] += 1
                found = True
                break
        if not found:
            cart['products'].append({'id': product.id, 'quantity': 1})
        request.session['cart'] = cart
        return redirect('view_cart')

# THIS IS MY VIEW_CART
def view_cart(request):
    cart = request.session.get('cart', {'products': []})
    products = []
    total = 0

    for item in cart['products']:
        try:
            product = Product.objects.get(id=item['id'])
            quantity = item['quantity']
            item_total = product.price * quantity
            total += item_total
            products.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
        except Product.DoesNotExist:
            continue

    context = {
        'cart': {'products': products},
        'cart_total': total,
    }
    return render(request, 'view_cart.html', context)

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {'products': []})
        updated_cart_products = [item for item in cart['products'] if item['id'] != int(product_id)]
        request.session['cart'] = {'products': updated_cart_products}
        return redirect('view_cart')
    return redirect('view_cart')


def get_cart(request):
    """Retrieve the cart from the session."""
    return request.session.get('cart', {})

def increase_quantity(request, product_id):
    """Increase the quantity of a product in the cart."""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1, 'price': str(product.price)}

    request.session['cart'] = cart  # Save updated cart to session
    return redirect('view_cart')

def decrease_quantity(request, product_id):
    """Decrease the quantity of a product in the cart."""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    if str(product_id) in cart:
        if cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1
        else:
            del cart[str(product_id)]  # Remove product if quantity goes to 0

    request.session['cart'] = cart  # Save updated cart to session
    return redirect('view_cart')

# THIS IS MY CHECKLIST
def checklist(request):
    if request.method == 'POST':
        selected_product_ids = request.POST.getlist('selected_products')
        selected_products = Product.objects.filter(id__in=selected_product_ids)
        total_amount = sum(product.price for product in selected_products)
        request.session['total_amount'] = str(total_amount)
        request.session['selected_products'] = list(selected_product_ids)
        return redirect('shipping_details')
    context = {'items' : items , 'orders' : orders}
    return render(request, 'checklist.html')

# THIS IS MY SHIPPING_DETAILS
def shipping_details(request):
    selected_product_ids = request.session.get('selected_products', [])
    selected_products = Product.objects.filter(id__in=selected_product_ids)
    total_amount = Decimal(request.session.get('total_amount', '0'))

    context = {
        'selected_products': selected_products,
        'total_amount': total_amount,
    }
    return render(request, 'shipping_details.html', context)

# THIS IS MY PLACE_ORDER
def place_order(request):
    if request.method == 'POST':
        try:
            order = Order.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                address=request.POST['address'],
                city=request.POST['city'],
                state=request.POST['state'],
                zipcode=request.POST['zipcode'],
            )
            product_ids = request.POST.getlist('product_ids')
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1  # Example quantity
                )
            return redirect('order_summary', order_id=order.id)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
    return render(request, 'order_summary.html')

# THIS IS MY ORDER_SUMMARY
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    selected_product_ids = request.session.get('selected_products', [])

    # Filter products based on selected product IDs
    selected_products = Product.objects.filter(id__in=selected_product_ids)

    # Clear the existing order items
    OrderItem.objects.filter(order=order).delete()

    # Create new order items based on selected products
    for product in selected_products:
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1)  # Set quantity as needed

    # Fetch updated order items
    order_items = OrderItem.objects.filter(order=order)
    total_amount = sum(item.get_total_item_price() for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'total_amount': total_amount,
        'selected_products': selected_products,
    }
    return render(request, 'order_summary.html', context)

def my_orders(request):
    if request.user.is_authenticated:
        # Filter orders for the authenticated user based on their email
        orders = Order.objects.filter(email=request.user.email)
    else:
        orders = []  # Return an empty list if the user is not authenticated

    return render(request, 'My_Orders.html', {'orders': orders})



# THIS IS MY CONTACT
def contact(request):
    return render(request, 'contact.html')
