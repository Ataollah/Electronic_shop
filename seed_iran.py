import os
import json
import django
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eshop.settings')
django.setup()

# Path to the JSON file
JSON_FILE = os.path.join(os.path.dirname(__file__), 'iran', 'json', 'provinces.json')

# Get the Province model from the iran app
Province = apps.get_model('iran', 'Province')

# def convert_foreign_keys(model, item):
#     """
#     Convert *_id keys in item dict to the correct ForeignKey field names for the given model.
#     """
#     opts = model._meta
#     new_item = item.copy()
#     for field in opts.fields:
#         if field.is_relation and field.many_to_one:
#             fk_name = field.name
#             fk_id_key = f"{fk_name}_id"
#             if fk_id_key in new_item:
#                 new_item[fk_name] = new_item.pop(fk_id_key)
#     # Special case: if model is City and 'province_id' is present, map it to 'county'
#     if model.__name__ == 'City' and 'province_id' in new_item:
#         new_item['county'] = new_item.pop('province_id')
#     return new_item

with open(JSON_FILE, encoding='utf-8') as f:
    data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    for item in data:
        Province.objects.update_or_create(**item)
print("Seeded Province from provinces.json")


# Get the County model from the iran app
County = apps.get_model('iran', 'County')
with open(os.path.join(os.path.dirname(__file__), 'iran', 'json', 'counties.json'), encoding='utf-8') as f:
    data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    for item in data:
        County.objects.update_or_create(**item)
print("Seeded County from counties.json")



# Get the City model from the iran app
City = apps.get_model('iran', 'City')
with open(os.path.join(os.path.dirname(__file__), 'iran', 'json', 'cities.json'), encoding='utf-8') as f:
    data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    existing_slugs = set(City.objects.values_list('slug', flat=True))
    for item in data:
        item.pop('province_id', None)
        original_slug = item['slug']
        slug = original_slug
        counter = 1
        while slug in existing_slugs:
            slug = f"{original_slug}{counter}"
            counter += 1
        item['slug'] = slug
        existing_slugs.add(slug)
        City.objects.update_or_create(id=item['id'], defaults=item)
print("Seeded City from cities.json")

# Get the District model from the iran app
District = apps.get_model('iran', 'District')
with open(os.path.join(os.path.dirname(__file__), 'iran', 'json', 'districts.json'), encoding='utf-8') as f:
    data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    existing_slugs = set(District.objects.values_list('slug', flat=True))
    for item in data:
        item.pop('province_id', None)
        original_slug = item['slug']
        slug = original_slug
        counter = 1
        while slug in existing_slugs:
            slug = f"{original_slug}{counter}"
            counter += 1
        item['slug'] = slug
        existing_slugs.add(slug)
        District.objects.update_or_create(id=item['id'], defaults=item)
print("Seeded District from districts.json")

# Get the Rural model from the iran app
Rural = apps.get_model('iran', 'Rural')
with open(os.path.join(os.path.dirname(__file__), 'iran', 'json', 'rurals.json'), encoding='utf-8') as f:
    data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    existing_slugs = set(Rural.objects.values_list('slug', flat=True))
    for item in data:
        item.pop('province_id', None)
        original_slug = item['slug']
        slug = original_slug
        counter = 1
        while slug in existing_slugs:
            slug = f"{original_slug}{counter}"
            counter += 1
        item['slug'] = slug
        existing_slugs.add(slug)
        Rural.objects.update_or_create(id=item['id'], defaults=item)
print("Seeded Rural from rurals.json")
