# inventory/templatetags/inventory_extras.py

from django import template

register = template.Library()

@register.filter
def create_range(value):
    """
    Returns a list containing numbers from 0 up to value-1.
    Useful for looping a specific number of times in templates.
    Example: 5|create_range would return [0, 1, 2, 3, 4]
    """
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return [] # Return an empty list if value is not a valid integer

@register.filter
def sub(value, arg):
    """
    Subtracts the arg from the value.
    Example: 10|sub:3 would return 7.
    Handles non-numeric inputs gracefully.
    """
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return '' # Return empty string on error

@register.filter
def dict_get(dictionary, key):
    """
    Allows dictionary lookup by key, object attribute access, or list indexing
    in Django templates. Handles cases where the key/attribute/index might not exist
    by returning an empty string.
    Example: my_dict|dict_get:'my_key', my_object|dict_get:'my_attribute', my_list|dict_get:0
    """
    if isinstance(dictionary, dict):
        # Handle dictionary key lookup
        return dictionary.get(key, '')
    elif isinstance(key, int) and hasattr(dictionary, '__getitem__'):
        # Handle list/tuple indexing with integer key
        try:
            return dictionary[key]
        except (IndexError, TypeError):
            return '' # Index out of bounds or not indexable
    elif hasattr(dictionary, key):
        # Handle object attribute access with string key
        return getattr(dictionary, key)
    return '' # Default if none of the above apply

@register.filter
def get_total_samples(officer_list):
    """Calculates the total number of samples for a list of officer entries."""
    total = 0
    for officer in officer_list:
        total += len(officer.get('samples', []))
    return total

@register.filter
def get_officers_count(stores_list):
    """Calculates the total number of distinct officers across all stores in a region."""
    count = 0
    for store in stores_list:
        count += len(store.get('officers', []))
    return count

@register.filter
def get_stores_count(regions_list):
    """Calculates the total number of distinct stores across all regions."""
    count = 0
    for region in regions_list:
        count += len(region.get('stores', []))
    return count

@register.filter
def add_to_sum(value, arg):
    """Custom filter to add a value to a running sum for {% with %} blocks."""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return value  # Return original value if conversion fails

@register.filter
def split(value, delimiter=' '):
    """Splits a string by a delimiter and returns a list."""
    if isinstance(value, str):
        return value.split(delimiter)
    return value # Return original value if not a string