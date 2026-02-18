from .start import register_start_handlers
from .buy import register_buy_handlers
from .my_subs import register_my_sub_handlers
from .points import register_points_handlers

def register_handlers(app):
    register_start_handlers(app)
    register_buy_handlers(app)
    register_my_sub_handlers(app)
    register_points_handlers(app)
