import random
import sqlite3

fishlist = [
    #Água doce
    ('Piaba', 2.0, 10.0, 12.0, 'Fih.'),
    ('Carpa', 2.0, 10.0, 50.0, 'Fish, Japan.'),
    ('Traíra', 1.2, 10.0, 40.0, 'O rato dos peixes.'),
    ('Lúcio', 1.0, 10.0, 60.0, 'Peixe favorito do Marcos.'),
    ('Tilápia', 1.0, 10.0, 30.0, 'Um clássico.'),
    ('Pacu', 1.0, 10.0, 35.0, 'E sua boca humanóide.'),
    ('Piranha', 0.7, 10.0, 20.0, 'Sua mãe.'),
    ('Peixe Betta', 0.6, 10.0, 6.0, 'Sobra nada.'),
    ('Barrigudinho', 0.5, 10.0, 4.0, 'Um peixe pequeno, gordo e burro.'),
    ('Dourado', 0.5, 10.0, 120.0, 'Rei do rio.'),
    ('Tambaqui', 0.5, 10.0, 110.0, 'Não coloque num tacho de óleo quente.'),
    ('Bagre', 0.3, 10.0, 70.0, 'Muito Cabeçudo.'),
    ('Pirarucu', 0.12, 10.0, 250.0, 'Um monstro carmesim.'),
    ('Jacaré', 0.1, 10, 500.0, 'O que o cara na minha boca disse?'),
    ('Pirarucu dourado', 0.05, 10.0, 350.0, 'Agora as mulheres te amam e os peixes lhe temem!'),
    ('Lúcio dourado', 0.05, 10.0, 120.0, 'O Marcos vai amar esse.'),
    
    #Água salgada
    ('Atum', 2.0, 10.0, 280.0, 'Qual o som que o peixe faz quando cai?'),
    ('Robalo',2.0, 10.0, 40.0, 'Não vem caixa nessa porra.'),
    ('Tainha', 1.2, 10.0, 45.0, 'Tainha, vinho...'),
    ('Cação', 0.7, 10.0, 160.0, 'Tipo um tubarão só que beta.'),
    ('Polvo', 0.7, 10.0, 100.0, 'As japonesas adoram.'),
    ('Peixe Espada', 0.5, 10.0, 300.0, 'Touche!'),
    ('Peixe palhaço', 0.5, 10.0, 40.0, 'Peixe arthur kkkkkk'),
    ('Tubarão Martelo', 0.3, 10.0, 100.0,'O carpinteiro dos mares.'),
    ('Tubarão Baleia', 0.3, 10.0, 1200.0, 'É um tubarão ou uma baleia?'),
    ('Lula', 0.3, 10.0, 60.0, 'Sem piadas políticas por favor'),
    ('Peixe-Lua', 0.3, 10.0, 300.0, 'Uma piada de mal gosto da evolução.'),
    ('Celacanto', 0.12, 10.0, 200.0, 'Ele parou de evoluir?'),
    ('Tubarão Branco', 0.12, 10.0, 450.0, 'Yo Mr. White!'),
    ('Tubarão duende', 0.1, 10.0, 300., 'Feioso do abismo.'),
    ('Peixe pescador', 0.1, 10.0, 80.0, 'Peixe canibal?'),
    ('Lula vampira do inferno', 0.1, 10.0, 30, 'Nome bom demais pra um bixo tão fofo.'),
    ('Lula colossal', 0.1, 10.0, 1400.0, 'O grande ladrão dos mares.'),
    ('Marlim dourado', 0.05, 10.0, 500.0, 'História de pescador!'),
    ('Sereia', 0.05, 10.0, 150.0, 'Ninguém vai acreditar em você.'),
    
    #Peixes primitivos
    ('Anomalacaris', 0.12, 10.0, 60.0, 'Ele da o seu melhor.'),
    ('Dunkleosteus', 0.12, 10.0, 300.0, 'Slam Dunk!'),
    
    #Peixes bizarros fodase
    ('Peixe Beiçudo', 0.3, 10.0, 40.0, 'Sem dentes.'),
    ('Peixe Lázaro', 0.05, 10.0, 167.0, 'Ele sempre volta'),
    ('Tigrex', 0.05, 10.0, 1700.0, 'E sua hitbox enorme.'),
    ('Larpeixe', 0.05, 10.0, 100.0, 'Ele não sabe o que fala'),
    ("Caboclo D'água", 0.03, 10.0, 190.0, 'baixo, grosso, musculoso e sempre enfezado.'),
    ('Barão Nashor', 0.03, 10.0, 600.0, 'Jogo errado'),
    ('Basculegion', 0.03, 10.0, 300.0, 'Essa porra não é um daqueles monstros de bolso?'),
    ('Magikarp', 0.03, 10.0, 20.0, 'Carpa estranha da porra.'),
    ('Gromp', 0.03, 10.0, 180.0, 'Combem ele!'),
    ('Bloop', 0.01, 10.0, 9000.0, 'Você sabia?'),
    ('Peixe planeta Infernus 67', 0.01, 10.0, 67.0, 'Procurado em 6 ou 7 países por terrorismo.'),
    ('Jormungundr filhote', 0.001, 10, 1000000.0, 'Um peixe misterioso.'),
    
    #lixo
    ('Lixo', 0.1, 3.0, 5.0, 'Literalmente inútil.'),
    ('Madeira velha', 0.1, 10.0, 10.0, 'Um galho a deriva'),
    ('Caixote da selva', 0.1, 10.0, 60.0, 'Mas aqui não serve pra nada.'),
    ('Chave de fenda', 0.1, 10.0, 12, 'Que?...'),
    ('Cadáver humano', 0.05, 0, 180.0, 'Recebeu o tronco, Memento Mori'),
]

