WeeWX-Redmeteo | Soporte de WeeWX para la Red de Estaciones Meteorológicas Personales Redmeteo.cl
=
Por David Aguilera-Riquelme, para la Red Meteoaficionada de Chile [(Visitar Sitio Web)](https://redmeteo.cl).

Basado en la [Extensión de Weewx-Windguru](https://github.com/claudobahn/weewx-windguru).

Este código está licenciado por la Licencia Pública General versión 3 de GNU (GPLv3). Úsese bajo su propio riesgo. No hay garantías de su funcionamiento.

### Requerimientos: Este plugin necesita al menos WeeWX versión 3 o superior corriendo en tu sistema.

## Instalación en tu sistema corriendo WeeWX 
1. Envía un correo a redmeteoaficionadachile@gmail.com, para que la admin te envíe los formularios de inscripción y la ID de Usuario de Redmeteo.cl

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
