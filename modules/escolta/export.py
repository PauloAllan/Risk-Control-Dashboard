from io import BytesIO

import pandas as pd



def export_excel(df: pd.DataFrame) -> bytes:
    """
    Converte os registros de escolta
    para arquivo Excel.
    """


    export = df.copy()


    # Renomear colunas para apresentação
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
            "horario_apresentacao": "Horário apresentação",
            "horario_saida": "Horário saída",
        }
    )


    # Formatação da data
    if "Data" in export.columns:

        export["Data"] = (
            pd.to_datetime(export["Data"])
            .dt.strftime("%d/%m/%Y")
        )


    # Remover campos internos
    export = export.drop(
        columns=[
            "id",
            "criado_em"
        ],
        errors="ignore"
    )


    output = BytesIO()


    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:


        export.to_excel(
            writer,
            index=False,
            sheet_name="Escoltas"
        )


        worksheet = writer.sheets["Escoltas"]


        # Congelar primeira linha
        worksheet.freeze_panes = "A2"


        # Ajustar largura das colunas
        for column in worksheet.columns:

            max_length = max(
                len(str(cell.value or ""))
                for cell in column
            )


            column_letter = (
                column[0]
                .column_letter
            )


            worksheet.column_dimensions[
                column_letter
            ].width = min(
                max_length + 2,
                40
            )


    return output.getvalue()