import streamlit as st
import pandas as pd
import altair as alt
import os

# Caminho para os arquivos processados
output_path = "data/processed/"

# Carregar os arquivos processados
def load_data():
    access_by_type = pd.read_csv(os.path.join(output_path, "access_by_type.csv"), index_col=0)
    access_by_title = pd.read_csv(os.path.join(output_path, "access_by_title.csv"), index_col=0)
    hours_by_title = pd.read_csv(os.path.join(output_path, "hours_by_title.csv"), index_col=0, header=None, names=["Hours"])
    access_by_month = pd.read_csv(os.path.join(output_path, "access_by_month.csv"))
    access_by_day = pd.read_csv(os.path.join(output_path, "access_by_day.csv"), header=0)
    access_by_weekday = pd.read_csv(os.path.join(output_path, "access_by_weekday.csv"), header=0)
    access_by_hour = pd.read_csv(os.path.join(output_path, "access_by_hour.csv"), header=0)
    access_comparison = pd.read_csv(os.path.join(output_path, "access_comparison.csv"))
    return (access_by_type, access_by_title, hours_by_title, access_by_month, 
            access_by_day, access_by_weekday, access_by_hour, access_comparison)

# Função para formatar timedelta em hh:mm:ss
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Carregar os dados
(access_by_type, access_by_title, hours_by_title, access_by_month,
 access_by_day, access_by_weekday, access_by_hour, access_comparison) = load_data()

# Ajustar o formato de horas por título
hours_by_title["Hours"] = pd.to_timedelta(hours_by_title["Hours"], errors="coerce")
access_comparison.set_index("Year", inplace=True)

# Calcular informações gerais
total_hours = hours_by_title["Hours"].sum()
average_hours = hours_by_title["Hours"].mean()
unique_titles = len(access_by_title)

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard de Visualização", layout="wide")

# Barra lateral para navegação
page = st.sidebar.selectbox(
    "Selecione a Página",
    ["Visão Geral", "Detalhamento por Título", "Análise Temporal"]
)

# Página 1: Visão Geral
if page == "Visão Geral":
    st.title("Visão Geral")
    st.metric("Total de Horas Assistidas", format_timedelta(total_hours))
    st.metric("Média de Horas Assistidas", format_timedelta(average_hours))
    st.metric("Quantidade de Títulos Assistidos", unique_titles)

    st.subheader("Total de Acessos por Tipo de Título")
    st.bar_chart(access_by_type)

    st.subheader("Comparação de Acessos por Ano")
    st.bar_chart(access_comparison)

# Página 2: Detalhamento por Título
elif page == "Detalhamento por Título":
    st.title("Detalhamento por Título")
    st.subheader("Total de Acessos por Título")
    st.dataframe(access_by_title)

    st.subheader("Total de Horas Assistidas por Título")
    st.dataframe(hours_by_title)

    st.subheader("Título Específico")
    selected_title = st.selectbox("Escolha um Título", access_by_title.index)
    title_accesses = access_by_title.loc[selected_title].values[0]
    title_hours = pd.to_timedelta(hours_by_title.loc[selected_title].values[0])
    st.write(f"Acessos: {title_accesses}")
    st.write(f"Horas Assistidas: {format_timedelta(title_hours)}")

# Página 3: Análise Temporal
elif page == "Análise Temporal":
    st.title("Análise Temporal")

    # Mapeamento de números para nomes dos meses
    month_names = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    # Ordem correta dos meses
    ordered_months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                      "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    # Acessos por Mês
    if not access_by_month.empty:
        access_by_month["Month_Name"] = access_by_month["Month"].map(month_names)
        access_by_month["Month_Name"] = pd.Categorical(access_by_month["Month_Name"], categories=ordered_months, ordered=True)
        chart = alt.Chart(access_by_month).mark_bar().encode(
            x=alt.X("Month_Name", sort=ordered_months, title="Mês", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Title", title="Acessos")
        ).properties(
            title="Acessos por Mês"
        )
        st.subheader("Acessos por Mês")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para Acessos por Mês.")

    # Acessos por Dia
    if not access_by_day.empty:
        access_by_day["Day"] = access_by_day["Day"].astype(int)
        full_days = pd.DataFrame({"Day": range(1, 32)})
        access_by_day = full_days.merge(access_by_day, on="Day", how="left").fillna(0)
        chart = alt.Chart(access_by_day).mark_bar().encode(
            x=alt.X("Day:O", title="Dia", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Title:Q", title="Acessos")
        ).properties(
            title="Acessos por Dia"
        )
        st.subheader("Acessos por Dia")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para Acessos por Dia.")

    # Acessos por Dia da Semana
    if not access_by_weekday.empty:
        weekday_translation = {
            "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
        }
        ordered_weekdays = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        access_by_weekday["Weekday"] = access_by_weekday["Weekday"].map(weekday_translation)
        access_by_weekday["Weekday"] = pd.Categorical(access_by_weekday["Weekday"], categories=ordered_weekdays, ordered=True)
        chart = alt.Chart(access_by_weekday).mark_bar().encode(
            x=alt.X("Weekday", sort=ordered_weekdays, title="Dia da Semana", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("count", title="Acessos")
        ).properties(
            title="Acessos por Dia da Semana"
        )
        st.subheader("Acessos por Dia da Semana")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para Acessos por Dia da Semana.")

    # Acessos por Hora
    if not access_by_hour.empty:
        if access_by_hour.shape[1] == 2:
            access_by_hour.columns = ["Hour", "Access"]
        else:
            st.error("O arquivo 'access_by_hour.csv' não contém o formato esperado (duas colunas: Hour, Title).")
            st.stop()
        access_by_hour["Hour"] = access_by_hour["Hour"].astype(int)
        access_by_hour = access_by_hour.sort_values("Hour")
        chart = alt.Chart(access_by_hour).mark_bar().encode(
            x=alt.X("Hour:O", title="Hora", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Access:Q", title="Acessos")
        ).properties(
            title="Acessos por Hora"
        )
        st.subheader("Acessos por Hora")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para Acessos por Hora.")