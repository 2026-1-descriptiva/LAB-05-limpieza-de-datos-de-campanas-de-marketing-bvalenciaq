"""
Escriba el codigo que ejecute la accion solicitada.
"""
from pathlib import Path
import pandas as pd

# pylint: disable=import-outside-toplevel
columnas_client = [
    "client_id",
    "age",
    "job",
    "marital",
    "education",
    "credit_default",
    "mortgage",
]

columnas_campaign = [
    "client_id",
    "number_contacts",
    "contact_duration",
    "previous_campaign_contacts",
    "previous_outcome",
    "campaign_outcome",
    "last_contact_date",
]

columnas_economics = [
    "client_id",
    "cons_price_idx",
    "euribor_three_months",
]
ruta = "files/input"

def crear_df(ruta):
    archivos = sorted(Path(ruta).glob("*.csv.zip"))
    df = pd.concat([pd.read_csv(a, index_col=0,) for a in archivos], ignore_index= True)
    return df

def limpieza_df(df):

    df['job'] = df['job'].str.replace('.','',regex = False)
    df['job'] = df['job'].str.replace('-','_',regex = False)

    df['education'] = df['education'].str.replace('.','_',regex = False)
    df['education'] = df['education'].replace('unknown',pd.NA)

    df['credit_default'] = (df['credit_default'] == 'yes').astype(int)

    df['mortgage'] = (df['mortgage'] == 'yes').astype(int)

    df['previous_outcome'] = (df['previous_outcome'] == 'success').astype(int)

    df['campaign_outcome'] = (df['campaign_outcome'] == 'yes').astype(int)

    df['last_contact_date'] = '2022-' + df['month'] + '-' + df['day'].astype('str')
    df['last_contact_date'] =pd.to_datetime(df['last_contact_date'],format="%Y-%b-%d")
    df['last_contact_date'] = df['last_contact_date'].dt.strftime("%Y-%m-%d")

    return df


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    df = crear_df(ruta)
    df_limpio = limpieza_df(df)

    clients = df_limpio[columnas_client]
    campaigns = df_limpio[columnas_campaign]
    economics = df_limpio[columnas_economics]

    clients.to_csv('files/output/client.csv', index=False)
    campaigns.to_csv('files/output/campaign.csv', index=False)
    economics.to_csv('files/output/economics.csv', index=False)


if __name__ == "__main__":
    clean_campaign_data()
