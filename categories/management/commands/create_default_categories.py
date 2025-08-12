from django.core.management.base import BaseCommand
from categories.models import Category


class Command(BaseCommand):
    help = 'Create default categories for the Budget Tracker API'

    def handle(self, *args, **options):
        """Create default categories if they don't exist."""
        
        default_categories = [
            {'name': 'Food & Dining', 'description': 'Groceries, restaurants, coffee, etc.'},
            {'name': 'Transportation', 'description': 'Gas, public transport, taxi, car maintenance'},
            {'name': 'Utilities', 'description': 'Electricity, water, internet, phone bills'},
            {'name': 'Entertainment', 'description': 'Movies, games, hobbies, subscriptions'},
            {'name': 'Healthcare', 'description': 'Medical expenses, insurance, pharmacy'},
            {'name': 'Shopping', 'description': 'Clothing, electronics, household items'},
            {'name': 'Education', 'description': 'Books, courses, tuition fees'},
            {'name': 'Savings', 'description': 'Money saved or invested'},
            {'name': 'Salary', 'description': 'Primary income from employment'},
            {'name': 'Freelance', 'description': 'Income from freelance work'},
            {'name': 'Investment', 'description': 'Income from investments and dividends'},
            {'name': 'Gift', 'description': 'Money received as gifts'},
            {'name': 'Rent', 'description': 'Monthly rent payments'},
            {'name': 'Insurance', 'description': 'Life, health, car insurance'},
            {'name': 'Other', 'description': 'Miscellaneous expenses and income'},
        ]

        created_count = 0
        existing_count = 0

        for category_data in default_categories:
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
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} categories created, {existing_count} already existed.'
            )
        )
