from django.contrib import admin
from .models import (
    Direccion,
    Categoria,
    Producto,
    Proveedor,
    Cliente,
    TelefonoCliente,
    Venta,
    DetalleVenta
)


class TelefonoClienteInline(admin.TabularInline):
    model = TelefonoCliente
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'direccion')
    search_fields = ('codigo', 'nombre')
    inlines = [TelefonoClienteInline]


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'fecha', 'descuento', 'monto_final')
    list_filter = ('fecha',)
    search_fields = ('numero_factura', 'cliente__nombre', 'cliente__codigo')
    inlines = [DetalleVentaInline]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio_actual', 'stock', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'telefono', 'producto')
    search_fields = ('codigo', 'nombre')


admin.site.register(Direccion)
admin.site.register(Categoria)
admin.site.register(TelefonoCliente)
admin.site.register(DetalleVenta)
