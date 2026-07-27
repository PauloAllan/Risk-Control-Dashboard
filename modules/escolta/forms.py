import streamlit as st

from datetime import date, time

from modules.escolta.crud import (
    insert_record,
    update_record
)



def validate_fields(
    plate,
    carrier,
    destination,
    ae
):

    errors = []


    if not plate:
        errors.append("Informe a placa.")


    if not carrier:
        errors.append("Informe a transportadora.")


    if not destination:
        errors.append("Informe o destino.")


    if not (ae.isdigit() and len(ae) == 8):
        errors.append(
            "A.E. deve conter exatamente 8 números."
        )


    return errors



def form_page():

    """
    Cadastro de uma nova escolta.
    """

    st.title("📝 Adicionar informações")


    st.caption(
        "Preencha os dados da operação."
    )


    with st.form(
        "cadastro_escolta",
        clear_on_submit=True
    ):


        col1, col2 = st.columns(2)


        with col1:

            operation_date = st.date_input(
                "Data",
                value=date.today(),
                format="DD/MM/YYYY"
            )


            plate = st.text_input(
                "Placa",
                placeholder="ABC1D23"
            ).upper().strip()


            carrier = st.text_input(
                "Transportadora"
            ).strip()


            cargo_value = st.number_input(
                "Valor da carga (R$)",
                min_value=0.0,
                step=100.0,
                format="%.2f"
            )


            destination = st.text_input(
                "Destino"
            ).strip()



        with col2:

            ae = st.text_input(
                "A.E.",
                max_chars=8,
                placeholder="00000000"
            ).strip()


            escort_type = st.radio(
                "Tipo de escolta",
                [
                    "Individual",
                    "Comboio"
                ],
                horizontal=True
            )


            presentation = st.time_input(
                "Horário apresentação",
                value=time(8,0)
            )


            departure = st.time_input(
                "Horário saída",
                value=time(9,0)
            )


            observation = st.text_area(
                "Observação",
                height=100
            ).strip()



        submit = st.form_submit_button(
            "Salvar registro",
            type="primary",
            use_container_width=True
        )



    if submit:


        errors = validate_fields(
            plate,
            carrier,
            destination,
            ae
        )


        if errors:

            st.error(
                " ".join(errors)
            )


        else:


            insert_record(
                (
                    operation_date.isoformat(),
                    plate,
                    carrier,
                    cargo_value,
                    destination,
                    ae,
                    escort_type,
                    observation,
                    presentation.strftime("%H:%M"),
                    departure.strftime("%H:%M")
                )
            )


            st.success(
                "Registro salvo com sucesso."
            )



def edit_page(record):

    """
    Edição de uma escolta existente.
    """


    st.title("✏️ Editar registro")


    with st.form(
        "editar_escolta"
    ):


        col1, col2 = st.columns(2)


        with col1:


            operation_date = st.date_input(
                "Data",
                value=record["data"].date()
            )


            plate = st.text_input(
                "Placa",
                value=record["placa"]
            ).upper().strip()


            carrier = st.text_input(
                "Transportadora",
                value=record["transportadora"]
            )


            cargo_value = st.number_input(
                "Valor da carga (R$)",
                value=float(record["valor_carga"])
            )


            destination = st.text_input(
                "Destino",
                value=record["destino"]
            )



        with col2:


            ae = st.text_input(
                "A.E.",
                value=str(record["ae"]),
                max_chars=8
            )


            escort_type = st.radio(
                "Tipo de escolta",
                [
                    "Individual",
                    "Comboio"
                ],
                index=0 if record["tipo_escolta"] == "Individual" else 1
            )


            presentation = st.time_input(
                "Apresentação",
                value=time.fromisoformat(
                    record["horario_apresentacao"]
                )
            )


            departure = st.time_input(
                "Saída",
                value=time.fromisoformat(
                    record["horario_saida"]
                )
            )


            observation = st.text_area(
                "Observação",
                value=record["observacao"] or ""
            )



        save = st.form_submit_button(
            "Salvar alterações",
            type="primary"
        )



    if save:


        errors = validate_fields(
            plate,
            carrier,
            destination,
            ae
        )


        if errors:

            st.error(
                " ".join(errors)
            )


        else:

            update_record(
                record["id"],
                (
                    operation_date.isoformat(),
                    plate,
                    carrier,
                    cargo_value,
                    destination,
                    ae,
                    escort_type,
                    observation,
                    presentation.strftime("%H:%M"),
                    departure.strftime("%H:%M")
                )
            )


            st.success(
                "Registro atualizado."
            )