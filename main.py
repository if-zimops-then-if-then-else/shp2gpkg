# This is a short python program that will merge three text files - containing information
# about parcels, owners and a respective key file to join the previous two - into one shapefile
# which will then be transformed into a geopackage.
# Although all the initial files will remain unchanged, I do not recommend using it without
# knowing what it does and I distance myself from every damage or harm this program can cause.
# It has been written for the sole purpose of helping a friend of mine to simplify the aforementioned
# process of joining a csv file into a shapefile/geopackage.
# The usage of this program is as follows:
#
# place the main.py/main.bat file in a folder
# place the following three files in a separate "data" folder:
#     one .PAR file
#     one .SOG file
#     one .TTC file
#     a shapefile
# simply run the main file and a geopackage will be created in the home directory

import csv
import math
import os
import time

import pandas as pd
import geopandas as gpd


def convert_to_csv(file, name):
    with open('data/' + file, 'r') as infile:
        # Open the CSV file for writing
        with open('data/' + name + '_1.csv', 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)
            # Read the file line by line
            for line in infile:
                # Split the line by the delimiter '|'
                fields = line.strip().split('|')
                # Write the fields to the CSV file
                writer.writerow(fields)


def shorten_sog(file):
    with open('data/' + file) as infile:
        reader = csv.reader(infile)
        # Open the CSV file for writing
        with open('data/' + 'SOG_2.csv', 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)
            # Read the file line by line
            for r in reader:
                # Write the fields to the CSV file
                if 10 < len(r):
                    writer.writerow((r[2], r[3], r[4], r[5], r[10]))
                else:
                    writer.writerow((r[2], r[3], r[4], r[5]))


def shorten_par(file):
    with open('data/' + file) as infile:
        reader = csv.reader(infile)
        # Open the CSV file for writing
        with open('data/' + 'PAR_2.csv', 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)
            # Read the file line by line
            for r in reader:
                # Write the fields to the CSV file
                writer.writerow((r[2], r[8], r[9], r[10]))


def shorten_ttc(file):
    with open('data/' + file) as infile:
        reader = csv.reader(infile)
        # Open the CSV file for writing
        with open('data/' + 'TTC_2.csv', 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)
            # Read the file line by line
            for r in reader:
                # Write the fields to the CSV file
                writer.writerow((r[2], r[4]))


def rem_duplicate_par(file):
    with open('data/' + file) as infile:
        reader = csv.reader(infile)
        # Open the CSV file for writing
        with open('data/' + 'PAR_3.csv', 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)
            # Read the file line by line
            known_ids = set()
            for r in reader:
                if r[0] not in known_ids:
                    known_ids.add(r[0])
                    writer.writerow(r)


def rem_duplicate_ttc(file):
    with open('data/' + file) as infile:
        reader = csv.reader(infile)
        # Open the CSV file for writing
        with open('data/' + 'TTC_3.csv', 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)
            # Read the file line by line
            known_par_ids = set()
            known_sog_ids = None
            # Iterate through every line, if it's a new PAR, add its ID to known ID's and create a new Owner set
            for r in reader:
                if r[1] not in known_par_ids:
                    known_sog_ids = set()
                    known_par_ids.add(r[1])
                    known_sog_ids.add(r[0])
                    writer.writerow(r)
                # If it's not new, add the corresponding Owner to known Owners
                elif r[0] not in known_sog_ids:
                    known_sog_ids.add(r[0])
                    writer.writerow(r)


