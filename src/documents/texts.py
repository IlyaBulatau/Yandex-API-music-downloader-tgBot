BUTTON_TEXT = {
    'search': 'Search music',
    'coins': 'Coins'
}

COMMANDS = {
    'start': f'You can download 1 track per day for free using the "{BUTTON_TEXT["search"]}" button\n\n\
In order to download more than 1 track per day, you can purchase coins by clicking the {BUTTON_TEXT["coins"]} button\n\n\
Feedback: @Ilbltv'
}

CALLBACK = {
    'coins': 'get_coins_by_uset_tg_id',
}