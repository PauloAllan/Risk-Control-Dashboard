from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_FOLDER = BASE_DIR / "database"

DATABASE_FOLDER.mkdir(
    exist_ok=True
)


DB_PATH = DATABASE_FOLDER / "painel_escoltas.db"



def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn



def initialize_database():

    with get_connection() as conn:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS escoltas (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                data TEXT NOT NULL,

                placa TEXT NOT NULL,

                transportadora TEXT NOT NULL,

                valor_carga REAL NOT NULL,

                destino TEXT NOT NULL,

                ae TEXT NOT NULL,

                tipo_escolta TEXT NOT NULL,

                observacao TEXT,

                horario_apresentacao TEXT NOT NULL,

                horario_saida TEXT NOT NULL,

                criado_em TEXT DEFAULT CURRENT_TIMESTAMP

            )
            """
        )