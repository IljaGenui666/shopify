# Builds catalog.csv (one row per photo) and shopify-import.csv (Shopify product template)
# from the photos in this folder. Product names are generic test names (no brand names).
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = sys.argv[1] if len(sys.argv) > 1 else 'PASTE_SHOPIFY_FILES_URL_HERE/'
f = lambda n: f'photo_{n}_2026-10-18_19-10-55.jpg'
CL = ['S', 'M', 'L', 'XL']; SH = ['40', '41', '42', '43', '44', '45']
# handle, title, category, type, price, sizes, [(color, [photo numbers])], lifestyle photos
P = [
 ('quilted-puffer-jacket', 'Quilted Puffer Jacket', 'Outerwear', 'Jackets', 289, CL,
   [('Sky Blue', [3]), ('Stone Grey', [4, 7, 8]), ('Burgundy', [6])], [1]),
 ('quilted-puffer-vest', 'Quilted Puffer Vest', 'Outerwear', 'Vests', 219, CL, [('Mixed colours', [5])], []),
 ('padded-gilet', 'Padded Gilet', 'Outerwear', 'Vests', 249, CL,
   [('Burgundy', [14]), ('Olive', [15]), ('Navy', [16])], []),
 ('hybrid-down-hoodie-jacket', 'Hybrid Down Hoodie Jacket', 'Outerwear', 'Jackets', 329, CL,
   [('Black', [42, 46, 45]), ('White', [43]), ('Navy', [44])], [41]),
 ('contrast-trim-long-sleeve', 'Contrast Trim Long Sleeve', 'Sweatshirts', 'Long sleeves', 89, CL,
   [('Navy', [9, 11, 12, 13]), ('Black', [10])], []),
 ('crest-long-sleeve-black', 'Crest Embroidered Long Sleeve — Black', 'Sweatshirts', 'Long sleeves', 79, CL,
   [('Black', [27, 31, 29, 30, 28, 32])], []),
 ('camo-hoodie', 'Camo Hoodie', 'Sweatshirts', 'Hoodies', 129, CL,
   [('Camo', [33, 35, 34, 36, 37, 38, 39, 40])], []),
 ('low-top-trainer-tan-suede', 'Low-Top Trainer — Tan Suede', 'Shoes', 'Sneakers', 159, SH, [('Tan', [17])], []),
 ('low-top-trainer-sage', 'Low-Top Trainer — Sage', 'Shoes', 'Sneakers', 159, SH, [('Sage', [18])], []),
 ('low-top-trainer-brown-white', 'Low-Top Trainer — Brown / White', 'Shoes', 'Sneakers', 169, SH, [('Brown', [19])], []),
 ('low-top-trainer-olive', 'Low-Top Trainer — Olive', 'Shoes', 'Sneakers', 159, SH, [('Olive', [20])], []),
 ('low-top-trainer-chocolate', 'Low-Top Trainer — Chocolate', 'Shoes', 'Sneakers', 159, SH, [('Chocolate', [21])], []),
 ('low-top-trainer-magenta', 'Low-Top Trainer — Magenta', 'Shoes', 'Sneakers', 159, SH, [('Magenta', [22])], []),
 ('low-top-trainer-pink', 'Low-Top Trainer — Pink', 'Shoes', 'Sneakers', 159, SH, [('Pink', [23])], []),
 ('low-top-trainer-brown-leather', 'Low-Top Trainer — Brown Leather', 'Shoes', 'Sneakers', 169, SH, [('Brown', [24])], []),
 ('low-top-trainer-green', 'Low-Top Trainer — Green', 'Shoes', 'Sneakers', 159, SH, [('Green', [25])], []),
 ('low-top-trainer-blossom', 'Low-Top Trainer — White Blossom', 'Shoes', 'Sneakers', 179, SH, [('White', [26])], []),
 ('top-handle-leather-bag', 'Top Handle Leather Bag', 'Bags', 'Handbags', 349, ['One size'],
   [('Black', [53, 47]), ('Pink', [48]), ('Tan', [49]), ('Taupe', [50]), ('Cream', [51]), ('Brown', [52])], []),
 ('porcelain-cup-saucer-set', 'Porcelain Cup & Saucer Set', 'Tableware', 'Cups', 119, ['Set of 2'],
   [('White / Multicolour', [55, 54, 56])], []),
]
# 1) catalog.csv — one row per photo
rows = []
used = set()
for h, t, cat, typ, price, sizes, colors, life in P:
    for color, nums in colors:
        for k, n in enumerate(nums):
            rows.append([f(n), t, h, cat, typ, color, 'main' if k == 0 else 'detail', price]); used.add(f(n))
    for n in life:
        rows.append([f(n), t, h, cat, typ, 'all', 'lifestyle', price]); used.add(f(n))
