from django.db import models


class Service(models.Model):
    name = models.CharField('Tên dịch vụ', max_length=120)
    slug = models.SlugField('Đường dẫn', unique=True)
    short_description = models.CharField('Mô tả ngắn', max_length=255)
    process = models.TextField('Quy trình')
    benefits = models.TextField('Lợi ích')
    is_active = models.BooleanField('Đang hiển thị', default=True)

    class Meta:
        verbose_name = 'Dịch vụ'
        verbose_name_plural = 'Dịch vụ'

    def __str__(self):
        return self.name

class PriceItem(models.Model):
    service = models.ForeignKey(Service, verbose_name='Dịch vụ', on_delete=models.CASCADE, related_name='price_items')
    item_name = models.CharField('Hạng mục', max_length=150)
    price = models.DecimalField('Giá', max_digits=12, decimal_places=0)
    unit = models.CharField('Đơn vị', max_length=50, blank=True, help_text='Ví dụ: /chiếc')

    class Meta:
        verbose_name = 'Bảng giá'
        verbose_name_plural = 'Bảng giá'

    def __str__(self):
        return self.item_name
