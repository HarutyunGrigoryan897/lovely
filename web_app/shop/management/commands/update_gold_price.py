"""
Django management command to manually update gold price
Usage: python manage.py update_gold_price
"""
from django.core.management.base import BaseCommand
from shop.scraper import update_gold_price_sync, should_update_gold_price
from shop.models import GoldPrice


class Command(BaseCommand):
    help = 'Scrape and update the gold price from external source'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if price was recently updated',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting gold price update...'))
        
        # Check if update is needed (unless forced)
        if not options['force'] and not should_update_gold_price():
            active_price = GoldPrice.objects.filter(is_active=True).first()
            if active_price:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Gold price is up to date: ${active_price.price_per_gram}/gram '
                        f'(last updated: {active_price.updated_at.strftime("%Y-%m-%d %H:%M:%S")})'
                    )
                )
                self.stdout.write(self.style.WARNING('Use --force to update anyway'))
                return
        
        # Perform the update
        self.stdout.write('Scraping gold price from external source...')
        self.stdout.write('This may take 30-60 seconds...')
        
        success, message = update_gold_price_sync()
        
        if success:
            self.stdout.write(self.style.SUCCESS(f'✓ {message}'))
            
            # Show current active price
            active_price = GoldPrice.objects.filter(is_active=True).first()
            if active_price:
                final_price = active_price.price_per_gram * (1 + active_price.markup_percentage / 100)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Base price: ${active_price.price_per_gram}/gram\n'
                        f'  Markup: {active_price.markup_percentage}%\n'
                        f'  Final price: ${final_price:.2f}/gram'
                    )
                )
        else:
            self.stdout.write(self.style.ERROR(f'✗ {message}'))
            self.stdout.write(
                self.style.WARNING(
                    'Troubleshooting tips:\n'
                    '  - Check internet connection\n'
                    '  - Ensure playwright is installed: playwright install\n'
                    '  - Check if source website is accessible'
                )
            )
