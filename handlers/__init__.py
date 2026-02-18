from .buy import register_buy_handlers
from .my_subs import register_my_sub_handlers
from .points import register_points_handlers
from .start import register_start_handler


def register_handlers(bot):

    register_start_handler(bot)
    register_buy_handlers(bot)
    register_my_sub_handlers(bot)
    register_points_handlers(bot)
