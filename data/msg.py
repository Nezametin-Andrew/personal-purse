def statistic_msg():
    return """
➖ Для выплат пользователям требуется {p_m} ltc.
💰 Чистый остаток на счету после выплат {balance} ltc.
    """


def balance_detail():
    return """
💰 На счету : {balance} ltc.
💸 Неподтвержденный баланс: {un_balance} ltc.
"""