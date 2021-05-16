from django import template
from django.utils.safestring import mark_safe

from main_app.models import Smartphone

register = template.Library()

TABLE_HEAD = """
                <table class="table">
                    <tbody>
             """

TABLE_TAIL = """
                    </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                        <td>{name}</td>
                        <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'notebook': {
        'Diagonal': 'diagonal',
        'Type of display': 'display_type',
        'Processor frequency': 'processor_freq',
        'RAM memory': 'ram',
        'Video': 'video',
        'Time without charge': 'time_without_charge',
    },
    'smartphone': {
        'Diagonal': 'diagonal',
        'Type of display': 'display_type',
        'Display resolution': 'resolution',
        'Accumulator volume': 'accum_volume',
        'RAM memory': 'ram',
        'Place for SD card': 'sd',
        'Max size of SD card memory': 'sd_volume_max',
        'Main camera megapixels': 'main_cam_mp',
        'Frontal camera megapixels': 'frontal_cam_mp',
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Max size of SD card memory')
        else:
            PRODUCT_SPEC['smartphone']['Max size of SD card memory'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
