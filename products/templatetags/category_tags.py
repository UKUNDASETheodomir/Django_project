from django import template

register = template.Library()

@register.filter
def get_icon(category_name):
    """
    Returns a Bootstrap icon class based on the category name.
    """
    if not category_name:
        return 'bi-tag'
        
    name = category_name.lower()
    
    icons = {
        'electronics': 'bi-laptop',
        'food': 'bi-basket',
        'movies': 'bi-film',
        'cars': 'bi-car-front',
        'other': 'bi-grid',
        
        # Legacy mappings
        'milk': 'bi-cup-straw',
        'milks': 'bi-cup-straw',
        'dairy': 'bi-droplet',
        'dairies': 'bi-droplet',
        'wine': 'bi-cup-straw',
        'wines': 'bi-cup-straw',
        'clothing': 'bi-bag-heart',
        'clothes': 'bi-bag-heart',
        'beauty': 'bi-stars',
        'delivery': 'bi-truck-flatbed',
        'baking': 'bi-egg-fried',
        'fruit': 'bi-apple',
        'fruits': 'bi-apple',
        'vegetable': 'bi-flower1',
        'vegetables': 'bi-flower1',
        'fresh': 'bi-brightness-high',
        'meat': 'bi-egg-fried',
        'seafood': 'bi-tsunami',
    }
    
    # Check for partial matches
    for key, icon in icons.items():
        if key in name:
            return icon
            
    return 'bi-tag' # Default icon
