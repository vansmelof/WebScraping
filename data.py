import tabula
import pandas as pd
import zipfile
import re
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


PDF_PATH = r'C:\Users\vanes\Documents\Teste\PIII A - Web Scraping'
CSV_OUT = 'tables.csv'
PAGES = '3-180'
ZIP_PATH = f'Teste_Vanessa_Melo.zip'

def get_table(pdf_path):
    df = tabula.read_pdf(pdf_path, pages = PAGES)
    return df

def save_csv(pdf_path, csv_output):
    df = tabula.convert_into(pdf_path, csv_output , 'csv', pages = PAGES)
    print(f'Saved: {csv_output}.')
    return df

def main():
    pdf_data = get_table(PDF_PATH)

    if pdf_data is not None:
        df = pd.DataFrame(pdf_data)
        save_csv(df, CSV_OUT)

        with zipfile.ZipFile(ZIP_PATH, 'w') as zip_file:
            zip_file.write(CSV_OUT)
        print(f'Compressed file: {ZIP_PATH}.')
    else:
        print('Error compressing.')

if __name__ == '__main__':
 main()

