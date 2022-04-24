from delivery_bot import broadcast_message


def test_delivery_bot():
    assert broadcast_message({"stock_name": "APPL", "buy_or_sell": "buy", "num_of_shares": 150}) == True


if __name__ == "__main__":
    print(f"[testing] starting...")
    test_delivery_bot()
    print(f"[testing] all passed")
