"""
Pruebas unitarias para los modelos de datos y cálculos matemáticos/financieros.
"""
from src.models.cliente import Cliente
from src.models.profesional import Profesional
from src.models.presupuesto import ItemPresupuesto, Presupuesto


def test_cliente_nombre_completo():
    c = Cliente(nombre="Carlos", apellido="Gómez", telefono="123456", email="carlos@test.com")
    assert c.nombre_completo == "Carlos Gómez"
    assert c.es_valido() is True

    c_empty = Cliente()
    assert c_empty.es_valido() is False


def test_profesional_serialization():
    p = Profesional(nombre="Ana", apellido="López", telefono="987654", email="ana@test.com")
    data = p.to_dict()
    assert data["nombre"] == "Ana"
    assert data["apellido"] == "López"

    p2 = Profesional.from_dict(data)
    assert p2.nombre_completo == "Ana López"


def test_item_presupuesto_subtotal():
    item = ItemPresupuesto(descripcion="Servicio de diseño UI", cantidad=3.0, precio_unitario=1500.0)
    assert item.subtotal == 4500.0
    assert item.es_valido() is True


def test_presupuesto_calculos_sin_impuesto_ni_descuento():
    p = Presupuesto()
    p.items = [
        ItemPresupuesto(descripcion="Item 1", cantidad=2.0, precio_unitario=100.0),  # 200
        ItemPresupuesto(descripcion="Item 2", cantidad=1.0, precio_unitario=300.0),  # 300
    ]
    p.tasa_descuento = 0.0
    p.aplicar_impuesto = False

    assert p.calcular_subtotal_bruto() == 500.0
    assert p.calcular_monto_descuento() == 0.0
    assert p.calcular_subtotal_neto() == 500.0
    assert p.calcular_monto_impuesto() == 0.0
    assert p.calcular_total() == 500.0


def test_presupuesto_calculos_con_descuento_e_impuesto():
    p = Presupuesto()
    p.items = [
        ItemPresupuesto(descripcion="Consultoría Cloud", cantidad=10.0, precio_unitario=100.0),  # 1000
    ]
    p.tasa_descuento = 10.0      # 10% de 1000 = 100 -> Neto = 900
    p.aplicar_impuesto = True
    p.tasa_impuesto = 21.0       # 21% de 900 = 189 -> Total = 1089

    assert p.calcular_subtotal_bruto() == 1000.0
    assert p.calcular_monto_descuento() == 100.0
    assert p.calcular_subtotal_neto() == 900.0
    assert p.calcular_monto_impuesto() == 189.0
    assert p.calcular_total() == 1089.0
