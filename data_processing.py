import pandas as pd
import os

# Caminhos para os arquivos
input_path = "data/raw/"
output_path = "data/processed/"

# Certificar-se de que a pasta de saída existe
os.makedirs(output_path, exist_ok=True)

# Carregar os arquivos
clickstream_data = pd.read_csv(os.path.join(input_path, "Clickstream.csv"))
viewing_activity_data = pd.read_excel(os.path.join(input_path, "ViewingActivity.xlsx"), engine='openpyxl')

# Separar e limpar os dados do arquivo ViewingActivity
viewing_activity_data = viewing_activity_data.iloc[:, 0].str.split(',', expand=True)
expected_columns = [
    "Profile Name", "Start Time", "Duration", "Attributes", "Title",
    "Supplemental Video Type", "Device Type", "Bookmark",
    "Latest Bookmark", "Country"
]
actual_columns = viewing_activity_data.shape[1]
if actual_columns < len(expected_columns):
    expected_columns = expected_columns[:actual_columns]
elif actual_columns > len(expected_columns):
    expected_columns += [f"Extra Column {i}" for i in range(actual_columns - len(expected_columns))]

viewing_activity_data.columns = expected_columns
viewing_activity_data["Start Time"] = pd.to_datetime(viewing_activity_data["Start Time"], errors='coerce')
viewing_activity_data["Duration"] = pd.to_timedelta(viewing_activity_data["Duration"], errors='coerce')
viewing_activity_data_cleaned = viewing_activity_data.dropna(subset=["Start Time", "Duration", "Title"]).copy()

# Adicionar colunas auxiliares para análise por tempo
viewing_activity_data_cleaned.loc[:, "Year"] = viewing_activity_data_cleaned["Start Time"].dt.year
viewing_activity_data_cleaned.loc[:, "Month"] = viewing_activity_data_cleaned["Start Time"].dt.month
viewing_activity_data_cleaned.loc[:, "Day"] = viewing_activity_data_cleaned["Start Time"].dt.day
viewing_activity_data_cleaned.loc[:, "Weekday"] = viewing_activity_data_cleaned["Start Time"].dt.day_name()
viewing_activity_data_cleaned.loc[:, "Hour"] = viewing_activity_data_cleaned["Start Time"].dt.hour

# Calcular as métricas
# 1. Total de horas assistidas
total_duration = viewing_activity_data_cleaned["Duration"].sum()

# 2. Média de horas assistidas
average_duration = viewing_activity_data_cleaned["Duration"].mean()

# 3. Quantidade de títulos assistidos
unique_titles = viewing_activity_data_cleaned["Title"].nunique()

# 4. Total de acessos por tipo de título
viewing_activity_data_cleaned.loc[:, "Type"] = viewing_activity_data_cleaned["Title"].apply(
    lambda x: "Série" if "Temporada" in str(x) else "Filme"
)
access_by_type = viewing_activity_data_cleaned["Type"].value_counts()

# 5. Total de acessos por título
access_by_title = viewing_activity_data_cleaned["Title"].value_counts()

# 6. Total de horas assistidas por título
hours_by_title = viewing_activity_data_cleaned.groupby("Title")["Duration"].sum()

# 7. Quantidade de acessos por mês/dia/semana/hora
access_by_month = viewing_activity_data_cleaned.groupby("Month")["Title"].count()
access_by_day = viewing_activity_data_cleaned.groupby("Day")["Title"].count()
access_by_weekday = viewing_activity_data_cleaned["Weekday"].value_counts()
access_by_hour = viewing_activity_data_cleaned.groupby("Hour")["Title"].count()

# 8. Comparação do total de acessos do ano atual versus anterior
current_year = viewing_activity_data_cleaned["Year"].max()
previous_year = current_year - 1

# Reformatar os dados para o formato Year/Access
access_comparison = pd.DataFrame({
    "Year": [previous_year, current_year],
    "Access": [
        viewing_activity_data_cleaned[viewing_activity_data_cleaned["Year"] == previous_year]["Title"].count(),
        viewing_activity_data_cleaned[viewing_activity_data_cleaned["Year"] == current_year]["Title"].count()
    ]
})

# Salvar os resultados em arquivos CSV
access_by_type.to_csv(os.path.join(output_path, "access_by_type.csv"), index=True, header=True)
access_by_title.to_csv(os.path.join(output_path, "access_by_title.csv"), index=True, header=True)
hours_by_title.to_csv(os.path.join(output_path, "hours_by_title.csv"), index=True, header=True)
access_by_month.to_csv(os.path.join(output_path, "access_by_month.csv"), index=True, header=True)
access_by_day.to_csv(os.path.join(output_path, "access_by_day.csv"), index=True, header=True)
access_by_weekday.to_csv(os.path.join(output_path, "access_by_weekday.csv"), index=True, header=True)
access_by_hour.to_csv(os.path.join(output_path, "access_by_hour.csv"), index=True, header=True)
access_comparison.to_csv(os.path.join(output_path, "access_comparison.csv"), index=False)

print("Dados processados e salvos na pasta 'data/processed/'.")