import sqlite3

DB_PATH = 'GENERAL_INVENTORY.db'

def setup_database():
    """Cria a tabela de inventário genérica se ela não existir."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_type TEXT NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            size REAL,
            rarity TEXT,
            base_value INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
def add_item(user_id, item_type, item_name, quantity=1, size=None, rarity=None, base_value=None):
    """Adiciona um item ao inventário de um usuário, usando tags para flexibilidade."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inventory (user_id, item_type, item_name, quantity, size, rarity, base_value)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, item_type, item_name, quantity, size, rarity, base_value))
    conn.commit()
    conn.close()

def get_inventory(user_id):
    """Recupera o inventário completo de um usuário."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT item_type, item_name, quantity, size, rarity, base_value, timestamp
        FROM inventory
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (user_id,))
    inventory_data = cursor.fetchall()
    conn.close()
    return inventory_data