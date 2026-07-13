from django.db import models
from django.utils.text import slugify

class GrantCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='💰')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Grant Categories'

    def __str__(self):
        return self.name


class Grant(models.Model):
    STATUS_CHOICES = [
        ('open',     'Open'),
        ('closed',   'Closed'),
        ('upcoming', 'Upcoming'),
    ]
    TYPE_CHOICES = [
        ('scholarship', 'Scholarship'),
        ('grant',       'Grant'),
        ('fellowship',  'Fellowship'),
        ('internship',  'Internship'),
        ('job',         'Job'),
    ]
    ELIGIBILITY_CHOICES = [
        ('ngo',          'NGO / Non-Profit'),
        ('individual',   'Individual'),
        ('student',      'Student'),
        ('researcher',   'Researcher'),
        ('organization', 'Organization'),
        ('any',          'Anyone'),
    ]

    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    category     = models.ForeignKey(
                       GrantCategory,
                       on_delete=models.SET_NULL,
                       null=True, blank=True
                   )
    type         = models.CharField(
                       max_length=20,
                       choices=TYPE_CHOICES,
                       default='grant'
                   )
    funder       = models.CharField(max_length=200)
    funder_logo  = models.ImageField(
                       upload_to='funders/',
                       blank=True, null=True
                   )
    description  = models.TextField()
    amount_min   = models.DecimalField(
                       max_digits=12,
                       decimal_places=2,
                       null=True, blank=True
                   )
    amount_max   = models.DecimalField(
                       max_digits=12,
                       decimal_places=2,
                       null=True, blank=True
                   )
    currency     = models.CharField(max_length=10, default='USD')
    eligibility  = models.CharField(
                       max_length=20,
                       choices=ELIGIBILITY_CHOICES,
                       default='any'
                   )
    countries    = models.TextField(
                       help_text='Comma separated country codes',
                       blank=True
                   )
    deadline     = models.DateField()
    apply_url    = models.URLField(blank=True)
    status       = models.CharField(
                       max_length=20,
                       choices=STATUS_CHOICES,
                       default='open'
                   )
    is_featured  = models.BooleanField(default=False)
    views        = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title