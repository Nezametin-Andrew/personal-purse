def statistic_msg():
    return """
➖ Для выплат пользователям требуется {p_m} ltc.
💰 Чистый статок на счету после выплат {balance} ltc.
    """


def balance_detail():
    return """
💰 На счету : {balance} ltc.
💸 Не подтвержденный баланс: {un_balance} ltc.
"""