def parse_tipo(file):
    with open('data/' + file) as infile:
        reader = csv.reader(infile)
        # Open the CSV file for writing
        with open('data/' + 'SOG_3.csv', 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)
            # Read the file line by line
            for r in reader:
                # Write the fields to the CSV file, create a TIPO for each owner based on the text string
                if r[1] == 'P':
                    r[1] = 'PRIVATI'
                    writer.writerow(r)
                elif r[1] == 'G':
                    if 'comune' in r[2].lower() or 'gemeinde' in r[3].lower() or 'comune' in r[
                            3].lower() or 'gemeinde' in r[2].lower():
                        r[1] = 'COMUNE'
                        writer.writerow(r)
                    elif 'alperia' in r[2].lower() or 'alperia' in r[3].lower():
                        r[1] = 'SOC. PUBBLICA'
                        writer.writerow(r)
                    elif 'konsortium' in r[2].lower() or 'konsortium' in r[3].lower() or 'consorzio' in r[
                            3].lower() or 'consorzio' in r[2].lower():
                        r[1] = 'SOC. PUBBLICA'
                        writer.writerow(r)
                    elif 'genossenschaft' in r[2].lower() or 'genossenschaft' in r[
                            3].lower() or 'società cooperativa' in r[3].lower() or 'società cooperativa' \
                            in r[2].lower():
                        r[1] = 'SOC. PUBBLICA'
                        writer.writerow(r)
                    elif 'öffentliches gut' in r[2].lower() or 'öffentliches gut' in r[
                            3].lower() or 'demanio pubblico' in r[3].lower() or 'demanio pubblico' in r[2].lower():
                        if 'acque' in r[2].lower() or 'aqcue' in r[3].lower() or 'gewässer' in r[3].lower() \
                                or 'gewässer' in r[2].lower():
                            r[1] = 'PAB AQCUE'
                            writer.writerow(r)
                        elif 'ferrovie' in r[2].lower() or 'ferrovie' in r[3].lower() or 'eisenbahn' in r[
                                3].lower() or 'eisenbahn' in r[2].lower():
                            r[1] = 'PAB FERROVIE'
                            writer.writerow(r)
                        elif 'foreste' in r[2].lower() or 'foreste' in r[3].lower() or 'forste' in r[
                                3].lower() or 'forste' in r[2].lower():
                            r[1] = 'PAB FORESTE'
                            writer.writerow(r)
                        elif 'militare' in r[2].lower() or 'militare' in r[3].lower() or 'militär' in r[
                                3].lower() or 'militär' in r[2].lower():
                            r[1] = 'PAB MILITARE'
                            writer.writerow(r)
                        elif 'patrimonio' in r[2].lower() or 'patrimonio' in r[3].lower() or 'erbe' in r[
                                3].lower() or 'erbe' in r[2].lower():
                            r[1] = 'PAB PATRIMONIO'
                            writer.writerow(r)
                        elif 'bonifica' in r[2].lower() or 'bonifica' in r[3].lower() or 'entwässerung' in r[
                                3].lower() or 'entwässerung' in r[2].lower():
                            r[1] = 'PAB BONIFICA'
                            writer.writerow(r)
                        elif 'strade' in r[2].lower() or 'straße' in r[3].lower() or 'strade' in r[
                                3].lower() or 'straße' in r[2].lower():
                            r[1] = 'PAB STRADE'
                            writer.writerow(r)
                        elif 'ipes' in r[2].lower() or 'ipes' in r[3].lower() or 'wohnbauinstitut' in r[
                            3].lower() or 'wohnbauinstitut' in \
                                r[2].lower():
                            r[1] = 'PAB IPES'
                            writer.writerow(r)
                        else:
                            r[1] = 'PAB'
                            writer.writerow(r)
                    elif 'acque' in r[2].lower() or 'aqcue' in r[3].lower() or 'gewässer' in r[
                        3].lower() or 'gewässer' in \
                            r[2].lower():
                        r[1] = 'PAB AQCUE'
                        writer.writerow(r)
                    elif 'ferrovie' in r[2].lower() or 'ferrovie' in r[3].lower() or 'eisenbahn' in r[
                            3].lower() or 'eisenbahn' in r[2].lower():
                        r[1] = 'PAB FERROVIE'
                        writer.writerow(r)
                    elif 'foreste' in r[2].lower() or 'foreste' in r[3].lower() or 'forste' in r[
                            3].lower() or 'forste' in r[2].lower():
                        r[1] = 'PAB FORESTE'
                        writer.writerow(r)
                    elif 'militare' in r[2].lower() or 'militare' in r[3].lower() or 'militär' in r[
                            3].lower() or 'militär' in r[2].lower():
                        r[1] = 'PAB MILITARE'
                        writer.writerow(r)
                    elif 'patrimonio' in r[2].lower() or 'patrimonio' in r[3].lower() or 'erbe' in r[
                            3].lower() or 'erbe' in r[2].lower():
                        r[1] = 'PAB PATRIMONIO'
                        writer.writerow(r)
                    elif 'bonifica' in r[2].lower() or 'bonifica' in r[3].lower() or 'entwässerung' in r[
                            3].lower() or 'entwässerung' in r[2].lower():
                        r[1] = 'PAB BONIFICA'
                        writer.writerow(r)
                    elif 'strade' in r[2].lower() or 'straße' in r[3].lower() or 'strade' in r[3].lower() \
                            or 'straße' in r[2].lower():
                        r[1] = 'PAB STRADE'
                        writer.writerow(r)
                    elif 'ipes' in r[2].lower() or 'ipes' in r[3].lower() or 'wohnbauinstitut' in r[
                        3].lower() or 'wohnbauinstitut' in \
                            r[2].lower():
                        r[1] = 'PAB IPES'
                        writer.writerow(r)
                    elif 'rete ferroviaria italiana' in r[2].lower() or 'rete ferroviaria italiana' in r[3].lower():
                        r[1] = 'RFI'
                        writer.writerow(r)
                    else:
                        r[1] = 'SOC. PRIVATA'
                        writer.writerow(r)
                else:
                    r[1] = 'M'
                    writer.writerow(r)


