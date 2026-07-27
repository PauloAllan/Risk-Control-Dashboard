import pandas as pd



def currency(value: float) -> str:
    """
    Formata valores monetários
    para padrão brasileiro.
    
    Exemplo:
    85000.50 -> R$ 85.000,50
    """

    return (
        f"R$ {value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )



def format_date(value) -> str:
    """
    Converte data para formato brasileiro.
    """

    if pd.isna(value):
        return ""

    return pd.to_datetime(
        value
    ).strftime("%d/%m/%Y")



def format_record(record) -> str:
    """
    Formata um registro para seleção
    em componentes Streamlit.
    """

    return (
        f"{record['placa']} | "
        f"{format_date(record['data'])} | "
        f"A.E. {record['ae']}"
    )



def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara dataframe para exibição.
    Remove colunas internas e formata campos.
    """

    display = df.copy()


    display = display.drop(
        columns=[
            "id",
            "criado_em"
        ],
        errors="ignore"
    )


    if "data" in display.columns:

        display["data"] = (
            pd.to_datetime(display["data"])
            .dt.strftime("%d/%m/%Y")
        )


    if "valor_carga" in display.columns:

        display["valor_carga"] = (
            display["valor_carga"]
            .apply(currency)
        )


    return display