"""Painel de Controle de Escoltas.

Execute com: streamlit run app.py
"""
from __future__ import annotations

import sqlite3
from datetime import date, time
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "painel_escoltas.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
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


def insert_record(values: tuple) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO escoltas
            (data, placa, transportadora, valor_carga, destino, ae, tipo_escolta,
             observacao, horario_apresentacao, horario_saida)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            values,
        )


def load_records() -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM escoltas ORDER BY data DESC, id DESC", conn)
    if df.empty:
        return df
    df["data"] = pd.to_datetime(df["data"])
    return df


def to_excel(df: pd.DataFrame) -> bytes:
    export = df.copy()
    export = export.rename(
        columns={
            "data": "Data",
            "placa": "Placa",
            "transportadora": "Transportadora",
            "valor_carga": "Valor da carga",
            "destino": "Destino",
            "ae": "A.E.",
            "tipo_escolta": "Tipo de escolta",
            "observacao": "Observação",
            "horario_apresentacao": "Horário de apresentação",
            "horario_saida": "Horário de saída",
        }
    )
    export["Data"] = pd.to_datetime(export["Data"]).dt.strftime("%d/%m/%Y")
    export = export.drop(columns=[column for column in ["id", "criado_em"] if column in export])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export.to_excel(writer, index=False, sheet_name="Escoltas")
        sheet = writer.sheets["Escoltas"]
        sheet.freeze_panes = "A2"
        for column in sheet.columns:
            letter = column[0].column_letter
            width = max(len(str(cell.value or "")) for cell in column) + 2
            sheet.column_dimensions[letter].width = min(width, 42)
    return output.getvalue()


def currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def set_page(page: str) -> None:
    st.session_state.page = page
    st.session_state.navigation = page


def home_page() -> None:
    st.markdown("<h1>Controle de Escoltas</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Centralize cadastros, acompanhe operações e analise seus resultados.</p>", unsafe_allow_html=True)
    st.divider()
    left, center, right = st.columns(3, gap="large")
    with left:
        st.markdown("### 📝 Novo registro")
        st.write("Cadastre dados da carga, veículo, horários e escolta.")
        st.button("Adicionar informações", use_container_width=True, on_click=set_page, args=("Cadastro",))
    with center:
        st.markdown("### 📋 Registros")
        st.write("Consulte todos os lançamentos e exporte sua planilha.")
        st.button("Ver tabela", use_container_width=True, on_click=set_page, args=("Registros",))
    with right:
        st.markdown("### 📊 Dashboard")
        st.write("Visualize indicadores, destinos e transportadoras.")
        st.button("Abrir dashboard", use_container_width=True, on_click=set_page, args=("Dashboard",))


