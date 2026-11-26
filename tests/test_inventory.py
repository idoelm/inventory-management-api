def test_inventory_flow_and_negative_stock_protection(client):
    # 1. יצירת מוצר חדש
    product_response = client.post(
        "/api/v1/products/",
        json={"name": "Laptop", "sku": "LAP-001","price": "3000", "quantity": 0,"description": "laptop to all"},
    )
    assert product_response.status_code in (200, 201)
    product = product_response.json()
    product_id = product["id"]

    # 2. יצירת מחסן חדש
    warehouse_response = client.post(
        "/api/v1/warehouses/",
        json={"name": "Main Warehouse", "location": "Tel Aviv"},
    )
    assert warehouse_response.status_code in (200, 201)
    warehouse = warehouse_response.json()
    warehouse_id = warehouse["id"]

    # 3. תנועת IN של 10 יחידות -> המלאי אמור לעלות ל-10
    in_response = client.post(
        "/api/v1/transactions/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "transaction_type": "IN",
            "quantity": 10,
        },
    )
    assert in_response.status_code in (200, 201)

    product_after_in = client.get(f"/api/v1/products/{product_id}").json()
    assert product_after_in["quantity"] == 10

    # 4. תנועת OUT תקינה של 4 יחידות -> המלאי אמור לרדת ל-6
    out_response = client.post(
        "/api/v1/transactions/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "transaction_type": "OUT",
            "quantity": 4,
        },
    )
    assert out_response.status_code in (200, 201)

    product_after_out = client.get(f"/api/v1/products/{product_id}").json()
    assert product_after_out["quantity"] == 6

    # 5. ניסיון להוציא 20 יחידות כשאין מספיק מלאי -> אמור להיחסם והמלאי נשאר 6
    invalid_out_response = client.post(
        "/api/v1/transactions/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "transaction_type": "OUT",
            "quantity": 20,
        },
    )
    assert invalid_out_response.status_code in (400, 422)

    product_after_invalid_out = client.get(f"/api/v1/products/{product_id}").json()
    assert product_after_invalid_out["quantity"] == 6

def test_transactions_filtering(client):
    # 1. יצירת שני מוצרים ושני מחסנים
    p1 = client.post(
        "/api/v1/products/",
        json={"name": "Laptop", "sku": "LAP-100", "price": 3500.0, "quantity": 0},
    ).json()
    p2 = client.post(
        "/api/v1/products/",
        json={"name": "Mouse", "sku": "MOU-200", "price": 120.0, "quantity": 0},
    ).json()

    w1 = client.post(
        "/api/v1/warehouses/",
        json={"name": "Tel Aviv Hub", "location": "Tel Aviv"},
    ).json()
    w2 = client.post(
        "/api/v1/warehouses/",
        json={"name": "Haifa Hub", "location": "Haifa"},
    ).json()

    # 2. יצירת 3 תנועות שונות
    client.post(
        "/api/v1/transactions/",
        json={"product_id": p1["id"], "warehouse_id": w1["id"], "transaction_type": "IN", "quantity": 10},
    )
    client.post(
        "/api/v1/transactions/",
        json={"product_id": p1["id"], "warehouse_id": w1["id"], "transaction_type": "OUT", "quantity": 3},
    )
    client.post(
        "/api/v1/transactions/",
        json={"product_id": p2["id"], "warehouse_id": w2["id"], "transaction_type": "IN", "quantity": 5},
    )

    res_in = client.get("/api/v1/transactions/", params={"transaction_type": "IN"})
    assert res_in.status_code == 200
    in_items = res_in.json()
    assert len(in_items) == 2
    assert all(item["transaction_type"] == "IN" for item in in_items)

    res_product = client.get("/api/v1/transactions/", params={"product_id": p1["id"]})
    assert res_product.status_code == 200
    product_items = res_product.json()
    assert len(product_items) == 2
    assert all(item["product_id"] == p1["id"] for item in product_items)

    res_combined = client.get(
        "/api/v1/transactions/",
        params={"warehouse_id": w1["id"], "transaction_type": "OUT"},
    )
    assert res_combined.status_code == 200
    combined_items = res_combined.json()
    assert len(combined_items) == 1
    assert combined_items[0]["product_id"] == p1["id"]
    assert combined_items[0]["quantity"] == 3