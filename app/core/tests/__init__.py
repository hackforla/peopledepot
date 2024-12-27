import warnings

from _pytest.mark.structures import PytestUnknownMarkWarning

warnings.filterwarnings("ignore", category=PytestUnknownMarkWarning)
