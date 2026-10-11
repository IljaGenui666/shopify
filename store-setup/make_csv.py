# Generates products.csv (Shopify product import format) from products.json
import csv, json, os
here = os.path.dirname(os.path.abspath(__file__))
products = json.load(open(os.path.join(here, 'products.json')))
IMG = 'https://images.unsplash.com/photo-{}?w=1600&h=2000&fit=crop&q=80&fm=jpg'
cols = ['Title','URL handle','Description','Vendor','Type','Tags','Published on online store','Status','SKU','Option1 name','Option1 value','Price','Compare-at price','Charge tax','Inventory tracker','Inventory quantity','Requires shipping','Fulfillment service','Product image URL','Image position','Image alt text','Collection']
rows = []
for p in products:
    sizes = p.get('sizes', ['S','M','L','XL'])
    desc = f"<p>{p['desc']}</p><ul><li>Relaxed streetwear fit</li><li>100% cotton unless stated otherwise</li></ul>"
    for i, size in enumerate(sizes):
        r = dict.fromkeys(cols, '')
        r.update({'URL handle': p['handle'], 'Option1 name': 'Size', 'Option1 value': size,
                  'SKU': f"{p['handle'].upper()[:20]}-{size.replace(' ','').upper()}",
                  'Price': f"{p['price']:.2f}", 'Compare-at price': f"{p['compare']:.2f}" if p.get('compare') else '',
                  'Charge tax': 'TRUE', 'Inventory tracker': 'shopify', 'Inventory quantity': '20',
                  'Requires shipping': 'TRUE', 'Fulfillment service': 'manual'})
        if i == 0:
            r.update({'Title': p['title'], 'Description': desc, 'Type': p['type'],
                      'Tags': ', '.join(['streetwear', p['type'].lower()] + (['sale'] if p.get('compare') else [])),
                      'Published on online store': 'TRUE', 'Status': 'active', 'Collection': p['type']})
        if i < len(p['imgs']):
            r.update({'Product image URL': IMG.format(p['imgs'][i]), 'Image position': str(i+1), 'Image alt text': p['title']})
        rows.append(r)
with open(os.path.join(here, 'products.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(products), 'products,', len(rows), 'rows')
