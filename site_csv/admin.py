from django.contrib import admin

from site_csv.models import User, Column, Schema, CSVData

admin.site.register(User)
admin.site.register(Column)
admin.site.register(Schema)
admin.site.register(CSVData)

