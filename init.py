import pandas as pd
import mysql.connector
from config import MyCONFIG

config = MyCONFIG()


file_path = 'Billionaires Statistics Dataset.csv'
data = pd.read_csv(file_path)


data = data.where(pd.notnull(data), "None")


conn = mysql.connector.connect(
    host=config.get_host(),
    user=config.get_username(),
    password=config.get_pwd(),
    database='BILLIONAIRES'
)
cursor = conn.cursor()


for index, row in data.iterrows():
    cursor.execute('''
        INSERT IGNORE INTO Billionaire (personName, age, gender, `rank`, finalWorth, source, country, city,
                                        countryOfCitizenship, organization, selfMade, status, birthDate,
                                        lastName, firstName, title, date, state, residenceStateRegion, birthYear,
                                        birthMonth, birthDay)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        row['personName'], row['age'], row['gender'], row['rank'], row['finalWorth'], row['source'],
        row['country'], row['city'], row['countryOfCitizenship'], row['organization'], row['selfMade'],
        row['status'], row['birthDate'], row['lastName'], row['firstName'], row['title'], row['date'],
        row['state'], row['residenceStateRegion'], row['birthYear'], row['birthMonth'], row['birthDay']
    ))


    industries = row['industries'].split(', ') if row['industries'] else []

    for industry in industries:
        cursor.execute('''
            INSERT IGNORE INTO Industry (industryName, category)
            VALUES (%s, %s)
        ''', (industry, row['category']))

        cursor.execute('''
            INSERT IGNORE INTO BillionaireIndustry (personName, industryId)
            VALUES (%s, (SELECT industryId FROM Industry WHERE industryName = %s))
        ''', (row['personName'], industry))

    cursor.execute('''
        INSERT IGNORE INTO Country (country, cpi_country, cpi_change_country, gdp_country, 
                                   gross_tertiary_education_enrollment, gross_primary_education_enrollment_country,
                                   life_expectancy_country, tax_revenue_country_country, total_tax_rate_country,
                                   population_country, latitude_country, longitude_country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        row['country'], row['cpi_country'], row['cpi_change_country'], row['gdp_country'],
        row['gross_tertiary_education_enrollment'], row['gross_primary_education_enrollment_country'],
        row['life_expectancy_country'], row['tax_revenue_country_country'],
        row['total_tax_rate_country'], row['population_country'], row['latitude_country'],
        row['longitude_country']
    ))


conn.commit()
conn.close()
