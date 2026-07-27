import streamlit as st

from components.navbar import navbar


# Configuração

st.set_page_config(
    page_title="Risk Control Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Remover sidebar

st.markdown(
    """
    <style>

    [data-testid="stSidebar"] {
        display:none;
    }


    [data-testid="stSidebarCollapsedControl"] {
        display:none;
    }


    .stApp {

        background-color:#0f172a;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# Navbar

navbar()



# Página inicial

st.title(
    "Risk Control Dashboard"
)


st.caption(
    "Bem-vindo ao seu sistema de gestão de frotas"
)



st.divider()



# Cards

col1, col2 = st.columns(
    2,
    gap="large"
)



with col1:

    st.subheader(
        "🛡️ Controle de Escoltas"
    )



    if st.button(
        "Acessar Escoltas",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Escolta.py"
        )



with col2:

    st.subheader(
        "✈️ Controle de Viagens"
    )


    if st.button(
        "Acessar Viagens",
        use_container_width=True
    ):

        st.info(
            "Módulo em desenvolvimento."
        )