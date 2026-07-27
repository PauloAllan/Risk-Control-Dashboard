import sqlite3
from pathlib import Path


# Caminho do banco
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "database" / "painel_escoltas.db"



def get_connection():

    """
    Cria conexão com banco SQLite.
    """

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn



def initialize_database():

    """
    Cria as tabelas necessárias
    caso ainda não existam.
    """

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