class PyPrinterSettings:
    verbose: bool = False
    use_tqdm: bool = True
    delimiter: str = " "


gs_settings = [PyPrinterSettings()]  # Hack to make this a pointer


def get_settings() -> PyPrinterSettings:
    return gs_settings[0]


def is_verbose_mode():
    return get_settings().verbose


def set_verbose_mode(newValue: bool = True):
    get_settings().verbose = newValue


def use_tqdm():
    return get_settings().use_tqdm


def get_delimiter():
    return get_settings().delimiter
