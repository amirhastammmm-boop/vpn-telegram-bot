def payment_success(bot, user_id, plan):

    config = create_wireguard_config(user_id)

    # ذخیره کانفیگ
    save_user_config(user_id, config)

    bot.send_message(
        user_id,
        "✅ پرداخت تایید شد\n\nکانفیگ شما:"
    )

    bot.send_document(
        user_id,
        config
    )

    add_points(user_id, 10)