def form_page() -> None:
    st.title("Adicionar informações")
    st.caption("Preencha os dados da operação. Os campos com * são obrigatórios.")
    with st.form("cadastro_escolta", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            operation_date = st.date_input("Data *", value=date.today(), format="DD/MM/YYYY")
            plate = st.text_input("Placa *", placeholder="ABC1D23").upper().strip()
            carrier = st.text_input("Transportadora *", placeholder="Nome da transportadora").strip()
            cargo_value = st.number_input("Valor da carga (R$) *", min_value=0.0, step=100.0, format="%.2f")
            destination = st.text_input("Destino *", placeholder="Cidade / UF").strip()
        with col2:
            ae = st.text_input("A.E. (8 dígitos) *", max_chars=8, placeholder="00000000").strip()
            escort_type = st.radio("Tipo de escolta *", ["Individual", "Comboio"], horizontal=True)
            presentation = st.time_input("Horário de apresentação *", value=time(8, 0))
            departure = st.time_input("Horário de saída *", value=time(9, 0))
            observation = st.text_area("Observação", placeholder="Informações adicionais", height=105).strip()
        submitted = st.form_submit_button("Salvar registro", type="primary", use_container_width=True)

    if submitted:
        errors = []
        if not plate:
            errors.append("Informe a placa.")
        if not carrier:
            errors.append("Informe a transportadora.")
        if not destination:
            errors.append("Informe o destino.")
        if not (ae.isdigit() and len(ae) == 8):
            errors.append("A.E. deve conter exatamente 8 dígitos numéricos.")
        if errors:
            st.error(" ".join(errors))
        else:
            insert_record((operation_date.isoformat(), plate, carrier, cargo_value, destination, ae,
                           escort_type, observation, presentation.strftime("%H:%M"), departure.strftime("%H:%M")))
            st.success("Registro salvo com sucesso.")


def records_page() -> None:
    st.title("Registros de escolta")
    df = load_records()
    if df.empty:
        st.info("Ainda não existem registros. Use a página “Adicionar informações” para começar.")
        return
    display = df.drop(columns=["id", "criado_em"], errors="ignore").copy()
    display["data"] = display["data"].dt.strftime("%d/%m/%Y")
    display["valor_carga"] = display["valor_carga"].map(currency)
    display = display.rename(columns={
        "data": "Data", "placa": "Placa", "transportadora": "Transportadora",
        "valor_carga": "Valor carga", "destino": "Destino", "ae": "A.E.",
        "tipo_escolta": "Tipo de escolta", "observacao": "Observação",
        "horario_apresentacao": "Apresentação", "horario_saida": "Saída",
    })
    st.download_button("⬇️ Baixar em Excel", data=to_excel(df), file_name="controle_escoltas.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary")
    st.dataframe(display, use_container_width=True, hide_index=True, height=500)


def dashboard_page() -> None:
    st.title("Dashboard")
    df = load_records()
    if df.empty:
        st.info("O dashboard será exibido assim que houver registros cadastrados.")
        return
    total = len(df)
    total_value = df["valor_carga"].sum()
    average = df["valor_carga"].mean()
    comboios = int((df["tipo_escolta"] == "Comboio").sum())
    a, b, c, d = st.columns(4)
    a.metric("Total de operações", total)
    b.metric("Valor total das cargas", currency(total_value))
    c.metric("Valor médio por carga", currency(average))
    d.metric("Operações em comboio", comboios)
    st.divider()
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Operações por transportadora")
        carriers = df.groupby("transportadora").size().sort_values(ascending=False).head(10)
        st.bar_chart(carriers, color="#1f77b4")
        st.subheader("Tipo de escolta")
        st.bar_chart(df.groupby("tipo_escolta").size(), color="#f59e0b")
    with col_right:
        st.subheader("Valor das cargas por destino")
        destinations = df.groupby("destino")["valor_carga"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(destinations, color="#10b981")
        st.subheader("Operações por data")
        daily = df.groupby(df["data"].dt.date).size()
        st.line_chart(daily, color="#8b5cf6")


def main() -> None:
    st.set_page_config(page_title="Controle de Escoltas", page_icon="🚚", layout="wide")
    st.markdown("""
        <style>
        .stApp { background: #f7f9fc; }
        h1, h2, h3 { color: #17365d; }
        .subtitle { color: #62748a; font-size: 1.1rem; }
        [data-testid="stMetricValue"] { color: #17365d; }
        </style>
    """, unsafe_allow_html=True)
    initialize_database()
    if "page" not in st.session_state:
        st.session_state.page = "Início"
    if "navigation" not in st.session_state:
        st.session_state.navigation = st.session_state.page
    with st.sidebar:
        st.markdown("# 🚚")
        st.title("Escoltas")
        page = st.radio("Navegação", ["Início", "Cadastro", "Registros", "Dashboard"], key="navigation")
        if page != st.session_state.page:
            st.session_state.page = page
    pages = {"Início": home_page, "Cadastro": form_page, "Registros": records_page, "Dashboard": dashboard_page}
    pages[st.session_state.page]()


if __name__ == "__main__":
    main()
