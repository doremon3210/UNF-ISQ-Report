import requests
import pandas as pd
import os.path
from os import path
#Id to parse into URL
#Accept only simple name
#Right now only the Computing and Math department identified
library_id = {"Computing": 6502, "Math": 6103, "Communication": 6108,               #Department
                "Fall": 80, "Spring": 10, "Summer": 50}                             #Season

#Get the Summary Data and Save it by season_year_department.csv
def download_data(year, season, department):
    #Change the Season string and Department string to Season ID and Department ID
    department_id = library_id[department]
    season_id = library_id[season]
    
    #Give the Year, Season ID, and Department ID to the URL so that we can get the Data 
    url = "https://bannerssb.unf.edu/nfpo-ssb/wkshisq.csv?pv_rpt=ISQ_Dept_Summary_Data&pv_term={}{}&pv_dept={}&pv_pidm=".format(year, season_id, department_id)
    
    r = requests.get(url, allow_redirects=True)
    
    #Save the Data
    file_name = "{}_{}_{}.csv".format(season, year, department)
    open(file_name, 'wb').write(r.content)

#Convert DataFrame to Pivot Table
def convert_data_to_pivot_table(year, season, department, df):
    #Convert DataFrame to Pivot Table
    df2 = pd.pivot_table(df, index = ["COURSE", "COURSE TITLE", "INSTRUCTOR"], values = ["F", 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'ENROLLED', "CLASS GPA", 'My overall rating of instructor'])
    
    #Change the order of the columns
    df2 = df2.reindex(columns = ["F", 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'ENROLLED', "CLASS GPA", 'My overall rating of instructor'])
    
    #Save the Data as Excel File
    export_file_name = "{}_{}_{}_rating.xlsx".format(season, year, department)
    df2.to_excel(export_file_name)


def main():
    #Get the specific Data
    year = input("Enter the Year: ")
    season = input("Enter the Season: ")
    department = input("Enter the Department: ")
    
    #If we're already have the data then skipping downloads
    file_name = "{}_{}_{}.csv".format(season, year, department)
    if not path.exists(file_name):
        #Download and Save the Data
        download_data(year, season, department)
        
    #Get the CSV Data that we just downloaded and Use Pandas to make DataFrame 
    df = pd.read_csv(file_name, skipinitialspace=True)
    
    #Convert Data to Pivot Table and Save it as Excel File
    convert_data_to_pivot_table(year, season, department, df)

if __name__ == "__main__":
    main()
    


                    


# %%
