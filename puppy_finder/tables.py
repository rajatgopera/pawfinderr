import django_tables2 as tables
from .models import Puppy
from django.utils.html import format_html
from django.urls import reverse

class PuppyTable(tables.Table):
    name = tables.Column(linkify=lambda record: reverse('puppy_detail', args=[record.id]))
    image = tables.Column(empty_values=(), orderable=False)
    actions = tables.Column(empty_values=(), orderable=False, verbose_name='Actions')
    
    class Meta:
        model = Puppy
        template_name = "django_tables2/bootstrap5.html"
        fields = ('image', 'name', 'breed', 'color', 'status', 'last_seen_location', 'last_seen_date')
        attrs = {'class': 'table table-hover'}
    
    def render_image(self, value, record):
        if record.image:
            return format_html(
                '<img src="{}" alt="{}" style="height: 50px; width: 50px; object-fit: cover;" class="rounded-circle">',
                record.image.url,
                record.name
            )
        return ""
    
    def render_actions(self, value, record):
        if record.status == 'LOST':
            return format_html(
                '<a href="{}" class="btn btn-sm btn-success">Found?</a>',
                reverse('mark_as_reunited', args=[record.id])
            )
        return ""
