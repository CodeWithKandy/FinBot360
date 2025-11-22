# data/parser.py

def parse_holdings(input_string):
    holdings = []
    try:
        pairs = input_string.split(',')
        for pair in pairs:
            if '=' in pair:
                parts = pair.strip().split('=')
                ticker = parts[0].strip().upper()
                rest = parts[1].strip()
                
                buy_price = None
                if '@' in rest:
                    qty_str, price_str = rest.split('@')
                    quantity = float(qty_str.strip())
                    buy_price = float(price_str.strip())
                else:
                    quantity = float(rest)
                
                holdings.append({
                    "ticker": ticker,
                    "quantity": quantity,
                    "buy_price": buy_price
                })
    except Exception as e:
        print(f"[ERROR] Failed to parse holdings: {e}")
    return holdings
