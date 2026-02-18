from .buy import register_buy_handlers
from .my_subs import register_my_sub_handlers


def register_handlers(bot):

    register_buy_handlers(bot)
    register_my_sub_handlers(bot)
