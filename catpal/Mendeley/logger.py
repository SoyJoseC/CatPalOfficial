class logcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class logtypes:
    INFO = 'INFO:'
    ERROR = 'ERROR'
    WARNING = 'WARNING'


def log_info(info):
    print(logcolors.OKGREEN, logtypes.INFO, info, logcolors.ENDC)
    pass


def log_error(error):
    print(logcolors.FAIL, logtypes.ERROR, error, logcolors.ENDC)
    pass


def log_warning(warning):
    print(logcolors.WARNING, logtypes.WARNING, warning, logcolors.ENDC)
    pass