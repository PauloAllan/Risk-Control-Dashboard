import pandas as pd

from modules.escolta.database import get_connection



def insert_record(values):

    """
    Insere um novo registro de escolta no banco.
    """

    with get_connection() as conn:

        conn.execute(
            """
            INSERT INTO escoltas
            (
                data,
                placa,
                transportadora,
                valor_carga,
                destino,
                ae,
                tipo_escolta,
                observacao,
                horario_apresentacao,
                horario_saida
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """,
            values
        )



def update_record(record_id, values):

    """
    Atualiza um registro existente.
    """

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE escoltas

            SET

                data = ?,
                placa = ?,
                transportadora = ?,
                valor_carga = ?,
                destino = ?,
                ae = ?,
                tipo_escolta = ?,
                observacao = ?,
                horario_apresentacao = ?,
                horario_saida = ?

            WHERE id = ?

            """,
            (*values, record_id)
        )



def delete_record(record_id):

    """
    Remove um registro pelo ID.
    """

    with get_connection() as conn:

        conn.execute(
            """
            DELETE FROM escoltas
            WHERE id = ?

            """,
            (record_id,)
        )



def load_records():

    """
    Busca todos os registros
    e retorna um DataFrame.
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            """
            SELECT *

            FROM escoltas

            ORDER BY data DESC, id DESC

            """,
            conn
        )


    if not df.empty:

        df["data"] = pd.to_datetime(
            df["data"]
        )


    return df



def get_record(record_id):

    """
    Busca um registro específico pelo ID.
    """

    with get_connection() as conn:

        result = conn.execute(
            """
            SELECT *

            FROM escoltas

            WHERE id = ?

            """,
            (record_id,)
        ).fetchone()


    if result:

        return dict(result)


    return None