# Installer for WindGuru WeeWX extension

from weecfg.extension import ExtensionInstaller


def loader():
    return RedmeteoInstaller()


class RedmeteoInstaller(ExtensionInstaller):
    def __init__(self):
        super(RedmeteoInstaller, self).__init__(
            version="0.2",
            name='redmeteo',
            description='Subir datos a Redmeteo.cl',
            restful_services='user.redmeteo.Redmeteo',
            config={
                'StdRESTful': {
                    'Redmeteo': {
                        'idestacion': 'RMCLXXXX',
                        'claveestacion': 'ABCDEFG'}}},
            files=[('bin/user', ['bin/user/redmeteo.py'])]
        )
