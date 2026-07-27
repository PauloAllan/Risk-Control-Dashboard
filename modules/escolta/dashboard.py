import streamlit as st

from modules.escolta.crud import load_records
from modules.escolta.utils import currency



def dashboard_page():

    """
    Dashboard de indicadores
    e análise das escoltas.
    """


    st.title("📊 Dashboard de Escoltas")

    st.caption(
        "Indicadores operacionais da gestão de frotas."
    )


    # Busca dados
    df = load_records()


    if df.empty:

        st.info(
            "Ainda não existem registros cadastrados."
        )

        return



    # ==========================
    # KPIs
    # ==========================

    total_operations = len(df)


    total_value = (
        df["valor_carga"]
        .sum()
    )


    average_value = (
        df["valor_carga"]
        .mean()
    )


    comboio_total = (
        df["tipo_escolta"]
        .eq("Comboio")
        .sum()
    )



    col1, col2, col3, col4 = st.columns(4)



    col1.metric(
        "Total de operações",
        total_operations
    )


    col2.metric(
        "Valor total das cargas",
        currency(total_value)
    )


    col3.metric(
        "Valor médio por carga",
        currency(average_value)
    )


    col4.metric(
        "Escoltas em comboio",
        comboio_total
    )



    st.divider()



    # ==========================
    # Gráficos
    # ==========================


    left, right = st.columns(2)



    with left:


        st.subheader(
            "🚛 Operações por transportadora"
        )


        transportadoras = (
            df
            .groupby("transportadora")
            .size()
            .sort_values(
                ascending=False
            )
            .head(10)
        )


        st.bar_chart(
            transportadoras
        )



        st.subheader(
            "🛡 Tipo de escolta"
        )


        tipos = (
            df
            .groupby("tipo_escolta")
            .size()
        )


        st.bar_chart(
            tipos
        )



    with right:


        st.subheader(
            "📍 Cargas por destino"
        )


        destinos = (
            df
            .groupby("destino")["valor_carga"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
        )


        st.bar_chart(
            destinos
        )



        st.subheader(
            "📅 Operações por data"
        )


        operacoes_dia = (
            df
            .groupby(
                df["data"].dt.date
            )
            .size()
        )


        st.line_chart(
            operacoes_dia
        )