def merge_files():
    header1 = ['par_id', 'pre', 'after', 'dot']
    header2 = ['sog_id', 'TIPO', 'surname', 'name', 'id-code']
    header3 = ['sog_id', 'par_id']

    par = pd.read_csv('data/PAR_3.csv', header=None)
    par.columns = header1
    sog = pd.read_csv('data/SOG_3.csv', header=None)
    sog.columns = header2
    ttc = pd.read_csv('data/TTC_3.csv', header=None)
    ttc.columns = header3

    sog_ttc = pd.merge(sog, ttc, on='sog_id')

    par_ttc = pd.merge(par, ttc, on='par_id')

    merged = pd.merge(par_ttc, sog_ttc, on=['par_id', 'sog_id'])
    merged = merged.drop('par_id', axis=1)
    merged = merged.drop('sog_id', axis=1)
    merged.to_csv('data/merged_files.csv', index=False)


def parse_fields(row):
    # parse the coded ID into the PT_CODE
    if row['dot'] == 'E':
        if math.isnan(row['after']):
            return '.' + str(int(row['pre']))
        else:
            return '.' + str(int(row['pre'])) + '/' + str(int(row['after']))
    else:
        if math.isnan(row['after']):
            return str(int(row['pre']))
        else:
            return str(int(row['pre'])) + '/' + str(int(row['after']))


def parse_id(file):
    # parse the coded ID into the PT_CODE
    df = pd.read_csv('data/' + file)
    df['Concatenated'] = df.apply(parse_fields, axis=1)
    # then drop the 3 now unused columns
    df = df.drop('pre', axis=1)
    df = df.drop('after', axis=1)
    df = df.drop('dot', axis=1)
    # set a new header
    header = ['TIPO', 'surname', 'name', 'id-code', 'PT_CODE']
    df.columns = header
    # sort the new csv file by PT_CODE ascending
    df.sort_values('PT_CODE', axis=0, ascending=True, inplace=True, na_position='first')
    # then write it back as a new csv file
    df.to_csv('data/parsed_ids.csv', index=False)


