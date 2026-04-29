from fastapi import FastAPI

app = FastAPI(title="Operations API")


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id == 1:
        return {
            "id": 1,
            "status": "paid",
            "amount": 12000,
        }

    return {
        "error": "order not found",
    }