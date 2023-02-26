from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView

from site_csv.forms import SchemaForm, CSVDataForms
from site_csv.forms import ColumnForm
from site_csv.models import Column, User, CSVData, Schema
from site_csv.utils import create_csv


class Login(LoginView):
    """
    Class for user authentication
    """
    model = User
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('create_schema')


class LogOut(LogoutView):
    """
    Class for logout
    """
    model = User
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('login')


@login_required
def create_schema_and_column(request):
    """
    Function for Schema and Column on one page
    :param request:
    :return:
    """
    if request.method == "GET":
        column = Column.objects.all()
        context = {
            "title": "New schema",
            "schemas_form": SchemaForm(),
            "column_form": ColumnForm(),
            "column": column,
        }
        return render(request, 'site_csv/schema_new.html', context=context)

    if request.method == "POST":
        columns_form = ColumnForm(request.POST)
        if columns_form.is_valid():
            columns_form.save()
            return HttpResponseRedirect(
                reverse("create_schema")
            )

        schema_edit = request.POST.copy()
        schema_edit["columns"] = Column.objects.all()
        form = SchemaForm(schema_edit)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("create_schema"))

    return HttpResponseRedirect(reverse("create_schema"))


@login_required
def create_csv_file(request, pk):
    """
    Function for creating csv files
    :param request:
    :param pk:
    :return:
    """
    if request.method == "GET":
        column = Column.objects.all()
        schema = Schema.objects.get(pk=pk)
        csv_data = CSVData.objects.filter(schema=schema)
        context = {
            "csv_data_forms": CSVDataForms(),
            "column": column,
            "schema": schema,
            "csv_data": csv_data,
        }
        return render(
            request,
            "site_csv/create_csv.html",
            context=context
        )
    if request.method == "POST":
        form = CSVDataForms(request.POST)
        rows = request.POST.get("rows")
        schema = Schema.objects.get(pk=pk)
        csv_data = CSVData.objects.filter(schema=schema)

        create_csv(rows, schema)

        context = {
            "csv_data_forms": CSVDataForms(),
            "schema": schema,
            "csv_data": csv_data,
        }
        return render(
            request,
            "site_csv/create_csv.html",
            context=context
        )


@login_required
def delete_column(request, pk):
    """
    Function for deleting Column
    :param request:
    :param pk:
    :return:
    """
    basket = Column.objects.get(pk=pk)
    basket.delete()
    return redirect('create_schema')


@login_required
def delete_schema(request, pk):
    """
    Function for deleting Schem
    :param request:
    :param pk:
    :return:
    """
    basket = Schema.objects.get(pk=pk)
    basket.delete()
    return redirect('schema_list')


class SchemaListViews(LoginRequiredMixin, ListView):
    """
    A class for displaying the Schem list
    """
    fields = "__all__"
    model = Schema
    template_name = 'site_csv/schema_list.html'


class UpdateSchema(LoginRequiredMixin, UpdateView):
    """
    A class for updating Schem
    """
    fields = '__all__'
    model = Schema
    template_name = 'site_csv/schema_update.html'
