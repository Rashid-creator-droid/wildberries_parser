def print_result(
    total_saved: int,
    total_items: int,
    use_filters: bool,
):
    if use_filters:
        print(
            f"\nТоваров прошедших фильтрацию — "
            f"{total_saved} из {total_items} загружено"
        )
    else:
        print(f"\nЗагружено {total_saved} товаров")