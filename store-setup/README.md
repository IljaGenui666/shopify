# Store setup (not part of the theme)

Shopify ignores this folder when it syncs the theme.

- `products.json` — the 18 demo streetwear products (source of truth).
- `make_csv.py` — turns `products.json` into `products.csv`.
- `products.csv` — import in Shopify admin: Products → Import.
  Creates the products with S/M/L/XL sizes and the collections
  Hoodies, T-shirts, Bottoms, Outerwear, Accessories (column "Collection").

Photos are free-licensed images from Unsplash (https://unsplash.com/license),
loaded by Shopify from the URLs in the CSV. They are demo images for a test
store: replace them with photos of your real products before selling.

Images to upload by hand in Customize (image_picker settings cannot be set from Git):
- Home → Image banner: https://unsplash.com/photos/two-people-sitting-on-the-hood-of-a-car (photo-1635650805023-f2529440b5aa)
- Home → Image with text: photo-1739384994765-d44f7af12029
