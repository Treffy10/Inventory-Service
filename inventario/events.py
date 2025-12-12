def emit_stock_updated(product_id, new_stock):
    print(f"[EVENT] StockUpdated → product={product_id}, stock={new_stock}")

def emit_stock_insufficient(product_id):
    print(f"[EVENT] StockInsufficient → product={product_id}")
