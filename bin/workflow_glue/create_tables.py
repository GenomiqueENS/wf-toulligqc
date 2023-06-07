import plotly.graph_objects as go

font = dict(size = 14)


def extract_metadata(data_file):
    """
    Extracts metadata from a data file and returns a dictionary containing the extracted information.
    :param data_file: Le chemin du fichier de données à analyser.
    :return: Un dictionnaire contenant les informations extraites.
    """
    data_dict = {
        '1d': {},
        'barcodes': {},
        'frequency': {}
    }

    with open(data_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('basecaller.sequencing.summary.1d.') and 'barcode' not in line and 'unclassified' not in line :
                key, value = line.split('=')
                key = ' '.join(key.split('.')[5:]).capitalize()
                data_dict['1d'][key] = value

            elif 'barcode' in line or 'unclassified' in line:
                if 'count' in line:
                    key, value = line.split('=')
                    key = ' '.join(key.split('.')[5:])
                    data_dict['barcodes'][key] = value

                elif 'frequency' in line:
                    key, value = line.split('=')
                    key = ' '.join(key.split('.')[5:])
                    if key.startswith('read') and 'barcoded' not in key:
                        data_dict['frequency'][key] = value

    return data_dict


def create_table(data, table_width, table_height, margin):
    fig = go.Figure(data)
    fig.update_layout(
        width=table_width,
        height=table_height,
        margin=dict(l=margin, 
                    r=margin, 
                    t=20, 
                    b=0) 
    )
    return fig.to_html()


def read_count_table(reads_data):

    reads_data = reads_data['1d']

    data=[go.Table(
                   header=dict(values=['','<b>All reads</b>', '<b>Pass reads</b>', '<b>Fail reads</b>'], font = font),
                   cells =dict(values=[['<b>Count</b>', '<b>Percent</b>'],
                                      [reads_data['Read count'], _round2(reads_data['Read count frequency'])],
                                      [reads_data['Read pass count'], _round2(reads_data['Read pass frequency'])],
                                      [reads_data['Read fail count'], _round2(reads_data['Read fail frequency'])]
                                      ],
                                font = font)
                   )]
    
    table_height = 150 
    table_width = 1000

    return create_table(data, 
                        table_width, 
                        table_height,
                        margin = 150) 


def read_table(reads_data, motif1, motif2):

    reads_data = reads_data['1d']
    header=dict(values=['','<b>All reads</b>', '<b>Pass reads</b>', '<b>Fail reads</b>'], font = font)

    cells = get_cells(reads_data, motif1, motif2)

    data=[go.Table(header=header,
                   cells =dict(values=[['<b>count</b>', '<b>mean</b>' , '<b>std</b>' , '<b>min</b>' , '<b>25%</b>' , '<b>median</b>', '<b>75%</b>', '<b>max</b>'],
                                      cells['all_reads'],
                                      cells['pass_reads'],
                                      cells['fail_reads']
                                      ],
                                font = font)
                   )]
    
    table_height = 400 
    table_width = 1000

    return create_table(data, 
                        table_width, 
                        table_height,
                        margin = 250)  


def barcodes_table(barcodes_data, reads):
    
    header=dict(values=['', '<b>Barcode arrangement (%)</b>', '<b>Read count</b>'], font = font)

    cells = get_cells_for_barcodes(barcodes_data)
    cell_barcode = cells['barcodes']['pass_barcodes'] if reads == 'Pass reads' else cells['barcodes']['fail_barcodes']
    cell_frequency = cells['barcodes']['read_pass'] if reads == 'Pass reads' else cells['barcodes']['read_fail']
    cell_reads_count = cells['read_pass'] if reads == 'Pass reads' else cells['read_fail']

    data=[go.Table(header=header,
                   cells =dict(values=[cell_barcode,
                                       cell_frequency,
                                       cell_reads_count
                                      ],
                                font = font)
                   )]
    
    table_height = 400 
    table_width = 1000

    return create_table(data, 
                        table_width, 
                        table_height,
                        margin = 250) 


def get_cells(metadata, motif1, motif2):

    all_reads=[_round2(item) for item in [metadata['All read length count'],
               metadata['All read '+motif1+' mean'],
               metadata['All read '+motif1+' std'],
               metadata['All read '+motif1+' min'],
               metadata['All read '+motif1+' 25%'],
               metadata['All read '+motif1+' 50%'],
               metadata['All read '+motif1+' 75%'],
               metadata['All read '+motif1+' max']
    ]]
    pass_reads=[_round2(item) for item in [metadata['Read pass count'],
               metadata['Pass reads '+motif2+' mean'],
               metadata['Pass reads '+motif2+' std'],
               metadata['Pass reads '+motif2+' min'],
               metadata['Pass reads '+motif2+' 25%'],
               metadata['Pass reads '+motif2+' 50%'],
               metadata['Pass reads '+motif2+' 75%'],
               metadata['Pass reads '+motif2+' max']
    ]]
    fail_reads=[_round2(item) for item in [metadata['Read fail count'],
               metadata['Fail reads '+motif2+' mean'],
               metadata['Fail reads '+motif2+' std'],
               metadata['Fail reads '+motif2+' min'],
               metadata['Fail reads '+motif2+' 25%'],
               metadata['Fail reads '+motif2+' 50%'],
               metadata['Fail reads '+motif2+' 75%'],
               metadata['Fail reads '+motif2+' max']
    ]]  
    dico_data = dict(all_reads = all_reads,
                     pass_reads = pass_reads,
                     fail_reads = fail_reads)
    
    return dico_data


def get_cells_for_barcodes(metadata):

    barcode_infos = metadata['barcodes']
    frequency_infos = metadata['frequency']
    SKIP_WORDS = ['base', 'non', 'barcoded']
    
    cells = {
        'all_read': [],
        'read_pass': [],
        'read_fail': [],
        'barcodes': {
            'pass_barcodes': [],
            'fail_barcodes': [],
            'read_pass': [],
            'read_fail': []
        }
    }
 
    for barcode, value in barcode_infos.items():

        if any(word in barcode for word in SKIP_WORDS) or float(value) == 0.0:
            continue

        barcode_parts = barcode.split(' ')
        read_key = "{}_{}".format(barcode_parts[0], barcode_parts[1])
        cells[read_key].append(_round2(value))
    
    for frequency, value in frequency_infos.items():
        if float(value) == 0.0:
            continue  
        frequency_parts = frequency.split(' ')
        read_key = "{}_{}".format(frequency_parts[0], frequency_parts[1])
        value = _round2(value) + '%' 
        cells['barcodes'][read_key].append(value)
        
        barcode = ' '.join(frequency_parts[2:-1])
        barcode = "<b>" + barcode + "</b>"
        barcode_key = "{}_barcodes".format(frequency_parts[1])
        if barcode not in cells['barcodes'][barcode_key]:
            cells['barcodes'][barcode_key].append(barcode)

    return cells


def tables(data_file):
    data = extract_metadata(data_file)

    tables = {"Read count histogram":read_count_table(data),
              "Distribution of read lengths":read_table(data, 'length', 'sequence length'),
              "PHRED score distribution":read_table(data, 'qscore', 'mean qscore'),
              "Pass barcoded reads distribution":barcodes_table(data, 'Pass reads'),
              "Fail barcoded reads distribution":barcodes_table(data, 'Fail reads')
              }
    
    return tables


def _round2(num):
        if "." in num:
            num = "{:.2f}".format(float(num))
            if '.00' in num:
                return "{:,d}".format(int(float(num)))
            else : return num
        else:
            return "{:,d}".format(int(num))