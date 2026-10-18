from django.db import models


class Direccion(models.Model):
    calle = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    comuna = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna} - {self.ciudad}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.nombre} (S/. {self.precio_actual})"


class Proveedor(models.Model):
    codigo = models.CharField(max_length=20, unique=True, help_text="DNI o RUC único")
    nombre = models.CharField(max_length=150)
    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proveedores'
    )
    telefono = models.CharField(max_length=20)
    pagina_web = models.URLField(blank=True, null=True)
    # Un producto es comercializado por varios proveedores, pero un proveedor provee un solo producto
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='proveedores',
        help_text="Producto que provee"
    )

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Cliente(models.Model):
    codigo = models.CharField(max_length=20, unique=True, help_text="DNI o Identificador único")
    nombre = models.CharField(max_length=150)
    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes'
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class TelefonoCliente(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='telefonos'
    )
    numero = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Teléfono de Cliente'
        verbose_name_plural = 'Teléfonos de Clientes'

    def __str__(self):
        return f"{self.numero} ({self.cliente.nombre})"


class Venta(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Descuento en porcentaje o monto fijo"
    )
    monto_final = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Factura #{self.numero_factura} - {self.cliente.nombre} - S/. {self.monto_final}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='detalles_venta'
    )
    precio_momento = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Factura #{self.venta.numero_factura}"
