from django.db import models


class PI(models.Model):
    name = models.CharField('姓名', db_column='姓名', max_length=50)
    phone = models.CharField('手机号', db_column='手机号', max_length=20)
    relationship = models.CharField('身份关系', db_column='身份关系', max_length=50)
    building = models.CharField('楼栋', db_column='楼栋', max_length=50)
    unit = models.CharField('单元', db_column='单元', max_length=50)
    room = models.CharField('房号', db_column='房号', max_length=50)
    property_type = models.CharField('房屋属性', db_column='房屋属性', max_length=20)

    class Meta:
        db_table = 'PI'
        verbose_name = '信息统计'
        verbose_name_plural = '信息统计'

    def __str__(self):
        return f'{self.name} {self.building}{self.unit}{self.room}'
