from masks import get_mask_card_number, get_mask_account

def mask_account_card(number_acc_or_card: str) -> str:
    """Функция обработки информации о картах и счетах"""
    if number_acc_or_card.startswith("Счет"):
        masked_data = get_mask_account(number_acc_or_card)
    else:
        masked_data = get_mask_card_number(number_acc_or_card)

    return masked_data


def get_date(date_info: str) -> str:
    """Функция форматирования даты"""

    date_str = date_info.strip()
    masked = f"{date_str[8:10]}.{date_str[5:7]}.{date_str[:4]}"
    return masked



card_number = "Visa Platinum 7000792289606361"
account_number = "Счет 73654108430135874305"
date_info = "2024-03-11T02:26:18.671407"
#print(get_mask_card_number(card_number))
#print(get_mask_account(account_number))
print(get_date(date_info))
