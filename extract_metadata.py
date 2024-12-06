from itertools import chain
import itertools
import math
import os
import re
import pandas as pd
import requests
import sys

import get_input

def fetch_metadata(doi):
    """Fetch metadata for a given DOI from CrossRef API."""
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        metadata = response.json()
        return metadata
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata for DOI {doi}: {e}")
        return None

def extract_title(metadata):
    try:
        if 'title' in metadata['message'] and len(metadata['message']['title']) > 0:
            return metadata['message']['title'][0]
        else:
            return "No title available"
    except KeyError:
        return "No title found"
    
def extract_authors(metadata):
    try:
        if 'author' in metadata['message'] and len(metadata['message']['author']) > 0:
            authors = [
                f"{author.get('given', '')} {author.get('family', '')}".strip()
                for author in metadata['message']['author']
            ]
            return authors
        else:
            return ["No authors available"]
    except KeyError:
        return ["No authors found"]
    
def extract_year(metadata):
    try:
        if 'published-print' in metadata['message'] and len(metadata['message']['published-print']['date-parts'][0]) > 0:
            return metadata['message']['published-print']['date-parts'][0][0]
        else:
            return "No year available"
    except KeyError:
        return "No year found"
    
def extract_abstract(metadata):
    try:
        if 'abstract' in metadata['message'] and len(metadata['message']['abstract']) > 0:
            return metadata['message']['abstract']
        else:
            return "No abstract available"
    except KeyError:
        return "No abstract found"
   
def extract_full_text_url(metadata):
    """Extract the full-text URL if available from CrossRef metadata."""
    try:
        if 'URL' in metadata['message']:
            return metadata['message']['URL']
        else:
            return "Full text URL not available"
    except KeyError:
        return "Full text URL not available"


def process_keywords(csv_file):
    try:
        data = pd.read_csv(csv_file, sep=",", on_bad_lines='skip')
    except FileNotFoundError:
        print(f"File {csv_file} not found!")
        sys.exit(1)
    
    if 'Country' not in data.columns:
        print("The CSV file must contain a 'Country' column.")
        sys.exit(1)
        
    if 'Adjective' not in data.columns:
        print("The CSV file must contain a 'Country' column.")
        sys.exit(1)
        
    if 'Area' not in data.columns:
        print("The CSV file must contain a 'Adjective' column.")
        sys.exit(1)
        
    mountains = {
            'Africa': [x for x in data['Africa'] if not (isinstance(x, float) and math.isnan(x))],
            'Asia': [x for x in data['Asia'] if not (isinstance(x, float) and math.isnan(x))],
            'Canada': [x for x in data['Canada'] if not (isinstance(x, float) and math.isnan(x))],
            'Europe': [x for x in data['Europe'] if not (isinstance(x, float) and math.isnan(x))],
            'Greenland': [x for x in data['Greenland'] if not (isinstance(x, float) and math.isnan(x))],
            'United States': [x for x in data['United States'] if not (isinstance(x, float) and math.isnan(x))],
            'Central America': [x for x in data['Central America'] if not (isinstance(x, float) and math.isnan(x))],
            'Mexico': [x for x in data['Mexico'] if not (isinstance(x, float) and math.isnan(x))],
            'Caribbean': [x for x in data['Caribbean'] if not (isinstance(x, float) and math.isnan(x))],
            'South America': [x for x in data['South America'] if not (isinstance(x, float) and math.isnan(x))],
            'Oceania': [x for x in data['Oceania'] if not (isinstance(x, float) and math.isnan(x))],
            'Antarctica':[x for x in data['Antarctica'] if not (isinstance(x, float) and math.isnan(x))],
        }
    
    countries = {
        'country': [x for x in data['Country'] if not (isinstance(x, float) and math.isnan(x))],
        'adjective': [x for x in data['Adjective'] if not (isinstance(x, float) and math.isnan(x))]
    }
    
    all_mountains = list(chain.from_iterable(mountains.values()))
    all_countries = list(chain.from_iterable(countries.values()))
    
    return {
        'countries': all_countries,
        'area': [x for x in data['Area'] if not (isinstance(x, float) and math.isnan(x))],
        'mountains': mountains,
        'all_mountains': all_mountains
    }
    
