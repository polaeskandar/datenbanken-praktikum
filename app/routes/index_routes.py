from flask import Blueprint, redirect, url_for, request, Response, flash, abort
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from app import app, db
from app.components.restaurants.restaurant_menu_component import (
    restaurant_menu_component,
)
from app.models.Cart import Cart
from app.models.CartItem import CartItem
from app.models.Restaurant import Restaurant
from app.models.MenuItem import MenuItem
from app.components.layout.navbar_component import navbar_component
from app.components.layout.footer_component import footer_component
from app.components.restaurants.cart_component import cart_component
from app.components.restaurants.restaurant_header_component import (
    restaurant_header_component,
)
from app.components.search.restaurants_list_component import restaurants_list_component
from app.components.search.search_header_component import search_header_component
from app.components.search.search_heading_carousel_component import (
    search_heading_carousel,
)
from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.routes import render_page
from app.services.component_safe_renderer import safe_render_component
from app.services.search.restaurant_search_service import RestaurantSearchService

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
@index_routes.route("/search", methods=["GET", "POST"])
@login_required
def index() -> Response:
    if current_user.is_restaurant():
        return redirect(url_for("admin.index"))

    restaurant_search_context = RestaurantSearchContext(
        restaurant_names=request.args.get("search_terms"),
        postal_codes=request.args.get("postal_codes"),
    )

    restaurant_search_service = RestaurantSearchService(restaurant_search_context)
    restaurants = restaurant_search_service.fetch_restaurants()

    components = build_components(
        [
            lambda: search_header_component(
                restaurant_search_service, len(restaurants)
            ),
            search_heading_carousel,
            lambda: restaurants_list_component(restaurants),
        ]
    )

    return render_page("layout.html", "Home", components)


@index_routes.route("/search/<int:restaurant_id>", methods=["GET", "POST"])
def restaurant_page(restaurant_id: int) -> Response:
    try:
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first_or_404(
            restaurant_id
        )
    except HTTPException:
        flash("The requested restaurant does not exist.", "danger")

        return redirect(url_for("index.index"))

    components = build_components_for_restaurant_page(
        [
            lambda: restaurant_header_component(restaurant),
            lambda: restaurant_menu_component(restaurant),
        ],
        [
            lambda: cart_component(restaurant),
        ],
    )

    return render_page("restaurant.html", "Home", components)


@index_routes.route("/search/<int:restaurant_id>/cart/add/<int:item_id>", methods=["GET"])
def add_to_cart(restaurant_id: int, item_id: int) -> Response:
    try:
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first_or_404()
    except HTTPException:
        flash("The requested restaurant does not exist.", "danger")

        return redirect(url_for("index.index"))

    try:
        item = MenuItem.query.filter_by(id=item_id).first_or_404()
    except HTTPException:
        flash("The requested menu item does not exist.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    # Query for the existing Cart
    cart = Cart.query.filter_by(
        customer_id=current_user.customer.id,
        restaurant_id=restaurant.id
    ).first()

    # Create cart if not found
    if cart is None:
        cart = Cart(
            customer=current_user.customer,
            restaurant=restaurant
        )
        db.session.add(cart)
        db.session.commit()

    # Look up if this item is already in the Cart
    item_in_cart = CartItem.query.filter_by(
        cart_id=cart.id,
        menu_item_id=item.id
    ).first()

    # If it's not in the cart, create a new CartItem; else increment quantity
    if item_in_cart is None:
        item_in_cart = CartItem(
            quantity=1,
            menu_item_id=item.id,
            cart_id=cart.id
        )
        db.session.add(item_in_cart)
    else:
        item_in_cart.quantity += 1

    db.session.commit()

    flash("Item added to cart.", "success")

    return redirect(request.referrer or url_for("index.index"))

@index_routes.route("/search/<int:restaurant_id>/cart/<int:cart_id>/increment/<int:item_id>", methods=["GET"])
def increment_item_quantity(restaurant_id: int, cart_id: int, item_id: int) -> Response:
    # 1. Fetch the restaurant
    try:
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first_or_404()
    except HTTPException:
        flash("The requested restaurant does not exist.", "danger")
        return redirect(url_for("index.index"))

    # 2. Fetch the item to ensure it actually exists
    try:
        item = MenuItem.query.filter_by(id=item_id).first_or_404()
    except HTTPException:
        flash("The requested menu item does not exist.", "danger")
        return redirect(request.referrer or url_for("index.index"))

    # 3. Find the user's cart for this restaurant
    cart = Cart.query.filter_by(
        id=cart_id
    ).first()

    # If there's no cart at all, there's nothing to increment
    if cart is None:
        flash("You don't have any items in your cart yet.", "warning")

        return redirect(request.referrer or url_for("index.index"))
    
    # Authorization check
    if current_user.customer.id != cart.customer_id:
        abort(403)

    # 4. Look for the CartItem that corresponds to this item
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        menu_item_id=item.id
    ).first()

    # If it's not in the cart, there's nothing to increment
    if cart_item is None:
        flash("This item is not currently in your cart.", "warning")

        return redirect(request.referrer or url_for("index.index"))

    # 5. Increment the quantity
    cart_item.quantity += 1
    db.session.commit()

    flash("Item quantity updated.", "success")

    return redirect(request.referrer or url_for("index.index"))


@index_routes.route("/search/<int:restaurant_id>/cart/<int:cart_id>/decrement/<int:item_id>", methods=["GET"])
def decrement_item_quantity(restaurant_id: int, cart_id: int, item_id: int) -> Response:
    # 1. Fetch the restaurant
    try:
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first_or_404()
    except HTTPException:
        flash("The requested restaurant does not exist.", "danger")
        return redirect(url_for("index.index"))

    # 2. Fetch the item to ensure it actually exists
    try:
        item = MenuItem.query.filter_by(id=item_id).first_or_404()
    except HTTPException:
        flash("The requested menu item does not exist.", "danger")
        return redirect(request.referrer or url_for("index.index"))

    # 3. Find the user's cart for this restaurant
    cart = Cart.query.filter_by(
        id=cart_id
    ).first()

    # If there's no cart at all, there's nothing to remove from
    if cart is None:
        flash("You don't have any items in your cart yet.", "warning")
    
        return redirect(request.referrer or url_for("index.index"))
    
    # Authorization check
    if current_user.customer.id != cart.customer_id:
        abort(403)

    # 4. Look for the CartItem that corresponds to this item
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        menu_item_id=item.id
    ).first()

    # If it's not in the cart, nothing to decrement
    if cart_item is None:
        flash("This item is not currently in your cart.", "warning")

        return redirect(request.referrer or url_for("index.index"))

    # 5. Decrement the quantity
    cart_item.quantity -= 1

    # 6. If quantity goes to zero or below, remove the item from the cart
    if cart_item.quantity <= 0:
        db.session.delete(cart_item)

    db.session.commit()

    flash("Item quantity updated.", "success")

    return redirect(request.referrer or url_for("index.index"))


def build_components(main_components: list) -> dict:
    return {
        "header": [safe_render_component(navbar_component)],
        "main": [safe_render_component(c) for c in main_components],
        "footer": [safe_render_component(footer_component)],
    }


def build_components_for_restaurant_page(
        main_components: list, aside_components: list
) -> dict:
    return {
        "header": [safe_render_component(navbar_component)],
        "main": [safe_render_component(mc) for mc in main_components],
        "aside": [safe_render_component(ac) for ac in aside_components],
        "footer": [safe_render_component(footer_component)],
    }