rows.append(['photo_2026-10-18_19-07-51.jpg', 'Quilted Puffer Jacket / Vest', '', 'Outerwear', '', 'all', 'duplicate of photo_2 (not used)', ''])
rows.append([f(2), 'Quilted Puffer Jacket / Vest', '', 'Outerwear', '', 'all', 'collection banner (rack)', ''])
with open(os.path.join(HERE, 'catalog.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['file', 'product', 'handle', 'category', 'type', 'color', 'photo role', 'price EUR']); w.writerows(rows)
missing = sorted(set(os.listdir(HERE)) - used - {'photo_2026-10-18_19-07-51.jpg', f(2)} - {x for x in os.listdir(HERE) if not x.endswith('.jpg')})
# 2) shopify-import.csv — Shopify product template columns + Collection
cols = ['Title','URL handle','Description','Vendor','Product category','Type','Tags','Published on online store','Status','SKU','Variant Barcodes','Option1 name','Option1 value','Option1 Linked To','Option2 name','Option2 value','Option2 Linked To','Option3 name','Option3 value','Option3 Linked To','Price','Compare-at price','Cost per item','Charge tax','Tax code','Unit price total measure','Unit price total measure unit','Unit price base measure','Unit price base measure unit','Inventory tracker','Inventory quantity','Continue selling when out of stock','Weight value (grams)','Weight unit for display','Requires shipping','Fulfillment service','Product image URL','Image position','Image alt text','Variant image URL','Gift card','SEO title','SEO description','Color (product.metafields.shopify.color-pattern)','Google Shopping / Google product category','Google Shopping / Gender','Google Shopping / Age group','Google Shopping / Manufacturer part number (MPN)','Google Shopping / Ad group name','Google Shopping / Ads labels','Google Shopping / Condition','Google Shopping / Custom product','Google Shopping / Custom label 0','Google Shopping / Custom label 1','Google Shopping / Custom label 2','Google Shopping / Custom label 3','Google Shopping / Custom label 4','Packed product length','Packed product width','Packed product height','Packed product dimension unit','Collection']
WEIGHT = {'Outerwear': 1200, 'Sweatshirts': 400, 'Shoes': 1300, 'Bags': 1000, 'Tableware': 900}
out = []
for h, t, cat, typ, price, sizes, colors, life in P:
    images = [n for _, nums in colors for n in nums] + life
    multi_color = len(colors) > 1
    variants = [(c, s, nums[0]) for c, nums in colors for s in sizes]
    for i, (color, size, vimg) in enumerate(variants):
        r = dict.fromkeys(cols, '')
        r.update({'URL handle': h, 'SKU': f"{h.upper()}-{color[:3].upper()}-{size.replace(' ', '').upper()}",
                  'Option1 value': size, 'Price': f'{price:.2f}', 'Charge tax': 'TRUE', 'Inventory tracker': 'shopify',
                  'Inventory quantity': '10', 'Continue selling when out of stock': 'DENY',
                  'Weight value (grams)': str(WEIGHT[cat]), 'Weight unit for display': 'g', 'Requires shipping': 'TRUE',
                  'Fulfillment service': 'manual'})
        if multi_color:
            r.update({'Option2 value': color, 'Variant image URL': BASE + f(vimg)})
        if i == 0:
            r.update({'Title': t, 'Description': f'<p>Test product for the store preview. Replace with your own description.</p>',
                      'Vendor': 'Test catalog', 'Type': typ, 'Tags': f'test, {cat}, {typ}', 'Published on online store': 'TRUE',
                      'Status': 'Active', 'Option1 name': 'Size', 'Gift card': 'FALSE', 'Collection': cat})
            if multi_color: r['Option2 name'] = 'Color'
        if i < len(images):
            r.update({'Product image URL': BASE + f(images[i]), 'Image position': str(i + 1), 'Image alt text': t})
        out.append(r)
    # extra image rows if more images than variants
    for j in range(len(variants), len(images)):
        r = dict.fromkeys(cols, ''); r.update({'URL handle': h, 'Product image URL': BASE + f(images[j]), 'Image position': str(j + 1), 'Image alt text': t}); out.append(r)
with open(os.path.join(HERE, 'shopify-import.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(out)
print(len(P), 'products,', len(out), 'import rows,', len(rows), 'photo rows; unassigned photos:', missing)
