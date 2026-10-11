# Generates products.csv for Shopify import from products.json.
# Columns follow store-setup/shopify_product_template.csv (Shopify's own template) exactly,
# plus a "Collection" column at the end (creates the collection on import).
import csv, json, os
here = os.path.dirname(os.path.abspath(__file__))
products = json.load(open(os.path.join(here, 'products.json'), encoding='utf-8'))
with open(os.path.join(here, 'shopify_product_template.csv'), encoding='utf-8-sig') as f:
    cols = next(csv.reader(f))
cols = cols + ['Collection']
IMG = 'https://images.unsplash.com/photo-{}?w=1600&h=2000&fit=crop&q=80&fm=jpg'
WEIGHT = {'Hoodies': 700, 'T-shirts': 250, 'Bottoms': 600, 'Outerwear': 1000, 'Accessories': 120}
rows = []
for p in products:
    sizes = p.get('sizes', ['S', 'M', 'L', 'XL'])
    desc = f"<p>{p['desc']}</p><ul><li>Relaxed streetwear fit</li><li>100% cotton unless stated otherwise</li></ul>"
    for i, size in enumerate(sizes):
        r = dict.fromkeys(cols, '')
        r.update({
            'URL handle': p['handle'],
            'SKU': f"{p['handle'].upper()}-{size.replace(' ', '').upper()}",
            'Option1 value': size,
            'Price': f"{p['price']:.2f}",
            'Compare-at price': f"{p['compare']:.2f}" if p.get('compare') else '',
            'Charge tax': 'TRUE',
            'Inventory tracker': 'shopify',
            'Inventory quantity': '20',
            'Continue selling when out of stock': 'DENY',
            'Weight value (grams)': str(WEIGHT.get(p['type'], 500)),
            'Weight unit for display': 'g',
            'Requires shipping': 'TRUE',
            'Fulfillment service': 'manual',
        })
        if i == 0:
            r.update({
                'Title': p['title'], 'Description': desc, 'Vendor': 'My Store', 'Type': p['type'],
                'Tags': ', '.join(['Streetwear', p['type']] + (['Sale'] if p.get('compare') else [])),
                'Published on online store': 'TRUE', 'Status': 'Active', 'Option1 name': 'Size',
                'Gift card': 'FALSE', 'Collection': p['type'],
            })
        if i < len(p['imgs']):
            r.update({'Product image URL': IMG.format(p['imgs'][i]), 'Image position': str(i + 1), 'Image alt text': p['title']})
        rows.append(r)
with open(os.path.join(here, 'products.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print(len(products), 'products,', len(rows), 'rows,', len(cols), 'columns')
