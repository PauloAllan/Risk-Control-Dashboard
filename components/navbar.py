import streamlit as st


def navbar():

    st.markdown(
        """
        <style>

        .nav-container {
            background-color: #111827;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 25px;
        }


        .stButton button {

            border-radius: 10px;

            height: 40px;

            font-weight: 600;

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(
        [4, 1, 1]
    )


    with col1:

        st.markdown(
            "🚚 **Risk Control Dashboard**"
        )


    with col2:

        if st.button(
            "🏠 Home",
            use_container_width=True
        ):

            st.switch_page(
                "app.py"
            )


    with col3:

        if st.button(
            "🛡 Escoltas",
            use_container_width=True
        ):

            st.switch_page(
                "pages/Escolta.py"
            )


    st.divider()