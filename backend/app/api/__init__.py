"""
API路由模块
"""

from flask import Blueprint

graph_bp = Blueprint('graph', __name__)
simulation_bp = Blueprint('simulation', __name__)
report_bp = Blueprint('report', __name__)
tianji_bp = Blueprint('tianji', __name__)
tianji_review_bp = Blueprint('tianji-review', __name__)

from . import graph  # noqa: E402, F401
from . import simulation  # noqa: E402, F401
from . import report  # noqa: E402, F401
from . import tianji  # noqa: E402, F401
from . import tianji_review  # noqa: E402, F401

