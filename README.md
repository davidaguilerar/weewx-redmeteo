WeeWX-Redmeteo | Soporte de WeeWX para la Red de Estaciones Meteorológicas Personales Redmeteo.cl
=
Por David Aguilera-Riquelme, para la Red Meteoaficionada de Chile [(Visitar Sitio Web)](https://redmeteo.cl).

Basado en la [Extensión de Weewx-Windguru](https://github.com/claudobahn/weewx-windguru).

Este código está licenciado por la Licencia Pública General versión 3 de GNU (GPLv3). Úsese bajo su propio riesgo. No hay garantías de su funcionamiento.

English: This code adds support to Redmeteo.cl (chilean weather network for enthusiasts of weather and climate) to upload live data as a RESTful service, directly on Red Meteoaficionada's server. This plugin needs at least WeeWX version 3 running on your system. A few bugs: Solar radiation, UV measurements and indoor sensors data are not supported by this plugin.

### Requerimientos: Este plugin necesita al menos WeeWX versión 3 o superior corriendo en tu sistema.

## Instalación en tu sistema corriendo WeeWX 
1. Envía un correo a administracion@redmeteo.cl, para que la admin te envíe los formularios de inscripción a la Red Meteorológica Aficionada y la ID de Usuario de Redmeteo.cl

2. Descarga la extensión vía terminal
    ```
    wget -O weewx-redmeteo.zip https://github.com/davidaguilerar/weewx-redmeteo/archive/master.zip
    ```

3. Ejecuta el instalador del plugin:
    ```
    wee_extension --install weewx-redmeteo.zip
    ```

4. Actualiza el archivo weewx.conf (normalmente se ubica en /etc/weewx/):

    ```
    [StdRESTful]
        [[Redmeteo]]
            idusuario = Tu_ID_usuario_redmeteoCL
    ```

5. Reinicia WeeWX
    ```
    sudo /etc/init.d/weewx stop
    sudo /etc/init.d/weewx start
    ```

## Cosas no soportadas por este plugin

Este plugin no permite transmitir datos de radiación solar/UV ni tampoco sensores de suelo.

### Te invito: Si eres programador Python, puedes ayudarme a extender este plugin, y poder ampliar el soporte de sensores (especialmente de radiación solar).
