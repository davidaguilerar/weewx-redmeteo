WeeWX-Redmeteo | Soporte de WeeWX para la Red de Estaciones Meteorológicas Personales Redmeteo.cl
=
Por David Aguilera-Riquelme, para la Red Meteorológica Aficionada de Chile [(Visitar Sitio Web)](https://redmeteo.cl).

Basado en la [Extensión de Weewx-Windguru](https://github.com/claudobahn/weewx-windguru).

Este código está licenciado por la Licencia Pública General versión 3 de GNU (GPLv3). Úsese bajo su propio riesgo. No hay garantías de su funcionamiento.

**Abstract in English** : This code adds support to *Redmeteo.cl* (chilean weather network for enthusiasts of weather and climate) to upload live data as a RESTful service, directly on Red Meteoaficionada's server. This plugin needs at least WeeWX version 3 running on your system. Note: Solar radiation, UV measurements and indoor sensors data *are not supported* by this plugin.

### Requerimientos: Este plugin necesita al menos WeeWX versión 3 o superior corriendo en tu sistema.

## Instalación en tu sistema corriendo WeeWX 
1. Envía un correo a redmeteoaficionadachile@gmail.com, para que la admin te envíe los formularios de inscripción a la Red Meteorológica Aficionada y la ID de Usuario de Redmeteo.cl
*Send an email to redmeteoaficionadachile@gmail.com in order to get the sign-up forms from the Redmeteo.cl Administration, and the Redmeteo User ID*

2. Descarga la extensión vía terminal
*Donwload the extension using a shell*
    ```
    wget -O weewx-redmeteo.zip https://github.com/davidaguilerar/weewx-redmeteo/archive/master.zip
    ```

3. Ejecuta el instalador del plugin:
*Execute the plugin install script*
    ```
    wee_extension --install weewx-redmeteo.zip
    ```

4. Actualiza el archivo weewx.conf (normalmente se ubica en /etc/weewx/):
*Update weewx.conf file (normally located at /etc/weewx/)*
    ```
    [StdRESTful]
        [[Redmeteo]]
            idusuario = Tu_ID_usuario_redmeteoCL
    ```

5. Reinicia WeeWX
*Restart WeeWX*
    ```
    sudo /etc/init.d/weewx stop
    sudo /etc/init.d/weewx start
    ```

## Cosas no soportadas por este plugin

Este plugin no permite transmitir datos de radiación solar/UV ni tampoco sensores de suelo.

### Te invito: Si eres programador Python, puedes ayudarme a extender este plugin, y poder ampliar el soporte de sensores (especialmente de radiación solar).
