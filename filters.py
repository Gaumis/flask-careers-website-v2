import babel.numbers


def inr_format(value):
  currency_in_number = value
  return babel.numbers.format_number(currency_in_number, locale="en_IN")
