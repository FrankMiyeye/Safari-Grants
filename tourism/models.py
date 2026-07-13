from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser

class Country(models.Model):
    name      = models.CharField(max_length=100)
    code      = models.CharField(max_length=3)
    flag      = models.CharField(max_length=10, default='🌍')
    continent = models.CharField(max_length=50, default='Africa')

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return self.name


class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('safari',    'Safari & Wildlife'),
        ('beach',     'Beach & Coastal'),
        ('mountain',  'Mountain & Hiking'),
        ('cultural',  'Cultural & Historical'),
        ('adventure', 'Adventure Sports'),
        ('luxury',    'Luxury Retreat'),
        ('national_park', 'National Park'),
    ]

    country      = models.ForeignKey(
                       Country,
                       on_delete=models.CASCADE,
                       related_name='destinations'
                   )
    name         = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    category     = models.CharField(
                       max_length=20,
                       choices=CATEGORY_CHOICES
                   )
    description  = models.TextField()
    highlights   = models.TextField(blank=True)
    main_image   = models.ImageField(
                       upload_to='destinations/',
                       blank=True, null=True
                   )
    latitude     = models.FloatField(default=0)
    longitude    = models.FloatField(default=0)
    is_featured  = models.BooleanField(default=False)
    views        = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-views']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class TourPackage(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy',        'Easy'),
        ('moderate',    'Moderate'),
        ('challenging', 'Challenging'),
    ]
    CATEGORY_CHOICES = [
        ('wildlife',  'Wildlife Safari'),
        ('beach',     'Beach & Coastal'),
        ('mountain',  'Mountain Trekking'),
        ('cultural',  'Cultural Tour'),
        ('adventure', 'Adventure Sports'),
        ('luxury',    'Luxury Retreat'),
        ('budget',    'Budget Safari'),
    ]

    title            = models.CharField(max_length=200)
    slug             = models.SlugField(unique=True, blank=True)
    destination      = models.ForeignKey(
                           Destination,
                           on_delete=models.CASCADE,
                           related_name='packages'
                       )
    category         = models.CharField(
                           max_length=20,
                           choices=CATEGORY_CHOICES,
                           default='wildlife'
                       )
    description      = models.TextField()
    duration_days    = models.PositiveIntegerField()
    max_group_size   = models.PositiveIntegerField(default=12)
    difficulty       = models.CharField(
                           max_length=20,
                           choices=DIFFICULTY_CHOICES,
                           default='moderate'
                       )
    price_per_person = models.DecimalField(
                           max_digits=10,
                           decimal_places=2
                       )
    discount_percent = models.PositiveIntegerField(default=0)
    includes         = models.TextField(blank=True)
    excludes         = models.TextField(blank=True)
    main_image       = models.ImageField(
                           upload_to='packages/',
                           blank=True, null=True
                       )
    is_featured      = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    rating           = models.FloatField(default=0.0)
    total_reviews    = models.PositiveIntegerField(default=0)
    views            = models.PositiveIntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount_percent > 0:
            discount = self.price_per_person * self.discount_percent / 100
            return self.price_per_person - discount
        return self.price_per_person

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('confirmed',   'Confirmed'),
        ('paid',        'Paid'),
        ('completed',   'Completed'),
        ('cancelled',   'Cancelled'),
        ('refunded',    'Refunded'),
    ]

    booking_ref   = models.CharField(max_length=12, unique=True)
    tourist       = models.ForeignKey(
                        CustomUser,
                        on_delete=models.CASCADE,
                        related_name='bookings'
                    )
    package       = models.ForeignKey(
                        TourPackage,
                        on_delete=models.SET_NULL,
                        null=True, blank=True
                    )
    start_date    = models.DateField()
    end_date      = models.DateField()
    num_adults    = models.PositiveIntegerField(default=1)
    num_children  = models.PositiveIntegerField(default=0)
    total_price   = models.DecimalField(
                        max_digits=12,
                        decimal_places=2
                    )
    currency      = models.CharField(max_length=10, default='USD')
    special_requests = models.TextField(blank=True)
    status        = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICES,
                        default='pending'
                    )
    paid_at       = models.DateTimeField(null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            import uuid
            self.booking_ref = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.booking_ref}"