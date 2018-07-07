import csv
import subprocess

if __name__ == '__main__':
    authors = []

    with open('author_list.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        authors = [{'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'institution': row['institution']} for row in reader]

    authors = sorted(authors, key=lambda k: k['last_name'])

    # list of the unique institutions ordered as the authors are
    institutions = []
    for author in authors:
        if author['institution'] not in institutions:
            institutions.append(author['institution'])

    # Get the number of the author's institution and write to string
    latex_file_string = ''
    for author in authors:
        author['institution_index'] = institutions.index(
            author['institution']) + 1
        latex_file_string += str(author['first_name']) + ' ' + str(author['last_name']) + \
            '$^{' + str(author['institution_index']) + '}$,\n'
    latex_file_string = latex_file_string[:-2] + '\n\\bigskip\n'

    for institution in institutions:
        latex_file_string += '\\par {\\footnotesize $^{' + \
            str(institutions.index(institution) + 1) + \
            '}$ ' + str(institution) + '}\n'

    latex_file_string += '\n\\clearpage\n'

    with open('src/authors.tex', 'w') as out_file:
        out_file.write(latex_file_string)

    # Add the editors
    editors = [author for author in authors if author['last_name'] in ['Feickert', 'Gleyzer', 'Seyfert', 'Schramm']]
    # Have order be Gleyzer, Seyfert, Schramm, Feickert
    editors = [editors[1], editors[3], editors[2], editors[0]]
    editors_string = '\\textbf{Editors}:'
    for editor in editors:
        editors_string += ' ' + str(editor['first_name']) + ' ' + str(editor['last_name']) + \
            '$^{' + str(editor['institution_index']) + '}$,'
    editors_string = editors_string[:-1] + '\\\\\\'
    subprocess.call(['sed', '-i.bak', '/Editors/c\{}'.format(editors_string), 'HSF_ML_CWP.tex'])
