import hashlib
import requests
from tqdm import tqdm

# Hardcoded ORCID ID
ORCID_ID = '0000-0002-9111-0699'

def infer_preprint_server(doi_url):
    if 'doi.org/10.31234' in doi_url:
        return 'OSF'
    if 'doi.org/10.1101' in doi_url:
        return 'bioRxiv'
    if 'doi.org/10.31730' in doi_url:
        return 'PsyArXiv'
    if 'doi.org/10.55458' in doi_url:
        return 'Neurolibre'
    # Add more DOI prefixes as needed
    return 'Unknown'

def infer_proceedings_venue(doi_url):
    if 'doi.org/10.1145' in doi_url:
        return 'ACM Digital Library'
    # Add more DOI prefixes as needed
    return ''

def extract_first_author(detailed_work):
    if detailed_work and 'contributors' in detailed_work:
        contributors = detailed_work['contributors'].get('contributor', [])
        for contributor in contributors:
            if 'contributor-attributes' in contributor and contributor['contributor-attributes'] and contributor['contributor-attributes'].get('contributor-sequence') == 'first':
                if 'credit-name' in contributor and contributor['credit-name']:
                    return contributor['credit-name']['value'].split()[-1]
        if contributors:
            first_contributor = contributors[0]
            if 'credit-name' in first_contributor and first_contributor['credit-name']:
                return first_contributor['credit-name']['value'].split()[-1]
    return 'unknown'

def sanitize_key(key):
    return key.replace(' ', '_').replace(',', '').replace(':', '').replace('.', '').replace('-', '_')

def generate_unique_id(work, detailed_work, entry_type):
    try:
        title = work['title']['title']['value']
        year = work.get('publication-date', {}).get('year', {}).get('value', '')
        first_author = extract_first_author(detailed_work)

        if entry_type == 'unpublished':
            venue = 'preprint'
        else:
            venue = work.get('journal-title', {}).get('value', 'misc') if work.get('journal-title') else 'misc'

        title_hash = hashlib.md5(title.encode('utf-8')).hexdigest()[:8]
        raw_key = f"{first_author}-{venue}-{year}-{title_hash}"
        return sanitize_key(raw_key)
    except Exception as e:
        print(f"Error generating unique ID: {e}")
        return 'unknown_id'

def construct_bibtex_entry(work, detailed_work):
    try:
        entry_type_map = {
            'journal-article': 'article',
            'book-chapter': 'incollection',
            'conference-paper': 'inproceedings',
            'preprint': 'unpublished',
            # Add more mappings as needed
        }

        entry_type = entry_type_map.get(work.get('type', 'misc'), 'misc')
        unique_id = generate_unique_id(work, detailed_work, entry_type)
        title = work['title']['title']['value']
        journal = work.get('journal-title', {}).get('value', '') if work.get('journal-title') else ''
        year = work.get('publication-date', {}).get('year', {}).get('value', '') if work.get('publication-date') else ''
        url = work.get('url', {}).get('value', '') if work.get('url') else ''
        authors = []
        if detailed_work and 'contributors' in detailed_work:
            for contributor in detailed_work['contributors'].get('contributor', []):
                if 'credit-name' in contributor and contributor['credit-name']:
                    authors.append(contributor['credit-name']['value'])
                elif 'contributor-orcid' in contributor and contributor['contributor-orcid']:
                    authors.append(contributor['contributor-orcid']['path'])

        # Retrieve preprint server or proceedings venue
        note = ''
        booktitle = ''
        if entry_type == 'unpublished' and url:
            preprint_server = infer_preprint_server(url)
            note = f"{preprint_server} preprint"
        elif entry_type == 'inproceedings':
            booktitle = work.get('journal-title', {}).get('value', '')
            if not booktitle:
                booktitle = infer_proceedings_venue(url)
                if booktitle == 'ACM Digital Library':
                    booktitle = 'Proceedings of the ACM Digital Library'

        bibtex_entry = f"@{entry_type}{{{unique_id},\n"
        bibtex_entry += f"  title = {{{title}}},\n"
        if journal:
            bibtex_entry += f"  journal = {{{journal}}},\n"
        if note:
            bibtex_entry += f"  note = {{{note}}},\n"
        if booktitle:
            bibtex_entry += f"  booktitle = {{{booktitle}}},\n"
        if year:
            bibtex_entry += f"  year = {{{year}}},\n"
        if url:
            bibtex_entry += f"  url = {{{url}}},\n"
        if authors:
            author_list = ' and '.join(authors)
            bibtex_entry += f"  author = {{{author_list}}},\n"
        bibtex_entry += "}\n"
        return bibtex_entry
    except Exception as e:
        print(f"Error constructing BibTeX entry: {e}")
        return ''

def fetch_detailed_work(orcid_id, put_code):
    try:
        url = f'https://pub.orcid.org/v3.0/{orcid_id}/work/{put_code}'
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to retrieve detailed work. HTTP Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching detailed work: {e}")
        return None

def fetch_orcid_works(orcid_id):
    url = f'https://pub.orcid.org/v3.0/{orcid_id}/works'
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        works = response.json()['group']
        bib_entries = {
            'article': [],
            'unpublished': [],
            'incollection': [],
            'inproceedings': [],
            'misc': []
        }
        ignored_entries = []
        entry_type_map = {
            'journal-article': 'article',
            'book-chapter': 'incollection',
            'conference-paper': 'inproceedings',
            'preprint': 'unpublished',
            # Add more mappings as needed
        }
        for work_group in tqdm(works, desc="Fetching works", unit="work"):
            work_summary = work_group['work-summary'][0]
            try:
                detailed_work = fetch_detailed_work(orcid_id, work_summary['put-code'])
                if detailed_work:
                    bibtex_entry = construct_bibtex_entry(work_summary, detailed_work)
                    if bibtex_entry:
                        entry_type = work_summary.get('type', 'misc')
                        entry_type_key = entry_type_map.get(entry_type, 'misc')
                        bib_entries[entry_type_key].append(bibtex_entry)
                    else:
                        ignored_entries.append((work_summary, 'BibTeX entry construction failed'))
                else:
                    ignored_entries.append((work_summary, 'Detailed work fetch failed'))
            except Exception as e:
                print(f"Error: {e}")
                ignored_entries.append((work_summary, str(e)))
        return bib_entries, ignored_entries
    else:
        raise Exception(f"Failed to retrieve works. HTTP Status code: {response.status_code}")

def save_bibtex_files(bib_entries):
    for entry_type, entries in bib_entries.items():
        with open(f'orcid_works_{entry_type}.bib', 'w') as bib_file:
            bib_file.write('\n\n'.join(entries))

def main():
    orcid_id = ORCID_ID
    bib_entries, ignored_entries = fetch_orcid_works(orcid_id)
    save_bibtex_files(bib_entries)
    print("BibTeX files updated successfully.")

    if ignored_entries:
        print("\nWarning: Some entries were ignored due to errors.")
        for entry, error in ignored_entries:
            print(f"\nEntry: {entry}")
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
