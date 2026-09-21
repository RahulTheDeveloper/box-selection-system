from itertools import permutations

from .models import Box


def dimensions_fit(
    product_length,
    product_width,
    product_height,
    box_length,
    box_width,
    box_height,
):
    product_dimensions = [
        product_length,
        product_width,
        product_height,
    ]

    box_dimensions = [
        box_length,
        box_width,
        box_height,
    ]

    for orientation in permutations(product_dimensions):
        if all(
            orientation[index] <= box_dimensions[index]
            for index in range(3)
        ):
            return True

    return False


def is_box_suitable(product, box):
    if product.weight > box.max_weight:
        return False

    return dimensions_fit(
        product.length,
        product.width,
        product.height,
        box.length,
        box.width,
        box.height,
    )


def get_suitable_boxes(product):
    boxes = Box.objects.all()

    suitable_boxes = []

    for box in boxes:
        if is_box_suitable(product, box):
            suitable_boxes.append(box)

    return suitable_boxes


def calculate_order_volume(order):
    total_volume = 0

    for item in order.items.select_related("product").all():
        product = item.product

        product_volume = (
            product.length
            * product.width
            * product.height
        )

        total_volume += product_volume * item.quantity

    return total_volume


def calculate_order_weight(order):
    total_weight = 0

    for item in order.items.select_related("product").all():
        total_weight += item.product.weight * item.quantity

    return total_weight


def get_suitable_boxes_for_order(order):
    if not order.items.exists():
        return []

    total_volume = calculate_order_volume(order)
    total_weight = calculate_order_weight(order)

    suitable_boxes = []

    for box in Box.objects.all():

        box_volume = (
            box.length
            * box.width
            * box.height
        )

        # Check total volume
        if total_volume > box_volume:
            continue

        # Check total weight
        if total_weight > box.max_weight:
            continue

        order_fits = True

        # Check every product's dimensions
        for item in order.items.select_related("product").all():

            product = item.product

            if not dimensions_fit(
                product.length,
                product.width,
                product.height,
                box.length,
                box.width,
                box.height,
            ):
                order_fits = False
                break

        if order_fits:
            suitable_boxes.append(box)

    return suitable_boxes


def recommend_box(order):
    suitable_boxes = get_suitable_boxes_for_order(order)

    if not suitable_boxes:
        return None

    # Smallest volume first.
    # If volume is same, lower cost first.
    suitable_boxes.sort(
        key=lambda box: (
            box.length * box.width * box.height,
            box.cost,
        )
    )

    return suitable_boxes[0]