from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.products.models import Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial prototype categories, products with rich attributes & SKUs, and admin/customer accounts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Phase 1 database seeding...'))

        # Create Admin User if not present
        admin_email = 'admin@swastik.com'
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password='Admin@12345',
                name='Swastik Admin',
                mobile_number='9999999999',
                whatsapp_number='9999999999'
            )
            self.stdout.write(self.style.SUCCESS(f'Created Admin user: {admin_email} (Password: Admin@12345)'))

        # Create Sample Customer User if not present
        customer_email = 'customer@swastik.com'
        if not User.objects.filter(email=customer_email).exists():
            User.objects.create_user(
                username='customer',
                email=customer_email,
                password='CustomerPass123',
                name='John Customer',
                mobile_number='9876543210',
                whatsapp_number='9876543210',
                addresses=[
                    {
                        "type": "Home",
                        "address_line1": "Flat 402, Sunshine Apartments",
                        "city": "Jaipur",
                        "pincode": "302001",
                        "is_default": True
                    }
                ]
            )
            self.stdout.write(self.style.SUCCESS(f'Created Customer user: {customer_email} (Password: CustomerPass123)'))

        # Define 4 core categories mapped to 4 sectors
        categories_data = [
            {
                'name': 'Bakery',
                'sector': 'BAKERY',
                'description': 'Freshly baked breads, artisanal cakes, cookies, and pastries.',
                'metadata': {
                    'supports_preorder': True,
                    'supports_customization': True,
                    'popular_subcategories': ['Breads', 'Cakes', 'Pastries', 'Cookies']
                }
            },
            {
                'name': 'Dairy / Milk',
                'sector': 'DAIRY',
                'description': 'Pure farm-fresh milk, paneer, fresh curd, ghee, and butter.',
                'metadata': {
                    'supports_subscriptions': True,
                    'subscription_frequencies': ['Daily', 'Alternate Days', 'Weekly', 'Monthly'],
                    'popular_subcategories': ['Milk', 'Curd & Lassi', 'Paneer & Butter', 'Ghee']
                }
            },
            {
                'name': 'Sweets',
                'sector': 'SWEETS',
                'description': 'Authentic traditional sweets, mithai, rasgulla, and gulab jamun.',
                'metadata': {
                    'weight_based_pricing': True,
                    'supports_gift_packs': True,
                    'popular_subcategories': ['Syrup Sweets', 'Dry Mithai', 'Ghee Sweets', 'Festival Packs']
                }
            },
            {
                'name': 'Confectionery',
                'sector': 'CONFECTIONERY',
                'description': 'Crispy savouries, namkeens, chocolates, chips, and beverages.',
                'metadata': {
                    'supports_combos': True,
                    'popular_subcategories': ['Namkeen & Savouries', 'Chocolates', 'Biscuits', 'Beverages']
                }
            }
        ]

        created_categories = {}
        for cat_info in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_info['name'],
                defaults={
                    'sector': cat_info['sector'],
                    'description': cat_info['description'],
                    'metadata': cat_info['metadata'],
                    'is_active': True
                }
            )
            created_categories[cat_info['sector']] = category
            status_str = 'Created' if created else 'Already exists'
            self.stdout.write(f'Category "{category.name}": {status_str}')

        # Define initial prototype products across all 4 business sectors with rich fields
        products_data = [
            # BAKERY SECTOR
            {
                'sku': 'SW-BAK-001',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Breads',
                'name': 'Whole Wheat Milk Bread',
                'description': 'Freshly baked soft whole wheat loaf rich in fiber and milk goodness.',
                'price': 40.00,
                'discount_price': 36.00,
                'tax_percentage': 5.00,
                'unit': '400 g',
                'stock_quantity': 150,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['fresh', 'daily-essential', 'whole-wheat'],
                'attributes': {
                    'shelf_life_days': 3,
                    'eggless': True,
                    'storage': 'Keep in a cool dry place'
                }
            },
            {
                'sku': 'SW-BAK-002',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Cakes',
                'name': 'Belgian Chocolate Truffle Cake',
                'description': 'Rich dark chocolate layer cake topped with decadent truffle icing.',
                'price': 550.00,
                'discount_price': 499.00,
                'tax_percentage': 18.00,
                'unit': '500 g',
                'stock_quantity': 25,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['bestseller', 'customizable', 'premium'],
                'attributes': {
                    'flavour': 'Dark Chocolate Truffle',
                    'eggless': True,
                    'custom_message_supported': True,
                    'advance_order_hours': 4
                }
            },
            # DAIRY SECTOR
            {
                'sku': 'SW-DAI-001',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Milk',
                'name': 'Full Cream Fresh Milk',
                'description': 'Pasteurized rich full cream milk delivered fresh every morning.',
                'price': 68.00,
                'discount_price': 65.00,
                'tax_percentage': 0.00,
                'unit': '1 L',
                'stock_quantity': 500,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['subscription-eligible', 'daily-fresh', 'pure-milk'],
                'attributes': {
                    'fat_content': '6.0%',
                    'snf_content': '9.0%',
                    'subscription_eligible': True,
                    'delivery_window': 'Morning 6:00 AM - 8:00 AM'
                }
            },
            {
                'sku': 'SW-DAI-002',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Paneer & Butter',
                'name': 'Fresh Malai Paneer',
                'description': 'Soft and creamy malai paneer cubes ideal for traditional curries.',
                'price': 120.00,
                'discount_price': 110.00,
                'tax_percentage': 0.00,
                'unit': '200 g',
                'stock_quantity': 80,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['protein-rich', 'fresh-made'],
                'attributes': {
                    'shelf_life_days': 5,
                    'refrigeration_required': True
                }
            },
            # SWEETS SECTOR
            {
                'sku': 'SW-SWT-001',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Syrup Sweets',
                'name': 'Kolkata Special Rasgulla',
                'description': 'Spongy soft cottage cheese balls soaked in light aromatic sugar syrup.',
                'price': 320.00,
                'discount_price': 299.00,
                'tax_percentage': 5.00,
                'unit': '1 kg',
                'stock_quantity': 40,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['traditional', 'festive-favorite', 'bestseller'],
                'attributes': {
                    'piece_count_approx': '16-18 Pcs',
                    'shelf_life_days': 7,
                    'packaging': 'Sealed Tin Box'
                }
            },
            {
                'sku': 'SW-SWT-002',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Ghee Sweets',
                'name': 'Desi Ghee Motichoor Ladoo',
                'description': 'Mouthwatering fine boondi ladoos made with pure desi ghee and saffron.',
                'price': 450.00,
                'discount_price': 420.00,
                'tax_percentage': 5.00,
                'unit': '500 g',
                'stock_quantity': 60,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['pure-ghee', 'mithai'],
                'attributes': {
                    'ghee_type': 'Pure Cow Desi Ghee',
                    'shelf_life_days': 15
                }
            },
            # CONFECTIONERY SECTOR
            {
                'sku': 'SW-CNF-001',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Namkeen & Savouries',
                'name': 'Special Ratlami Sev',
                'description': 'Spicy crispy gram flour savouries blended with authentic clove and spices.',
                'price': 140.00,
                'discount_price': 130.00,
                'tax_percentage': 12.00,
                'unit': '400 g',
                'stock_quantity': 200,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['spicy', 'crispy-namkeen', 'tea-time'],
                'attributes': {
                    'spice_level': 'Medium High',
                    'shelf_life_months': 4
                }
            },
            {
                'sku': 'SW-CNF-002',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Chocolates',
                'name': 'Handcrafted Chocolate Assortment',
                'description': 'Premium box of milk, dark, and hazelnut filled chocolates.',
                'price': 350.00,
                'discount_price': 320.00,
                'tax_percentage': 18.00,
                'unit': '250 g',
                'stock_quantity': 45,
                'is_available': True,
                'brand': 'Swastik Confectionery',
                'tags': ['gift-pack', 'chocolates', 'premium'],
                'attributes': {
                    'piece_count': 12,
                    'contains_nuts': True
                }
            }
        ]

        for prod_info in products_data:
            product, created = Product.objects.get_or_create(
                sku=prod_info['sku'],
                defaults={
                    'name': prod_info['name'],
                    'category': prod_info['category'],
                    'subcategory_name': prod_info['subcategory_name'],
                    'description': prod_info['description'],
                    'price': prod_info['price'],
                    'discount_price': prod_info['discount_price'],
                    'tax_percentage': prod_info['tax_percentage'],
                    'unit': prod_info['unit'],
                    'stock_quantity': prod_info['stock_quantity'],
                    'is_available': prod_info['is_available'],
                    'is_active': True,
                    'brand': prod_info['brand'],
                    'tags': prod_info['tags'],
                    'attributes': prod_info['attributes']
                }
            )
            status_str = 'Created' if created else 'Already exists'
            self.stdout.write(f'Product [{product.sku}] "{product.name}": {status_str}')

        self.stdout.write(self.style.SUCCESS('Successfully completed Phase 1 database seeding with rich schemas!'))
