from django.db import models
from django.contrib.auth.models import User

class Journal(models.Model):
    name = models.CharField(max_length=512, unique=True)
    abbreviation = models.CharField(max_length=32, unique=True)
    impact_factor = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True, default=None)
    impact_factor_year = models.IntegerField(null=True, blank=True, default=None)
    impact_factor_quartile = models.CharField(max_length=1, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} - {self.abbreviation}"

class Paper(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    source = models.CharField(max_length=32, null=True, blank=True, default='')
    parse_time = models.DateTimeField(null=True, blank=True, default=None)

    title = models.CharField(max_length=512)
    journal = models.CharField(max_length=512, null=True, blank=True, default='')
    journal_abbreviation = models.CharField(max_length=32, null=True, blank=True, default='')
    journal_impact_factor = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True, default=None)
    journal_impact_factor_quartile = models.CharField(max_length=1, null=True, blank=True, default='')
    pub_date = models.CharField(max_length=32, null=True, blank=True, default='')
    pub_date_dt = models.DateField(null=True, blank=True, default=None)
    pub_year = models.IntegerField(null=True, blank=True, default=None)
    doi = models.CharField(max_length=128, null=True, blank=True, default='')
    pmid = models.CharField(max_length=32, null=True, blank=True, default='')
    abstract = models.TextField(null=True, blank=True, default='')

    article_type = models.CharField(max_length=255, null=True, blank=True, default='')
    description = models.CharField(max_length=255, null=True, blank=True, default='')
    novelty = models.CharField(max_length=255, null=True, blank=True, default='')
    limitation = models.CharField(max_length=255, null=True, blank=True, default='')
    research_goal = models.CharField(max_length=255, null=True, blank=True, default='')
    research_objects = models.CharField(max_length=255, null=True, blank=True, default='')
    chemical_class = models.CharField(max_length=200, blank=True)
    exposure_route = models.CharField(max_length=200, blank=True)
    health_effects = models.TextField(blank=True)
    target_organism = models.CharField(max_length=100, blank=True)
    experimental_model = models.CharField(max_length=100, blank=True)
    mechanism = models.TextField(blank=True)
    field_category = models.CharField(max_length=255, blank=True, null=True)
    disease_category = models.CharField(max_length=255, blank=True, null=True)
    technique = models.CharField(max_length=255, blank=True, null=True)
    model_type = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="模型类型"
    )

    def __str__(self):
        return f"{self.pub_year} - {self.journal} - {self.title}"
