from Alibaba.models import ProductModel, Category  # Replace 'yourapp' with your actual app name

# List of all product data
product_data = [
    {'id': 1, 'title': 'Fjallraven - Foldsack No. 1 Backpack', 'selling_price': 109.95, 'discount': 10.5, 'description': 'Perfect pack for everyday use.', 'category_id': 1, 'product_image': 'proImage/Fjallraven_-_Foldsack_No_hPxn4mu._1_Backpack.jpg', 'composition': ''},
    {'id': 2, 'title': 'Mens Casual Premium Slim Fit T-Shirts', 'selling_price': 22.3, 'discount': 5.2, 'description': 'Slim-fitting style, lightweight fabric.', 'category_id': 1, 'product_image': 'proImage/shirt_RIfXOD3.jpg', 'composition': 'xuycj'},
    {'id': 3, 'title': 'Mens Cotton Jacket', 'selling_price': 55.99, 'discount': 8.0, 'description': 'Great for Spring/Autumn/Winter.', 'category_id': 1, 'product_image': 'proImage/Mens_Cotton_Jacket.png', 'composition': ''},
    {'id': 4, 'title': 'Mens Casual Slim Fit', 'selling_price': 15.99, 'discount': 3.5, 'description': 'The color could be slightly different.', 'category_id': 1, 'product_image': 'proImage/Mens_Casual_Slim_Fit.jpg', 'composition': ''},
    {'id': 5, 'title': "John Hardy Women's Legends Naga Bracelet", 'selling_price': 695.0, 'discount': 15.75, 'description': 'Inspired by the mythical water dragon.', 'category_id': 3, 'product_image': 'proImage/Solid_Gold_Petite_Micropave.jpg', 'composition': ''},
    {'id': 6, 'title': 'Solid Gold Petite Micropave', 'selling_price': 168.0, 'discount': 12.1, 'description': 'Satisfaction Guaranteed. Return within 30 days.', 'category_id': 3, 'product_image': 'proImage/Solid_Gold_Petite_Micropave_ring.jpg', 'composition': ''},
    {'id': 7, 'title': 'Fjallraven - Foldsack No. 1 Backpack', 'selling_price': 109.95, 'discount': 10.5, 'description': 'Perfect pack for everyday use.', 'category_id': 1, 'product_image': 'proImage/Fjallraven_-_Foldsack_No._1_Backpack_black.jpg', 'composition': ''},
    {'id': 8, 'title': 'Mens Casual Premium Slim Fit T-Shirts', 'selling_price': 22.3, 'discount': 5.2, 'description': 'Slim-fitting style, lightweight fabric.', 'category_id': 1, 'product_image': 'proImage/white_Mens_Casual_Premium_Slim_Fit_T-Shirts.jpg', 'composition': ''},
    {'id': 9, 'title': 'Mens Cotton Jacket', 'selling_price': 55.99, 'discount': 8.0, 'description': 'Great for Spring/Autumn/Winter.', 'category_id': 1, 'product_image': 'proImage/Mens_Cotton_Jacket_ek8Aw9Z.png', 'composition': ''},
    {'id': 10, 'title': 'Mens Casual Slim Fit', 'selling_price': 15.99, 'discount': 3.5, 'description': 'The color could be slightly different.', 'category_id': 1, 'product_image': 'proImage/Mens_Casual_Slim.png', 'composition': ''},
    {'id': 11, 'title': "John Hardy Women's Legends Naga Bracelet", 'selling_price': 695.0, 'discount': 15.75, 'description': 'Inspired by the mythical water dragon.', 'category_id': 3, 'product_image': 'proImage/4braclate.png', 'composition': ''},
    {'id': 12, 'title': 'Solid Gold Petite Micropave', 'selling_price': 168.0, 'discount': 12.1, 'description': 'Satisfaction Guaranteed. Return within 30 days.', 'category_id': 3, 'product_image': 'proImage/silver.jpg', 'composition': 'xyz'},
    {'id': 13, 'title': 'Fjallraven - Foldsack No. 1 Backpack', 'selling_price': 109.95, 'discount': 10.2, 'description': 'Perfect pack for everyday use', 'category_id': 1, 'product_image': 'proImage/beautiShirts_FhI6m7a.jpg', 'composition': 'xyz'},
    {'id': 14, 'title': "BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats", 'selling_price': 56.99, 'discount': 0.0, 'description': 'Detachable functional liner: Skin friendly, lightweight and warm. 3-in-1 detachable design for all seasons.', 'category_id': 3, 'product_image': 'proImage/51Y5NI-I5jL._AC_UX679_.png', 'composition': '100% Polyester; Warm Fleece'},
    {'id': 15, 'title': "Lock and Love Women's Removable Hooded Faux Leather Moto Biker Jacket", 'selling_price': 29.95, 'discount': 0.0, 'description': 'Faux leather material for style and comfort. Denim-style with removable hoodie.', 'category_id': 3, 'product_image': 'proImage/81XH0e8fefL._AC_UY879_.png', 'composition': '100% Polyurethane shell, 100% Polyester lining'},
    {'id': 16, 'title': 'Rain Jacket Women Windbreaker Striped Climbing Raincoats', 'selling_price': 39.99, 'discount': 0.0, 'description': 'Lightweight raincoat with adjustable drawstring waist and lined hood.', 'category_id': 2, 'product_image': 'proImage/71HblAHs5xL._AC_UY879_-2.png', 'composition': 'Cotton lined hood, polyester body'},
    {'id': 17, 'title': "MBJ Women's Solid Short Sleeve Boat Neck V", 'selling_price': 9.85, 'discount': 0.0, 'description': 'Lightweight fabric with great stretch for comfort. Ribbed sleeves and neckline.', 'category_id': 2, 'product_image': 'proImage/71z3kpMAYsL._AC_UY879_.png', 'composition': '95% Rayon, 5% Spandex'},
    {'id': 18, 'title': "Opna Women's Short Sleeve Moisture", 'selling_price': 7.95, 'discount': 0.0, 'description': 'Breathable and moisture-wicking short sleeve for comfort and movement.', 'category_id': 2, 'product_image': 'proImage/51eg55uWmdL._AC_UX679_.png', 'composition': '100% Cationic Polyester'},
    {'id': 19, 'title': 'DANVOUY Womens T Shirt Casual Cotton Short', 'selling_price': 12.99, 'discount': 0.0, 'description': 'Soft casual T-shirt with letter print and slight stretch for everyday wear.', 'category_id': 2, 'product_image': 'proImage/61pHAEJ4NML._AC_UX679_.png', 'composition': '95% Cotton, 5% Spandex'}
]

# Insert data
for item in product_data:
    category = Category.objects.get(id=item['category_id'])
    ProductModel.objects.create(
        title=item['title'],
        selling_price=item['selling_price'],
        discount=item['discount'],
        description=item['description'],
        category=category,
        product_image=item['product_image'],
        composition=item['composition']
    )

print("✅ All 19 product records inserted successfully.")