def create_database():
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fishes (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            spawn_weight REAL,
            base_price REAL,
            base_size REAL,
            description TEXT
        )
    ''')
    
    #Ligar o pragma depois!!!!!!!!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            fish_id INTEGER,
            size REAL,
            stars INTEGER,
            FOREIGN KEY (fish_id) REFERENCES fishes(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            ronaldos INTEGER PRIMARY KEY
            )
        ''')
    
    #cursor.execute(''')
    
    #print(cursor.execute('SELECT * FROM inventory').fetchall())
    #print(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())

    connection.commit()
    connection.close()

def seed_fishes():
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    
    for name, spawn_weight, base_price, base_size, description in fishlist:
        cursor.execute('''
            INSERT OR IGNORE INTO fishes (name, spawn_weight, base_price, base_size, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, spawn_weight, base_price, base_size, description))
        cursor.execute('''
            UPDATE fishes 
            SET spawn_weight = ?, base_price = ?, base_size = ?, description = ?
            WHERE name = ?
        ''', (spawn_weight, base_price, base_size, description, name))

    connection.commit()
    print("Tudo certo com o banco de dados.")
    connection.close()
    
def get_fishes():
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM fishes')
    fishes = cursor.fetchall()
    connection.close()
    return fishes

def get_weighted_random_fish():
    fishes = get_fishes()
    
    total_weight = sum(fish[2] for fish in fishes)
    random_value = random.uniform(0, total_weight)
    
    cumulative_weight = 0
    for fish in fishes:
        cumulative_weight += fish[2]
        if random_value <= cumulative_weight:
            return fish

def get_user_inventory(user_id):
        connection = sqlite3.connect('data/database.db')
        cursor = connection.cursor()
        
        cursor.execute('''
            SELECT inventory.fish_id, fishes.name, inventory.size, inventory.stars
            FROM inventory
            JOIN fishes ON inventory.fish_id = fishes.id
            WHERE inventory.user_id = ?
        ''', (user_id,))
        inventory_items = cursor.fetchall()
        connection.close()
        
        return inventory_items
        
def add_fish_to_inventory(user_id, fish_id, size, stars):
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO inventory (user_id, fish_id, size, stars)
        VALUES (?, ?, ?, ?)
    ''', (user_id, fish_id, size, stars))
    
    connection.commit()
    connection.close()