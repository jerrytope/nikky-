from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Create default categories for the cosmetics store'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Skincare',
                'description': 'Facial care products including cleansers, moisturizers, and treatments'
            },
            {
                'name': 'Makeup',
                'description': 'Cosmetic products for enhancing beauty including foundation, lipstick, and eyeshadow'
            },
            {
                'name': 'Haircare',
                'description': 'Products for hair care including shampoos, conditioners, and styling products'
            },
            {
                'name': 'Fragrance',
                'description': 'Perfumes and body sprays for men and women'
            },
            {
                'name': 'Bath & Body',
                'description': 'Body care products including soaps, lotions, and bath products'
            },
            {
                'name': 'Tools & Accessories',
                'description': 'Beauty tools and accessories including brushes, mirrors, and applicators'
            },
            {
                'name': 'Men',
                'description': 'Cosmetic and grooming products specifically for men'
            },
            {
                'name': 'Other',
                'description': 'Miscellaneous beauty and cosmetic products'
            }
        ]

        created_count = 0
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        ) 