def concat_fields(file):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv('data/' + file)
    # Concatenate three fields into one string using the apply function
    df['joined'] = df.apply(
        lambda row: ', '.join(
            [str(val) for val in [row['surname'], row['name'], row['id-code']] if not pd.isnull(val)]), axis=1)
    df = df.drop('surname', axis=1)
    df = df.drop('name', axis=1)
    df = df.drop('id-code', axis=1)
    # Write the modified DataFrame to a new CSV file
    df.to_csv('data/concat.csv', index=False)


def custom_agg(df):
    merged_owner = '\n '.join(df['joined'])
    num_owners = merged_owner.count('\n') + 1
    property_type = df['TIPO'].unique()
    if len(property_type) == 1:
        merged_type = property_type[0]
    else:
        merged_type = 'MISTA'
    return pd.Series({'NUM_PROP': num_owners, 'PROP': merged_owner, 'TIPO': merged_type})


def join_ids(file):
    df = pd.read_csv('data/' + file)
    # Group the rows by ID and concatenate the strings
    grouped_df = df.groupby('PT_CODE').apply(custom_agg).reset_index()
    # Write the modified DataFrame to a new CSV file
    header = ['PT_CODE', 'NUM_PROP', 'PROP', 'TIPO']
    grouped_df.columns = header
    grouped_df.to_csv('data/' + 'final.csv', index=False)


def merge_shapefile(file, num):
    shapefile = gpd.read_file('data/' + file)
    csvfile = pd.read_csv('data/final.csv')

    shapefile.to_file('data/geopackage.gpkg', layer='layer_name', driver='GPKG', index=False)

    gpkg = gpd.read_file('data/geopackage.gpkg', layer='layer_name')

    joined = gpkg.merge(csvfile, on='PT_CODE')

    joined = joined.rename(columns={'joined': 'PROP'})

    joined.to_file(num + '_geopackage.gpkg', driver='GPKG', index=False)

    os.remove('data/final.csv')
    os.remove('data/geopackage.gpkg')


def main():
    print("STARTING")
    time.sleep(1)
    par_file, sog_file, ttc_file, shp_file = None, None, None, None
    for f in os.listdir('data/'):
        if f.endswith('.PAR'):
            print(f)
            par_file = f
        elif f.endswith('.SOG'):
            print(f)
            sog_file = f
        elif f.endswith('.TTC'):
            print(f)
            ttc_file = f
        elif f.endswith('.shp'):
            print(f)
            shp_file = f

    num = par_file.split('_')[0]
    print(num)
    # convert PAR SOG and TTC to csv files
    convert_to_csv(par_file, 'PAR')
    convert_to_csv(sog_file, 'SOG')
    convert_to_csv(ttc_file, 'TTC')
    # cut out unused columns
    shorten_par('PAR_1.csv')
    os.remove('data/PAR_1.csv')
    shorten_sog('SOG_1.csv')
    os.remove('data/SOG_1.csv')
    shorten_ttc('TTC_1.csv')
    os.remove('data/TTC_1.csv')
    # remove duplicate parcels and duplicate keys
    rem_duplicate_par('PAR_2.csv')
    os.remove('data/PAR_2.csv')
    rem_duplicate_ttc('TTC_2.csv')
    os.remove('data/TTC_2.csv')
    # add the TIPO to the SOG file
    parse_tipo('SOG_2.csv')
    os.remove('data/SOG_2.csv')
    # merge all three files together
    merge_files()
    os.remove('data/PAR_3.csv')
    os.remove('data/SOG_3.csv')
    os.remove('data/TTC_3.csv')
    # parse the coded ID into PT_CODE
    parse_id('merged_files.csv')
    os.remove('data/merged_files.csv')
    # concatenate the surname, name and id-code for each owner
    concat_fields('parsed_ids.csv')
    os.remove('data/parsed_ids.csv')
    # join multiple owners of one parcel together
    join_ids('concat.csv')
    os.remove('data/concat.csv')
    # merge the final csv file into the given shapefile and transform that into a geopackage
    merge_shapefile(shp_file, num)
    print("SUCCESS")
    time.sleep(3)
    exit(0)


if __name__ == '__main__':
    main()

# copyright: Simon Schnabl