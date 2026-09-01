from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.products.models import Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial prototype categories, 50 detailed products across all sectors, and superuser/customer accounts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Phase 1 database seeding...'))

        # Create/Update Requested Superuser
        superuser_email = 'Swastikartisanbakehouse@gmail.com'
        superuser_pass = 'ASHISH.kc1999'

        superuser, created = User.objects.get_or_create(email=superuser_email)
        superuser.username = 'swastik_admin'
        superuser.name = 'Swastik Artisan Bakehouse Admin'
        superuser.set_password(superuser_pass)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.is_active = True
        superuser.save()

        status_str = 'Created new' if created else 'Updated existing'
        self.stdout.write(self.style.SUCCESS(f'{status_str} Superuser: {superuser_email} (Password: {superuser_pass})'))

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
            self.stdout.write(self.style.SUCCESS(f'Created Customer user: {customer_email}'))

        # Define 4 core categories mapped to 4 sectors
        categories_data = [
            {
                'name': 'Bakery',
                'sector': 'BAKERY',
                'description': 'Freshly baked breads, artisanal cakes, cookies, pastries, and savory bakes.',
                'metadata': {
                    'supports_preorder': True,
                    'supports_customization': True,
                    'popular_subcategories': ['Breads', 'Cakes', 'Pastries', 'Cookies', 'Muffins & Bakes']
                }
            },
            {
                'name': 'Dairy / Milk',
                'sector': 'DAIRY',
                'description': 'Pure farm-fresh milk, paneer, fresh curd, ghee, butter, and daily dairy essentials.',
                'metadata': {
                    'supports_subscriptions': True,
                    'subscription_frequencies': ['Daily', 'Alternate Days', 'Weekly', 'Monthly'],
                    'popular_subcategories': ['Milk', 'Curd & Lassi', 'Paneer & Butter', 'Ghee', 'Cheese & Cream']
                }
            },
            {
                'name': 'Sweets',
                'sector': 'SWEETS',
                'description': 'Authentic traditional sweets, mithai, rasgulla, gulab jamun, and festive sweet boxes.',
                'metadata': {
                    'weight_based_pricing': True,
                    'supports_gift_packs': True,
                    'popular_subcategories': ['Syrup Sweets', 'Dry Mithai', 'Ghee Sweets', 'Festival Packs']
                }
            },
            {
                'name': 'Confectionery',
                'sector': 'CONFECTIONERY',
                'description': 'Crispy savouries, namkeens, chocolates, roasted nuts, biscuits, and beverages.',
                'metadata': {
                    'supports_combos': True,
                    'popular_subcategories': ['Namkeen & Savouries', 'Chocolates', 'Nuts & Dry Fruits', 'Biscuits & Wafers']
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
            cat_status = 'Created' if created else 'Already exists'
            self.stdout.write(f'Category "{category.name}": {cat_status}')

        # Define 50 rich products across all 4 business sectors
        products_data = [
            # ==================== BAKERY SECTOR (13 Products) ====================
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
                'attributes': {'shelf_life_days': 3, 'eggless': True, 'storage': 'Cool dry place'}
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
                'attributes': {'flavour': 'Dark Chocolate Truffle', 'eggless': True, 'custom_message': True}
            },
            {
                'sku': 'SW-BAK-003',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Breads',
                'name': 'Multigrain Artisanal Loaf',
                'description': 'Hearty bread packed with flaxseeds, sunflower seeds, and oats.',
                'price': 60.00,
                'discount_price': 55.00,
                'tax_percentage': 5.00,
                'unit': '400 g',
                'stock_quantity': 80,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['multigrain', 'healthy', 'high-fiber'],
                'attributes': {'shelf_life_days': 3, 'eggless': True}
            },
            {
                'sku': 'SW-BAK-004',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Pastries',
                'name': 'Red Velvet Cream Cheese Pastry',
                'description': 'Soft red velvet sponge layered with smooth cream cheese frosting.',
                'price': 120.00,
                'discount_price': 110.00,
                'tax_percentage': 18.00,
                'unit': '150 g',
                'stock_quantity': 40,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['pastry', 'dessert', 'eggless'],
                'attributes': {'refrigeration_required': True, 'eggless': True}
            },
            {
                'sku': 'SW-BAK-005',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Muffins & Bakes',
                'name': 'French Butter Croissant Box',
                'description': 'Flaky golden layered croissants baked with premium butter.',
                'price': 140.00,
                'discount_price': 125.00,
                'tax_percentage': 18.00,
                'unit': '2 Pcs',
                'stock_quantity': 35,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['croissant', 'breakfast', 'flaky'],
                'attributes': {'shelf_life_days': 2, 'contains_butter': True}
            },
            {
                'sku': 'SW-BAK-006',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Cookies',
                'name': 'Double Chocolate Chip Cookies',
                'description': 'Crispy outside and chewy inside cookies filled with rich chocolate chips.',
                'price': 180.00,
                'discount_price': 160.00,
                'tax_percentage': 18.00,
                'unit': '250 g',
                'stock_quantity': 90,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['cookies', 'chocochip', 'tea-time'],
                'attributes': {'shelf_life_days': 30, 'eggless': True}
            },
            {
                'sku': 'SW-BAK-007',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Muffins & Bakes',
                'name': 'Wild Blueberry Muffin Duo',
                'description': 'Moist vanilla muffins studded with real sweet blueberries.',
                'price': 110.00,
                'discount_price': 99.00,
                'tax_percentage': 18.00,
                'unit': '2 Pcs',
                'stock_quantity': 50,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['muffins', 'blueberry', 'snack'],
                'attributes': {'shelf_life_days': 4, 'eggless': True}
            },
            {
                'sku': 'SW-BAK-008',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Pastries',
                'name': 'Fudgy Walnut Chocolate Brownie',
                'description': 'Dense dark chocolate brownie topped with roasted California walnuts.',
                'price': 90.00,
                'discount_price': 85.00,
                'tax_percentage': 18.00,
                'unit': '100 g',
                'stock_quantity': 65,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['brownie', 'walnut', 'fudgy'],
                'attributes': {'contains_nuts': True, 'eggless': True}
            },
            {
                'sku': 'SW-BAK-009',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Breads',
                'name': 'Garlic Herb Focaccia Bread',
                'description': 'Italian flatbread infused with extra virgin olive oil, garlic, and rosemary.',
                'price': 95.00,
                'discount_price': 85.00,
                'tax_percentage': 5.00,
                'unit': '300 g',
                'stock_quantity': 40,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['focaccia', 'garlic-bread', 'artisanal'],
                'attributes': {'shelf_life_days': 2, 'eggless': True}
            },
            {
                'sku': 'SW-BAK-010',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Cakes',
                'name': 'Fresh Pineapple Cream Cake',
                'description': 'Light sponge layered with sweet whipped cream and juicy pineapple chunks.',
                'price': 450.00,
                'discount_price': 410.00,
                'tax_percentage': 18.00,
                'unit': '500 g',
                'stock_quantity': 20,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['pineapple', 'cream-cake', 'celebration'],
                'attributes': {'flavour': 'Pineapple', 'eggless': True}
            },
            {
                'sku': 'SW-BAK-011',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Cookies',
                'name': 'Roasted Almond Biscotti Box',
                'description': 'Twice-baked Italian crunch biscuits packed with toasted whole almonds.',
                'price': 210.00,
                'discount_price': 195.00,
                'tax_percentage': 18.00,
                'unit': '200 g',
                'stock_quantity': 45,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['biscotti', 'almond', 'coffee-pair'],
                'attributes': {'shelf_life_days': 45, 'contains_nuts': True}
            },
            {
                'sku': 'SW-BAK-012',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Muffins & Bakes',
                'name': 'Glazed Cinnamon Bun Pair',
                'description': 'Soft rolled dough swirled with aromatic cinnamon sugar and sweet glaze.',
                'price': 130.00,
                'discount_price': 115.00,
                'tax_percentage': 18.00,
                'unit': '2 Pcs',
                'stock_quantity': 30,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['cinnamon-roll', 'sweet-bake'],
                'attributes': {'shelf_life_days': 3, 'eggless': True}
            },
            {
                'sku': 'SW-BAK-013',
                'category': created_categories['BAKERY'],
                'subcategory_name': 'Pastries',
                'name': 'Vanilla Custard Choux Buns',
                'description': 'Light pastry shells generously filled with rich Madagascar vanilla custard.',
                'price': 160.00,
                'discount_price': 145.00,
                'tax_percentage': 18.00,
                'unit': '4 Pcs',
                'stock_quantity': 25,
                'is_available': True,
                'brand': 'Swastik Bakery',
                'tags': ['custard', 'choux', 'gourmet'],
                'attributes': {'refrigeration_required': True, 'shelf_life_days': 2}
            },

            # ==================== DAIRY SECTOR (12 Products) ====================
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
                'attributes': {'fat_content': '6.0%', 'snf_content': '9.0%', 'subscription_eligible': True}
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
                'stock_quantity': 180,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['protein-rich', 'fresh-made'],
                'attributes': {'shelf_life_days': 5, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-DAI-003',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Ghee',
                'name': 'Pure Desi Cow Ghee',
                'description': 'Traditional bilona method pure cow ghee with granulating aroma.',
                'price': 580.00,
                'discount_price': 540.00,
                'tax_percentage': 12.00,
                'unit': '500 g',
                'stock_quantity': 100,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['pure-ghee', 'cow-ghee', 'bilona'],
                'attributes': {'shelf_life_months': 9, 'aroma': 'Granulated Traditional'}
            },
            {
                'sku': 'SW-DAI-004',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Curd & Lassi',
                'name': 'Fresh Thick Set Curd (Dahi)',
                'description': 'Thick creamy curd made from wholesome pure milk.',
                'price': 45.00,
                'discount_price': 42.00,
                'tax_percentage': 0.00,
                'unit': '400 g',
                'stock_quantity': 250,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['curd', 'dahi', 'probiotic'],
                'attributes': {'shelf_life_days': 7, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-DAI-005',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Paneer & Butter',
                'name': 'Creamy Salted White Butter',
                'description': 'Traditional fresh white butter churned from pure cream.',
                'price': 115.00,
                'discount_price': 105.00,
                'tax_percentage': 12.00,
                'unit': '200 g',
                'stock_quantity': 90,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['butter', 'white-butter', 'churned'],
                'attributes': {'shelf_life_days': 15, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-DAI-006',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Curd & Lassi',
                'name': 'Sweet Alphonso Mango Lassi',
                'description': 'Refreshing chilled lassi blended with natural Alphonso mango pulp.',
                'price': 50.00,
                'discount_price': 45.00,
                'tax_percentage': 12.00,
                'unit': '300 ml',
                'stock_quantity': 120,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['mango-lassi', 'chilled', 'summer-drink'],
                'attributes': {'shelf_life_days': 5, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-DAI-007',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Curd & Lassi',
                'name': 'Masala Spiced Butter Milk (Chaas)',
                'description': 'Light digestive chaas flavoured with roasted cumin, mint, and black salt.',
                'price': 30.00,
                'discount_price': 25.00,
                'tax_percentage': 0.00,
                'unit': '500 ml',
                'stock_quantity': 300,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['chaas', 'masala-buttermilk', 'digestive'],
                'attributes': {'shelf_life_days': 4, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-DAI-008',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Cheese & Cream',
                'name': 'Fresh Malai Cream',
                'description': 'Thick pasteurized whipping and cooking dairy cream.',
                'price': 90.00,
                'discount_price': 82.00,
                'tax_percentage': 5.00,
                'unit': '250 g',
                'stock_quantity': 60,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['fresh-cream', 'cooking', 'desserts'],
                'attributes': {'fat_content': '25%', 'shelf_life_days': 10}
            },
            {
                'sku': 'SW-DAI-009',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Cheese & Cream',
                'name': 'Processed Mozzarella Cheese Block',
                'description': 'Great melting mozzarella cheese block perfect for pizzas and toasties.',
                'price': 160.00,
                'discount_price': 148.00,
                'tax_percentage': 12.00,
                'unit': '200 g',
                'stock_quantity': 75,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['mozzarella', 'cheese', 'pizza-cheese'],
                'attributes': {'shelf_life_months': 6, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-DAI-010',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Milk',
                'name': 'Dutch Chocolate Milk Bottle',
                'description': 'Delicious chilled milk flavoured with rich cocoa.',
                'price': 40.00,
                'discount_price': 38.00,
                'tax_percentage': 12.00,
                'unit': '200 ml',
                'stock_quantity': 150,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['chocolate-milk', 'kids-favorite', 'chilled'],
                'attributes': {'shelf_life_days': 15, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-DAI-011',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Milk',
                'name': 'Low Fat Toned Milk Pouch',
                'description': 'Healthy pasteurized toned milk with reduced fat for daily wellness.',
                'price': 56.00,
                'discount_price': 54.00,
                'tax_percentage': 0.00,
                'unit': '1 L',
                'stock_quantity': 400,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['toned-milk', 'low-fat', 'daily-essential'],
                'attributes': {'fat_content': '3.0%', 'snf_content': '8.5%'}
            },
            {
                'sku': 'SW-DAI-012',
                'category': created_categories['DAIRY'],
                'subcategory_name': 'Paneer & Butter',
                'name': 'Unsweetened Pure Khoya / Mawa',
                'description': 'Fresh condensed milk khoya ideal for preparing homemade sweets.',
                'price': 140.00,
                'discount_price': 130.00,
                'tax_percentage': 5.00,
                'unit': '250 g',
                'stock_quantity': 50,
                'is_available': True,
                'brand': 'Swastik Dairy',
                'tags': ['khoya', 'mawa', 'sweet-making'],
                'attributes': {'shelf_life_days': 7, 'refrigeration_required': True}
            },

            # ==================== SWEETS SECTOR (13 Products) ====================
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
                'stock_quantity': 80,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['traditional', 'festive-favorite', 'bestseller'],
                'attributes': {'piece_count': '16-18 Pcs', 'packaging': 'Sealed Tin'}
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
                'stock_quantity': 100,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['pure-ghee', 'motichoor', 'mithai'],
                'attributes': {'ghee_type': 'Pure Desi Ghee', 'shelf_life_days': 15}
            },
            {
                'sku': 'SW-SWT-003',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Syrup Sweets',
                'name': 'Shahi Soft Gulab Jamun',
                'description': 'Warm golden khoya balls dipped in cardamom infused rose syrup.',
                'price': 340.00,
                'discount_price': 310.00,
                'tax_percentage': 5.00,
                'unit': '1 kg',
                'stock_quantity': 90,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['gulab-jamun', 'syrup-sweet', 'bestseller'],
                'attributes': {'piece_count': '20 Pcs', 'shelf_life_days': 10}
            },
            {
                'sku': 'SW-SWT-004',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Dry Mithai',
                'name': 'Kaju Katli Premium Box',
                'description': 'Diamond cut cashew fudge decorated with pure edible silver vark.',
                'price': 520.00,
                'discount_price': 480.00,
                'tax_percentage': 5.00,
                'unit': '400 g',
                'stock_quantity': 110,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['kaju-katli', 'cashew', 'festive-gift'],
                'attributes': {'cashew_content': '80%', 'shelf_life_days': 30}
            },
            {
                'sku': 'SW-SWT-005',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Ghee Sweets',
                'name': 'Pure Ghee Roasted Besan Ladoo',
                'description': 'Aromatic slow roasted gram flour spheres enriched with cardamom and almonds.',
                'price': 380.00,
                'discount_price': 350.00,
                'tax_percentage': 5.00,
                'unit': '500 g',
                'stock_quantity': 85,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['besan-ladoo', 'desighee', 'traditional'],
                'attributes': {'shelf_life_days': 45}
            },
            {
                'sku': 'SW-SWT-006',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Syrup Sweets',
                'name': 'Royal Saffron Rasmalai',
                'description': 'Soft cottage cheese patties soaked in thick saffron pistachio flavoured milk.',
                'price': 180.00,
                'discount_price': 165.00,
                'tax_percentage': 5.00,
                'unit': '4 Pcs',
                'stock_quantity': 40,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['rasmalai', 'saffron', 'chilled-sweet'],
                'attributes': {'shelf_life_days': 3, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-SWT-007',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Dry Mithai',
                'name': 'Traditional Alwar Milk Cake',
                'description': 'Caramelized grainy milk fudge made from pure reduced milk.',
                'price': 360.00,
                'discount_price': 335.00,
                'tax_percentage': 5.00,
                'unit': '400 g',
                'stock_quantity': 60,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['milk-cake', 'kalakand', 'grainy-fudge'],
                'attributes': {'shelf_life_days': 12}
            },
            {
                'sku': 'SW-SWT-008',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Dry Mithai',
                'name': 'Crispy Flaky Soan Papdi',
                'description': 'Multi-layered flaky sweet crisp infused with cardamom and pistachios.',
                'price': 210.00,
                'discount_price': 190.00,
                'tax_percentage': 5.00,
                'unit': '500 g',
                'stock_quantity': 120,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['soan-papdi', 'flaky-sweet', 'gift-box'],
                'attributes': {'shelf_life_months': 4}
            },
            {
                'sku': 'SW-SWT-009',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Dry Mithai',
                'name': 'Special Mathura Peda',
                'description': 'Authentic roasted khoya pedas dusted with fine cardamom powder.',
                'price': 290.00,
                'discount_price': 270.00,
                'tax_percentage': 5.00,
                'unit': '400 g',
                'stock_quantity': 70,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['peda', 'mathura-peda', 'khoya-sweet'],
                'attributes': {'shelf_life_days': 20}
            },
            {
                'sku': 'SW-SWT-010',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Syrup Sweets',
                'name': 'Desi Ghee Kurkuri Jalebi',
                'description': 'Crispy golden spirals fried in pure ghee and soaked in saffron syrup.',
                'price': 120.00,
                'discount_price': 110.00,
                'tax_percentage': 5.00,
                'unit': '250 g',
                'stock_quantity': 45,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['jalebi', 'crispy', 'fresh-hot'],
                'attributes': {'best_consumed': 'Same Day'}
            },
            {
                'sku': 'SW-SWT-011',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Syrup Sweets',
                'name': 'Malai Cream Cham Cham',
                'description': 'Cylindrical chhena sweets coated with mawa flakes and dry fruits.',
                'price': 280.00,
                'discount_price': 260.00,
                'tax_percentage': 5.00,
                'unit': '500 g',
                'stock_quantity': 50,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['cham-cham', 'bengali-sweet'],
                'attributes': {'shelf_life_days': 5, 'refrigeration_required': True}
            },
            {
                'sku': 'SW-SWT-012',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Ghee Sweets',
                'name': 'Pure Ghee Mysore Pak',
                'description': 'Melt-in-mouth traditional South Indian sweet rich in desi ghee.',
                'price': 410.00,
                'discount_price': 380.00,
                'tax_percentage': 5.00,
                'unit': '400 g',
                'stock_quantity': 65,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['mysore-pak', 'ghee-sweet', 'rich'],
                'attributes': {'shelf_life_days': 20}
            },
            {
                'sku': 'SW-SWT-013',
                'category': created_categories['SWEETS'],
                'subcategory_name': 'Dry Mithai',
                'name': 'Sugarfree Dry Fruit & Nut Ladoo',
                'description': 'Healthy dates and figs based spheres loaded with almonds, cashews, and pistachios.',
                'price': 620.00,
                'discount_price': 570.00,
                'tax_percentage': 5.00,
                'unit': '400 g',
                'stock_quantity': 55,
                'is_available': True,
                'brand': 'Swastik Sweets',
                'tags': ['sugarfree', 'dry-fruit-ladoo', 'healthy-sweet'],
                'attributes': {'no_added_sugar': True, 'shelf_life_days': 60}
            },

            # ==================== CONFECTIONERY SECTOR (12 Products) ====================
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
                'tags': ['spicy', 'ratlami-sev', 'tea-time'],
                'attributes': {'spice_level': 'Medium High', 'shelf_life_months': 4}
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
                'stock_quantity': 80,
                'is_available': True,
                'brand': 'Swastik Confectionery',
                'tags': ['gift-pack', 'chocolates', 'premium'],
                'attributes': {'piece_count': 12, 'contains_nuts': True}
            },
            {
                'sku': 'SW-CNF-003',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Namkeen & Savouries',
                'name': 'Crispy Spicy Aloo Bhujia',
                'description': 'Tangy potato and gram flour crisp threads spiced with mint and dry mango powder.',
                'price': 130.00,
                'discount_price': 118.00,
                'tax_percentage': 12.00,
                'unit': '400 g',
                'stock_quantity': 220,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['aloo-bhujia', 'namkeen', 'snack'],
                'attributes': {'shelf_life_months': 6}
            },
            {
                'sku': 'SW-CNF-004',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Nuts & Dry Fruits',
                'name': 'Slow Roasted Salted Cashews',
                'description': 'Jumbo W240 cashews roasted in pure ghee and tossed with rock salt.',
                'price': 310.00,
                'discount_price': 285.00,
                'tax_percentage': 12.00,
                'unit': '200 g',
                'stock_quantity': 95,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['cashews', 'roasted-nuts', 'premium-snack'],
                'attributes': {'shelf_life_months': 6}
            },
            {
                'sku': 'SW-CNF-005',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Namkeen & Savouries',
                'name': 'Kerala Crunchy Salted Banana Chips',
                'description': 'Crisp raw nendran banana slices fried in coconut oil with turmeric.',
                'price': 110.00,
                'discount_price': 98.00,
                'tax_percentage': 12.00,
                'unit': '250 g',
                'stock_quantity': 140,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['banana-chips', 'coconut-oil', 'crispy'],
                'attributes': {'oil_type': 'Pure Coconut Oil', 'shelf_life_months': 3}
            },
            {
                'sku': 'SW-CNF-006',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Nuts & Dry Fruits',
                'name': 'Smoky Roasted Almonds with Sea Salt',
                'description': 'California whole almonds wood-fire roasted with sea salt.',
                'price': 290.00,
                'discount_price': 270.00,
                'tax_percentage': 12.00,
                'unit': '200 g',
                'stock_quantity': 110,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['almonds', 'roasted', 'healthy-snack'],
                'attributes': {'shelf_life_months': 6}
            },
            {
                'sku': 'SW-CNF-007',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Namkeen & Savouries',
                'name': 'Traditional Ajwain Khasta Mathri',
                'description': 'Crispy flaky savory crackers flavoured with carom seeds and black pepper.',
                'price': 125.00,
                'discount_price': 115.00,
                'tax_percentage': 12.00,
                'unit': '400 g',
                'stock_quantity': 130,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['mathri', 'ajwain', 'tea-companion'],
                'attributes': {'shelf_life_months': 4}
            },
            {
                'sku': 'SW-CNF-008',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Namkeen & Savouries',
                'name': 'Chatpata Chana Chor Garam',
                'description': 'Flattened roasted black chickpeas spiced with tangy chaat masala.',
                'price': 115.00,
                'discount_price': 105.00,
                'tax_percentage': 12.00,
                'unit': '350 g',
                'stock_quantity': 150,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['chana-chor', 'tangy', 'protein-snack'],
                'attributes': {'roasted': True, 'shelf_life_months': 5}
            },
            {
                'sku': 'SW-CNF-009',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Chocolates',
                'name': '70% Dark Chocolate Almond Bar',
                'description': 'Rich single-origin dark cocoa slab studded with whole roasted almonds.',
                'price': 160.00,
                'discount_price': 145.00,
                'tax_percentage': 18.00,
                'unit': '100 g',
                'stock_quantity': 90,
                'is_available': True,
                'brand': 'Swastik Confectionery',
                'tags': ['dark-chocolate', '70-percent', 'almond-bar'],
                'attributes': {'cocoa_percentage': '70%', 'shelf_life_months': 9}
            },
            {
                'sku': 'SW-CNF-010',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Namkeen & Savouries',
                'name': 'Mini Samosa Crisps',
                'description': 'Bite-sized triangular crispy samosas filled with sweet and spicy lentil mix.',
                'price': 95.00,
                'discount_price': 88.00,
                'tax_percentage': 12.00,
                'unit': '200 g',
                'stock_quantity': 175,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['mini-samosa', 'party-snack', 'crispy'],
                'attributes': {'shelf_life_months': 3}
            },
            {
                'sku': 'SW-CNF-011',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Biscuits & Wafers',
                'name': 'Rich Butter Salt Cookies Box',
                'description': 'Melt-in-mouth savory butter cookies sprinkled with rock salt crystals.',
                'price': 175.00,
                'discount_price': 160.00,
                'tax_percentage': 18.00,
                'unit': '300 g',
                'stock_quantity': 110,
                'is_available': True,
                'brand': 'Swastik Confectionery',
                'tags': ['butter-cookies', 'salted', 'bakery-style'],
                'attributes': {'shelf_life_months': 4}
            },
            {
                'sku': 'SW-CNF-012',
                'category': created_categories['CONFECTIONERY'],
                'subcategory_name': 'Biscuits & Wafers',
                'name': 'Tangy Lemon Chatpata Wafers',
                'description': 'Thin crispy potato wafers seasoned with tangy lemon pepper spices.',
                'price': 65.00,
                'discount_price': 58.00,
                'tax_percentage': 12.00,
                'unit': '150 g',
                'stock_quantity': 210,
                'is_available': True,
                'brand': 'Swastik Snacks',
                'tags': ['potato-chips', 'lemon-flavor', 'chatpata'],
                'attributes': {'shelf_life_months': 4}
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
            if not created:
                # Update existing products with full detailed attributes if already present
                product.name = prod_info['name']
                product.category = prod_info['category']
                product.subcategory_name = prod_info['subcategory_name']
                product.description = prod_info['description']
                product.price = prod_info['price']
                product.discount_price = prod_info['discount_price']
                product.tax_percentage = prod_info['tax_percentage']
                product.unit = prod_info['unit']
                product.stock_quantity = prod_info['stock_quantity']
                product.is_available = prod_info['is_available']
                product.brand = prod_info['brand']
                product.tags = prod_info['tags']
                product.attributes = prod_info['attributes']
                product.save()

            prod_status = 'Created' if created else 'Updated'
            self.stdout.write(f'Product [{product.sku}] "{product.name}": {prod_status}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded 50 detailed products and superuser!'))
