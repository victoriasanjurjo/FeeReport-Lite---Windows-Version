"""
Pruebas para el servicio de configuración y persistencia JSON.
"""
from src.models.profesional import Profesional
from src.services.config_service import ConfigService


def test_config_service_defaults():
    service = ConfigService()
    pref_curr = service.get_preference("currency_symbol", "$")
    assert pref_curr is not None


def test_config_service_save_profesional(tmp_path, monkeypatch):
    monkeypatch.setattr("src.services.config_service.get_config_dir", lambda: tmp_path)
    service = ConfigService()

    prof = Profesional(nombre="Gonzalo", apellido="Rivas", telefono="11998877", email="gonzalo@test.com")
    assert service.save_profesional(prof) is True

    # Recargar instancia
    service2 = ConfigService()
    prof_recargado = service2.get_profesional()
    assert prof_recargado.nombre == "Gonzalo"
    assert prof_recargado.apellido == "Rivas"
