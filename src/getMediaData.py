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
