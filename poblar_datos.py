import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab03.settings')
django.setup()

from encuesta.models import Pregunta, Opcion
from ventas.models import (
    Direccion,
    Categoria,
    Producto,
    Proveedor,
    Cliente,
    TelefonoCliente,
    Venta,
    DetalleVenta
)
from django.contrib.auth import get_user_model


def poblar_encuesta():
    print("-> Poblando datos para la app 'encuesta'...")
    Pregunta.objects.all().delete()
    Opcion.objects.all().delete()

    # Pregunta 1
    p1 = Pregunta.objects.create(
        pregunta_texto="Hora que te levantas:",
        pub_date=timezone.now()
    )
    Opcion.objects.create(pregunta=p1, opcion_texto="6am", votos=0)
    Opcion.objects.create(pregunta=p1, opcion_texto="7am", votos=0)
    Opcion.objects.create(pregunta=p1, opcion_texto="8am", votos=0)

    # Pregunta 2
    p2 = Pregunta.objects.create(
        pregunta_texto="Te movilizas en:",
        pub_date=timezone.now()
    )
    Opcion.objects.create(pregunta=p2, opcion_texto="Taxi", votos=0)
    Opcion.objects.create(pregunta=p2, opcion_texto="Bus", votos=0)
    Opcion.objects.create(pregunta=p2, opcion_texto="Auto propio", votos=0)

    print(f"   [OK] {Pregunta.objects.count()} preguntas creadas y {Opcion.objects.count()} opciones creadas.")


def poblar_ventas():
    print("-> Poblando datos ficticios para la app 'ventas' (Caso de Estudio)...")
    DetalleVenta.objects.all().delete()
    Venta.objects.all().delete()
    TelefonoCliente.objects.all().delete()
    Proveedor.objects.all().delete()
    Cliente.objects.all().delete()
    Producto.objects.all().delete()
    Categoria.objects.all().delete()
    Direccion.objects.all().delete()

    # 1. Direcciones
    dir_prov1 = Direccion.objects.create(
        calle="Av. Los Ingenieros", numero="450", comuna="Santiago de Surco", ciudad="Lima"
    )
    dir_prov2 = Direccion.objects.create(
        calle="Jr. Paruro", numero="1204", comuna="Cercado de Lima", ciudad="Lima"
    )
    dir_cli1 = Direccion.objects.create(
        calle="Av. Javier Prado Este", numero="2150", comuna="San Borja", ciudad="Lima"
    )
    dir_cli2 = Direccion.objects.create(
        calle="Calle Las Camelias", numero="340", comuna="San Isidro", ciudad="Lima"
    )

    # 2. Categorías
    cat_comp = Categoria.objects.create(
        nombre="Cómputo y Laptops",
        descripcion="Equipos portátiles, componentes y estaciones de trabajo."
    )
    cat_perif = Categoria.objects.create(
        nombre="Periféricos",
        descripcion="Teclados, mouse, audífonos y accesorios ergonómicos."
    )

    # 3. Productos
    prod1 = Producto.objects.create(
        nombre="Laptop Lenovo ThinkPad E14",
        precio_actual=3450.00,
        stock=15,
        categoria=cat_comp
    )
    prod2 = Producto.objects.create(
        nombre="Mouse Inalámbrico Logitech MX Master 3S",
        precio_actual=420.00,
        stock=30,
        categoria=cat_perif
    )
    prod3 = Producto.objects.create(
        nombre="Monitor Dell UltraSharp 27'' 4K",
        precio_actual=1850.00,
        stock=8,
        categoria=cat_comp
    )

    # 4. Proveedores (un producto comercializado por varios proveedores, un proveedor provee un solo producto)
    prov1 = Proveedor.objects.create(
        codigo="20100456781",
        nombre="TechDistribuciones S.A.C.",
        direccion=dir_prov1,
        telefono="01-4458920",
        pagina_web="https://www.techdist.example.com",
        producto=prod1
    )
    prov2 = Proveedor.objects.create(
        codigo="20500891234",
        nombre="Importaciones Cómputo Perú",
        direccion=dir_prov2,
        telefono="01-3321456",
        pagina_web="https://www.importcomputo.example.com",
        producto=prod1  # El prod1 también es comercializado por prov2
    )
    prov3 = Proveedor.objects.create(
        codigo="20601234567",
        nombre="Accesorios & Periféricos Global",
        direccion=dir_prov1,
        telefono="01-5542311",
        pagina_web="https://www.accglobal.example.com",
        producto=prod2
    )

    # 5. Clientes
    cli1 = Cliente.objects.create(
        codigo="72458912",
        nombre="Juan Carlos Pérez Rodríguez",
        direccion=dir_cli1
    )
    TelefonoCliente.objects.create(cliente=cli1, numero="987654321")
    TelefonoCliente.objects.create(cliente=cli1, numero="912345678")

    cli2 = Cliente.objects.create(
        codigo="75123490",
        nombre="María Fernanda Gómez Salas",
        direccion=dir_cli2
    )
    TelefonoCliente.objects.create(cliente=cli2, numero="998877665")

    # 6. Ventas y Detalles de Venta
    # Venta 1: Cliente 1 compra 1 laptop y 1 mouse
    v1 = Venta.objects.create(
        numero_factura="F001-00001001",
        cliente=cli1,
        descuento=50.00,
        monto_final=3820.00
    )
    DetalleVenta.objects.create(
        venta=v1,
        producto=prod1,
        precio_momento=3450.00,
        cantidad=1,
        monto_total=3450.00
    )
    DetalleVenta.objects.create(
        venta=v1,
        producto=prod2,
        precio_momento=420.00,
        cantidad=1,
        monto_total=420.00
    )

    # Venta 2: Cliente 2 compra 2 monitores (descuento 100)
    v2 = Venta.objects.create(
        numero_factura="F001-00001002",
        cliente=cli2,
        descuento=100.00,
        monto_final=3600.00
    )
    DetalleVenta.objects.create(
        venta=v2,
        producto=prod3,
        precio_momento=1850.00,
        cantidad=2,
        monto_total=3700.00
    )

    print(f"   [OK] {Cliente.objects.count()} clientes, {Producto.objects.count()} productos y {Venta.objects.count()} ventas registradas exitosamente.")


def crear_superusuario():
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("-> Superusuario creado: usuario 'admin' / contraseña 'admin123'")
    else:
        print("-> Superusuario 'admin' ya existe.")


if __name__ == "__main__":
    print("=== Inicializando población de datos de prueba ===")
    poblar_encuesta()
    poblar_ventas()
    crear_superusuario()
    print("=== Proceso completado exitosamente ===")
