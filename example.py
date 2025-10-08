# Transpiled from P-Lang

print("--- P-Lang Configuration Example ---")

db_config = {
    "Production": {"host": "prod.db.internal", "user": "prod_user", "timeout": 30},
    "Development": {"host": "localhost", "user": "dev_user", "timeout": 5},
}
current_stance = "Production"
print(f"Current resolution stance is: {current_stance}")
active_config = db_config[current_stance]
print(f"Connecting to database at: {active_config['host']}")
print("------------------------------------")
current_stance = "Development"
print(f"Current resolution stance is: {current_stance}")
active_config = db_config[current_stance]
print(f"Connecting to database at: {active_config['host']}")
print("------------------------------------")
