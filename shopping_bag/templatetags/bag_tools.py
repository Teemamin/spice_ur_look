from django import template


register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity


@register.filter(name='calc_delivery')
def calc_delivery(total, fixeddelivery):
    return float(total) + float(fixeddelivery)