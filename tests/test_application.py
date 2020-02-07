from micropy.core import Application


def test_application():
    app = Application()

    assert isinstance(app, Application)
