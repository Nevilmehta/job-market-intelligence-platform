from app.core.config import settings

def test_settings_have_app_name():
    assert settings.APP_NAME == "Job Market Intelligence Platform"