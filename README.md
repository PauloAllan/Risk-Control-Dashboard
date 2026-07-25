<div align="center">

# 🚚 Controle de Escoltas

### Operações sob controle. Decisões à vista.

<p>
  <img src="https://img.shields.io/badge/Python-3.13-111827?style=for-the-badge&logo=python&logoColor=FBBF24" alt="Python 3.13" />
  <img src="https://img.shields.io/badge/Streamlit-1.38%2B-111827?style=for-the-badge&logo=streamlit&logoColor=FF4B4B" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Banco-SQLite-111827?style=for-the-badge&logo=sqlite&logoColor=60A5FA" alt="SQLite" />
</p>

<p>
  Uma aplicação local, rápida e objetiva para registrar, acompanhar e analisar operações de escolta.
</p>

</div>

---

## Visão geral

O **Controle de Escoltas** reúne as informações essenciais de cada operação em um único lugar: veículo, transportadora, valor da carga, destino, A.E., modalidade de escolta e horários.

O resultado é um fluxo simples: **cadastrar → acompanhar → analisar**.

## Recursos

| Módulo | O que entrega |
| :--- | :--- |
| `Cadastro` | Registro completo da operação com validação de A.E. de 8 dígitos. |
| `Registros` | Tabela centralizada, seleção por placa e exportação em Excel. |
| `Edição` | Página dedicada para revisar e atualizar um lançamento. |
| `Exclusão` | Remoção protegida por confirmação. |
| `Dashboard` | Indicadores, volumes por transportadora, destinos e tipo de escolta. |

## Dados registrados

```text
Data · Placa · Transportadora · Valor da carga · Destino
A.E. · Tipo de escolta · Observação · Horário de apresentação · Horário de saída
```

## Início rápido

> Requisito: Python 3.10 ou superior.

```powershell
# 1. Entre na pasta do projeto
cd "C:\Users\paulo\OneDrive\Documentos\Painel de Controle"

# 2. Instale as dependências
python -m pip install -r requirements.txt

# 3. Inicie o painel
python -m streamlit run app.py
```

Abra o endereço exibido no terminal — normalmente [`http://localhost:8501`](http://localhost:8501).

## Como usar

1. Em **Adicionar informações**, cadastre uma nova operação.
2. Em **Registros**, consulte a tabela ou faça o download do Excel.
3. Selecione uma **placa** e escolha **Editar registro** ou **Apagar registro**.
4. Acompanhe os principais indicadores em **Dashboard**.

## Estrutura

```text
.
├── app.py                 # Aplicação Streamlit e regras de negócio
├── requirements.txt       # Dependências do projeto
├── painel_escoltas.db     # Banco local (criado automaticamente)
└── README.md              # Documentação
```

## Privacidade dos dados

Os registros são armazenados localmente em `painel_escoltas.db`. O arquivo é criado na primeira execução e não é enviado para serviços externos pela aplicação.

---

<div align="center">
  <sub>Feito para operações que precisam de clareza, agilidade e controle.</sub>
</div>
