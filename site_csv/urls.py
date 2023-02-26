from django.urls import path

from site_csv.views import create_schema_and_column, delete_column, Login, create_csv_file, \
    SchemaListViews, delete_schema, UpdateSchema, LogOut

urlpatterns = [
    path('', SchemaListViews.as_view(), name='schema_list'),
    path('new-schema/', create_schema_and_column, name='create_schema'),
    path('schema-update/<int:pk>', UpdateSchema.as_view(), name='schema_update'),
    path('create-csv/<int:pk>', create_csv_file, name='create_csv'),
    path('schema-delete/<int:pk>', delete_schema, name='schema_delete'),
    path('column-delete/<int:pk>', delete_column, name='columns_delete'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
]