def convert_lists_to_string(df):
    for column in df.columns:
        df[column] = df[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    return df
       

def process_dois(csv_file, output_file, area_keywords, row_number_start=None, row_number_end=None):
    """
    Read DOIs from a CSV, fetch metadata, and save results to another CSV.
    Optionally process only specific rows based on their numbers.
    
    Args:
        csv_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        area_keywords (dict): Keywords for area, countries, and mountain ranges.
        row_numbers_start (str, optional): Start of row numbers to process.
        row_numbers_end (str, optional): End of row numbers to process.
    """
    try:
        data = pd.read_csv(csv_file, sep=";", on_bad_lines='skip')
    except FileNotFoundError:
        print(f"File {csv_file} not found!")
        sys.exit(1)
    
    if 'DOI' not in data.columns:
        print("The CSV file must contain a 'DOI' column.")
        sys.exit(1)
              
    if row_number_end == "0":
        row_number_end = data.shape[0]
        
        
    try:
        row_number_start = int(row_number_start)
        row_number_end = int(row_number_end)
    except ValueError:
        print("Please enter valid integers for the row numbers.")
        sys.exit(1)
    
    row_numbers =  list(range(row_number_start, row_number_end))  
    print(f"Row numbers to process: {row_numbers}")
    if row_numbers:
        try:
            data = data.iloc[row_numbers]
        except IndexError:
            print("Some row numbers are out of range!")
            sys.exit(1)
    
    results = []
    for doi in data['DOI']:
        print(f"Processing DOI: {doi}")
        metadata = fetch_metadata(doi)
        if metadata:
            title = extract_title(metadata)
            url = extract_full_text_url(metadata)
            authors = extract_authors(metadata)
            year = extract_year(metadata)
    
            chapter_study = get_input.get_chapter_from_url(url, 'Study')
            chapter_keywords = get_input.get_chapter_from_url(url, 'Keywords')
            abstract = extract_abstract(metadata)
    
            species = [
                get_input.extract_italicized_text(abstract), 
                get_input.extract_italicized_text(title),
                get_input.extract_italicized_text(chapter_keywords)
                ]
            flattened_species = list(itertools.chain(*species))
    
            area = [
                get_input.search_keywords_in_text(abstract, area_keywords['area']),
                get_input.search_keywords_in_text(title, area_keywords['area']),
                get_input.search_keywords_in_text(chapter_keywords, area_keywords['area'])
                ]
            flattened_area = list(itertools.chain(*area))
    
            country = [
                get_input.search_keywords_in_text(abstract, area_keywords['countries']),
                get_input.search_keywords_in_text(chapter_study, area_keywords['countries']),
                get_input.search_keywords_in_text(chapter_keywords, area_keywords['countries'])
                ]
            flattened_country = list(itertools.chain(*country))
    
            mountainRange = [
                get_input.search_keywords_in_text(abstract, area_keywords['all_mountains']),
                get_input.search_keywords_in_text(chapter_study, area_keywords['all_mountains']),
                get_input.search_keywords_in_text(chapter_keywords, area_keywords['all_mountains'])
                ]
            flattened_mountainRange = list(itertools.chain(*mountainRange))

            results.append({
                'DOI': doi,
                'Title': title,
                'Year': year,
                'Authors': authors,
                'URL': url,
                'Keywords': chapter_keywords,
                'Species': list(set(flattened_species)),
                'Area': list(set(flattened_area)),
                'Country': list(set(flattened_country)),
                'Mountain Range': list(set(flattened_mountainRange))        
                })
        else:
            results.append({
                'DOI': doi,
                'Title': "Error fetching metadata",
                'Year': "",
                'Authors': "",
                'URL': "",
                'Keywords': "",
                'species': "",
                'Area': "",
                'Country': "",
                'Mountain Range': ""
            })
    
    output_df = pd.DataFrame(results)
    output_df = convert_lists_to_string(output_df)
    if os.path.exists(output_file):
        
        output_df.to_csv(output_file, mode='a', index=False, header=False)
        print(f"Appended results to {output_file}")
    else:
        output_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")


