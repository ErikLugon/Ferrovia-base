import sqlite3
import logging

DB_PATH = 'GENERAL_INVENTORY.db'

logger = logging.getLogger(__name__)

def setup_database():
    """Cria as tabelas necessárias se não existirem: inventory e global_settings."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabela de inventário
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
    # Tabela para configurações globais (chave, valor, última atualização como ISO string)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            last_update TEXT
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

def get_global_setting(key):
    """Retorna um tuple (value, last_update) ou None se não existir."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT value, last_update FROM global_settings WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        logger.debug("get_global_setting: key=%s -> %s", key, row)
        return row
    logger.debug("get_global_setting: key=%s -> None", key)
    return None

def set_global_setting(key, value, last_update=None):
    """Insere ou atualiza uma configuração global. `last_update` deve ser string ISO de data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO global_settings (key, value, last_update)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value, last_update=excluded.last_update
    ''', (key, value, last_update))
    conn.commit()
    conn.close()
    logger.debug("set_global_setting: key=%s value=%s last_update=%s", key, value, last_update)