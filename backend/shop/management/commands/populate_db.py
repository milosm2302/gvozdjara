from django.core.management.base import BaseCommand
from shop.models import Category, Subcategory, Product, ProductVariant
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popunjava bazu sa proizvodima iz cenovnika'

    def handle(self, *args, **kwargs):
        self.stdout.write('Kreiranje kategorija...')

        # Kreiranje glavnih kategorija
        cat_profili = Category.objects.get_or_create(
            name='Profili i Cevi',
            defaults={'description': 'Železni profili, firiket, flahovi i cevi različitih dimenzija'}
        )[0]

        cat_kutije = Category.objects.get_or_create(
            name='Kutije',
            defaults={'description': 'Kvadratne i pravougaone kutije različitih dimenzija'}
        )[0]

        cat_ukrasni = Category.objects.get_or_create(
            name='Ukrasni Elementi',
            defaults={'description': 'Siljci, cvetovi, listovi i ostali dekorativni elementi'}
        )[0]

        self.stdout.write('Kreiranje potkategorija...')

        # Potkategorije za profile
        subcat_firiket = Subcategory.objects.get_or_create(
            name='Firiket',
            category=cat_profili,
            defaults={'description': 'Firiket profili - obični i grifovani'}
        )[0]

        subcat_flahovi = Subcategory.objects.get_or_create(
            name='Flahovi',
            category=cat_profili,
            defaults={'description': 'Vučeni flahovi različitih dimenzija'}
        )[0]

        # Potkategorije za ukrasne elemente
        subcat_siljci = Subcategory.objects.get_or_create(
            name='Siljci',
            category=cat_ukrasni,
            defaults={'description': 'Kovani siljci različitih visina'}
        )[0]

        subcat_cvetovi = Subcategory.objects.get_or_create(
            name='Cvetovi',
            category=cat_ukrasni,
            defaults={'description': 'Dekorativni kovani cvetovi'}
        )[0]

        subcat_listovi = Subcategory.objects.get_or_create(
            name='Listovi',
            category=cat_ukrasni,
            defaults={'description': 'Dekorativni kovani listovi'}
        )[0]

        subcat_kovanice = Subcategory.objects.get_or_create(
            name='Kovanice',
            category=cat_ukrasni,
            defaults={'description': 'Kovane dekoracije i elementi'}
        )[0]

        self.stdout.write('Dodavanje FIRIKET proizvoda...')

        # FIRIKET - Obični
        firiket_obican = Product.objects.get_or_create(
            name='Firiket Obični (6m)',
            defaults={
                'description': 'Kvalitetni firiket profil, dužina 6 metara. Različite dimenzije dostupne.',
                'price': Decimal('350.00'),
                'category': cat_profili,
                'subcategory': subcat_firiket,
                'featured': True,
                'in_stock': True,
                'stock_quantity': 100
            }
        )[0]

        # Varijante za obični firiket
        firiket_dimenzije = [
            ('12×12mm', Decimal('0.00')),
            ('14×14mm', Decimal('50.00')),
            ('16×16mm', Decimal('100.00')),
            ('20×20mm', Decimal('150.00')),
            ('25×25mm', Decimal('250.00')),
            ('30×30mm', Decimal('400.00')),
            ('40×40mm', Decimal('650.00')),
        ]

        for dim_name, price_adj in firiket_dimenzije:
            ProductVariant.objects.get_or_create(
                product=firiket_obican,
                name=dim_name,
                defaults={
                    'price_adjustment': price_adj,
                    'sku': f'FIRIKET-O-{dim_name.replace("×", "x").replace("mm", "")}',
                    'in_stock': True,
                    'stock_quantity': 50
                }
            )

        # FIRIKET - Grifovan
        firiket_grifovan = Product.objects.get_or_create(
            name='Firiket Grifovan (6m)',
            defaults={
                'description': 'Grifovani firiket profil sa teksturom, dužina 6 metara. Različite dimenzije dostupne.',
                'price': Decimal('400.00'),
                'category': cat_profili,
                'subcategory': subcat_firiket,
                'on_sale': True,
                'sale_price': Decimal('350.00'),
                'featured': False,
                'in_stock': True,
                'stock_quantity': 80
            }
        )[0]

        grifovan_dimenzije = [
            ('12×12mm', Decimal('0.00')),
            ('14×14mm', Decimal('60.00')),
            ('16×16mm', Decimal('120.00')),
            ('20×20mm', Decimal('180.00')),
        ]

        for dim_name, price_adj in grifovan_dimenzije:
            ProductVariant.objects.get_or_create(
                product=firiket_grifovan,
                name=dim_name,
                defaults={
                    'price_adjustment': price_adj,
                    'sku': f'FIRIKET-G-{dim_name.replace("×", "x").replace("mm", "")}',
                    'in_stock': True,
                    'stock_quantity': 40
                }
            )

        self.stdout.write('Dodavanje FLAHOVA...')

        # FLAHOVI VUCENI
        flahovi = Product.objects.get_or_create(
            name='Flahovi Vučeni (6m)',
            defaults={
                'description': 'Vučeni flahovi za bravariju i građevinarstvo, dužina 6 metara.',
                'price': Decimal('280.00'),
                'category': cat_profili,
                'subcategory': subcat_flahovi,
                'featured': True,
                'in_stock': True,
                'stock_quantity': 120
            }
        )[0]

        flahovi_dimenzije = [
            ('12×6mm', Decimal('0.00')),
            ('30×5mm', Decimal('120.00')),
            ('40×8mm', Decimal('200.00')),
            ('50×6mm', Decimal('180.00')),
            ('60×8mm', Decimal('280.00')),
            ('80×8mm', Decimal('400.00')),
        ]

        for dim_name, price_adj in flahovi_dimenzije:
            ProductVariant.objects.get_or_create(
                product=flahovi,
                name=dim_name,
                defaults={
                    'price_adjustment': price_adj,
                    'sku': f'FLAH-{dim_name.replace("×", "x").replace("mm", "")}',
                    'in_stock': True,
                    'stock_quantity': 60
                }
            )

        self.stdout.write('Dodavanje KUTIJA...')

        # KUTIJE
        kutije = Product.objects.get_or_create(
            name='Kutije - Kvadratni Profil (6m)',
            defaults={
                'description': 'Kvadratne kutije za konstrukcije, ograde i bravariju. Dužina 6 metara.',
                'price': Decimal('450.00'),
                'category': cat_kutije,
                'subcategory': None,
                'on_sale': True,
                'sale_price': Decimal('400.00'),
                'featured': True,
                'in_stock': True,
                'stock_quantity': 90
            }
        )[0]

        kutije_dimenzije = [
            ('20×20×2mm', Decimal('0.00')),
            ('30×30×2mm', Decimal('150.00')),
            ('40×40×2mm', Decimal('250.00')),
            ('50×50×3mm', Decimal('400.00')),
            ('60×60×3mm', Decimal('550.00')),
            ('80×80×4mm', Decimal('850.00')),
        ]

        for dim_name, price_adj in kutije_dimenzije:
            ProductVariant.objects.get_or_create(
                product=kutije,
                name=dim_name,
                defaults={
                    'price_adjustment': price_adj,
                    'sku': f'KUTIJA-{dim_name.replace("×", "x").replace("mm", "")}',
                    'in_stock': True,
                    'stock_quantity': 45
                }
            )

        self.stdout.write('Dodavanje UKRASNIH ELEMENATA...')

        # SILJCI
        siljci_proizvodi = [
            {
                'name': 'Siljak Kovani - Visina 150mm',
                'description': 'Kovani siljak visine 150mm, idealan za ograde i kapije.',
                'price': Decimal('120.00'),
                'sku': 'SILJAK-150',
            },
            {
                'name': 'Siljak Kovani - Visina 200mm',
                'description': 'Kovani siljak visine 200mm, robustan i dekorativan.',
                'price': Decimal('150.00'),
                'sale_price': Decimal('130.00'),
                'on_sale': True,
                'sku': 'SILJAK-200',
            },
            {
                'name': 'Siljak Kovani - Visina 250mm',
                'description': 'Kovani siljak visine 250mm za visoke ograde.',
                'price': Decimal('180.00'),
                'sku': 'SILJAK-250',
            },
        ]

        for siljak_data in siljci_proizvodi:
            Product.objects.get_or_create(
                name=siljak_data['name'],
                defaults={
                    'description': siljak_data['description'],
                    'price': siljak_data['price'],
                    'category': cat_ukrasni,
                    'subcategory': subcat_siljci,
                    'on_sale': siljak_data.get('on_sale', False),
                    'sale_price': siljak_data.get('sale_price', None),
                    'featured': False,
                    'in_stock': True,
                    'stock_quantity': 200
                }
            )

        # CVETOVI
        cvetovi_proizvodi = [
            {
                'name': 'Cvet Kovani - Model A',
                'description': 'Dekorativni kovani cvet, ručno izrađen.',
                'price': Decimal('95.00'),
            },
            {
                'name': 'Cvet Kovani - Model B',
                'description': 'Elegantni kovani cvet sa detaljnom obradom.',
                'price': Decimal('110.00'),
                'sale_price': Decimal('95.00'),
                'on_sale': True,
            },
        ]

        for cvet_data in cvetovi_proizvodi:
            Product.objects.get_or_create(
                name=cvet_data['name'],
                defaults={
                    'description': cvet_data['description'],
                    'price': cvet_data['price'],
                    'category': cat_ukrasni,
                    'subcategory': subcat_cvetovi,
                    'on_sale': cvet_data.get('on_sale', False),
                    'sale_price': cvet_data.get('sale_price', None),
                    'featured': True,
                    'in_stock': True,
                    'stock_quantity': 150
                }
            )

        # LISTOVI
        listovi_proizvodi = [
            {
                'name': 'List Kovani - Mala',
                'description': 'Kovani list male veličine za dekoraciju.',
                'price': Decimal('45.00'),
            },
            {
                'name': 'List Kovani - Velika',
                'description': 'Veliki kovani list sa detaljnom obradom.',
                'price': Decimal('75.00'),
            },
        ]

        for list_data in listovi_proizvodi:
            Product.objects.get_or_create(
                name=list_data['name'],
                defaults={
                    'description': list_data['description'],
                    'price': list_data['price'],
                    'category': cat_ukrasni,
                    'subcategory': subcat_listovi,
                    'featured': False,
                    'in_stock': True,
                    'stock_quantity': 180
                }
            )

        # KOVANICE
        kovanice_proizvodi = [
            {
                'name': 'Kovanica Dekorativna - Rozeta',
                'description': 'Dekorativna kovanica u obliku rozete.',
                'price': Decimal('160.00'),
                'featured': True,
            },
            {
                'name': 'Kovanica Dekorativna - Spirala',
                'description': 'Elegantna spiralna kovanica.',
                'price': Decimal('140.00'),
                'sale_price': Decimal('120.00'),
                'on_sale': True,
            },
        ]

        for kovanica_data in kovanice_proizvodi:
            Product.objects.get_or_create(
                name=kovanica_data['name'],
                defaults={
                    'description': kovanica_data['description'],
                    'price': kovanica_data['price'],
                    'category': cat_ukrasni,
                    'subcategory': subcat_kovanice,
                    'on_sale': kovanica_data.get('on_sale', False),
                    'sale_price': kovanica_data.get('sale_price', None),
                    'featured': kovanica_data.get('featured', False),
                    'in_stock': True,
                    'stock_quantity': 100
                }
            )

        self.stdout.write(self.style.SUCCESS('✓ Baza uspešno popunjena sa proizvodima!'))
        self.stdout.write(f'  Kategorije: {Category.objects.count()}')
        self.stdout.write(f'  Potkategorije: {Subcategory.objects.count()}')
        self.stdout.write(f'  Proizvodi: {Product.objects.count()}')
        self.stdout.write(f'  Varijante: {ProductVariant.objects.count()}')
