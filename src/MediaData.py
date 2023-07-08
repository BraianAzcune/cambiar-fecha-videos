import os
import datetime
from win32com.propsys import propsys, pscon


def getFechaProduccion(path: str):
    properties = propsys.SHGetPropertyStoreFromParsingName(os.path.normpath(path))
    dt = properties.GetValue(pscon.PKEY_Media_DateEncoded)
    dt = dt.GetValue()
    if not isinstance(dt, datetime.datetime):
        # sys.exit("version incorrecta de tiempo python dt")
        return None
    return dt


def updateDateProduction(path_origin, path_to_update):
    print("se recibe", path_origin, path_to_update)
    if path_origin == path_to_update:
        print("origen y destino iguales")
        return
    print("carga origen")
    properties = propsys.SHGetPropertyStoreFromParsingName(
        os.path.normpath(path_origin)
    )
    print("pedir fecha a origen")
    dt = properties.GetValue(pscon.PKEY_Media_DateEncoded)

    # el tercer parametro en 2, significa abrir para poder editar
    print("cargar destino")
    properties2 = propsys.SHGetPropertyStoreFromParsingName(
        os.path.normpath(path_to_update), None, 2
    )
    print("antes de actualizar")
    properties2.SetValue(pscon.PKEY_Media_DateEncoded, dt)
    print("antes de commit")
    properties2.Commit()
