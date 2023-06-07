from dominate.tags import figure, div, section, h2
from dominate.util import raw
import locale
from collections import defaultdict
import plotly.graph_objects as go

#str(datetime.timedelta(seconds = sec))

metadata = {'Overall statistics':[
        'toulligqc.info.report.name',
        'sequencing.telemetry.extractor.sample.id',
        'basecaller.sequencing.summary.1d.extractor.yield',
        'basecaller.sequencing.summary.1d.extractor.n50',
        'basecaller.sequencing.summary.1d.extractor.l50',
    ],
    'Run metadata':[
        'sequencing.telemetry.extractor.run.id',
        'sequencing.telemetry.extractor.exp.start.time',
        'sequencing.telemetry.extractor.flowcell.version',
        'sequencing.telemetry.extractor.kit.version',
        'sequencing.telemetry.extractor.barcode.kits.version',
        'basecaller.sequencing.summary.1d.extractor.run.time'
    ],
    'Device and software': [
        'sequencing.telemetry.extractor.minknow.version',
        'sequencing.telemetry.extractor.device.id',
        'sequencing.telemetry.extractor.device.type',
        'sequencing.telemetry.extractor.distribution.version',
        'sequencing.telemetry.extractor.software.name',
        'sequencing.telemetry.extractor.software.version']
    }


order=["Read_count_histogram.html",
    "Distribution_of_read_lengths.html",
    "Yield_plot_through_time.html",
    "PHRED_score_distribution.html",
    "PHRED_score_density_distribution.html",
    "Correlation_between_read_length_and_PHRED_score.html",
    "Channel_occupancy_of_the_flowcell.html",
    "Read_length_over_time.html",
    "PHRED_score_over_time.html",
    "Translocation_speed.html",
    "Pass_barcoded_reads_distribution.html",
    "Fail_barcoded_reads_distribution.html",
    "Read_size_distribution_for_barcodes.html",
    "PHRED_score_distribution_for_barcodes.html",
    ]


def defaultCount():
	return 'Unknown'


def _format_int(i):
    return '{:,d}'.format(i)


def _format_int_with_prefix(i):
    for x in ((12, 'T'), (9, 'G'), (6, 'M'), (3, 'K')):
        if i / 10 ** x[0] > 1:
            return '{:.2f}{}'.format(float(i) / float(10 ** x[0]), x[1])
    return i


def _format_run_time(seconds):
    return '%dh%02dm%02ds' % (seconds // 3600, (seconds % 3600) // 60, seconds % 60)


def read_data_file(data):
    dico = defaultdict(defaultCount)
    with open(data,'r') as f:
            for line in f:
                (key, val) = line.split('=')
                dico[key] = val
    return dico


def check_metadata(dataFile, metadata=metadata):
    metadata_dict = {}
    data = read_data_file(dataFile)
    for section in metadata:
        section_details = {}
        for info in metadata[section]:
            key = ' '.join(info.split('.')[3:]).capitalize()
            val = data[info].strip()
            if len(val) == 0:
                section_details[key] = 'Unknown'
            else :
                if '50' in key:
                    key = str(key.split(' ')[2]).capitalize()
                    val = _format_int(int(val))
                if 'yield' in key:
                    key = str(key.split(' ')[2]).capitalize()
                    val = _format_int_with_prefix(int(val))
                if 'run time' in key:
                    key = ' '.join(key.split(' ')[2:]).capitalize()
                    val = _format_run_time(locale.atof(val))
                section_details[key] = val
        metadata_dict[section] = section_details
    return metadata_dict


def extract_metadata(data):
    data_dict = {}
    with open(data,'r') as f:
        for line in f:
            if line.startswith('basecaller.sequencing.summary.1d.'):
                key, value = line.strip().split('=')
                key = ' '.join(key.split('.')[5:]).capitalize()
                data_dict[key] = float(value)
    return data_dict



def find_index(lst, element):
    if element in lst:
        return lst.index(element)+1
    else:
        return False


def clean_name(name):
    chars_to_remove = [",", "[", "]"]
    return ''.join([char for char in name if char not in chars_to_remove])


def resize_figure(rawText):
    rawText.replace('562','500').replace('1000', '850')
    return rawText


def sort_figures(files, order=order):
    figures = dict()
    outIdx = len(files)
    for f in files:
        f = clean_name(f)
        _, fname = f.rsplit('/',1)
        ftitle = fname.split('.')[0].replace('_', ' ')
        idx = find_index(order, fname) 
        if idx:  
            figures[idx-1] = [f,ftitle]
        else: 
            figures[outIdx] = [f,ftitle]
            outIdx+=1
    return dict(sorted(figures.items()))


def _summary(graphs):
    """
    Compose the summary section of the page
    :param graphs:
    :return: a string with HTML code for the module list
    """
    result = "        <ul class=\"menu-vertical\">\n"
    for i, t in enumerate(graphs):
        result += "          <li class=\"mv-item\"><a href=\"#M" + str(i) + "\">" + t + "</a></li>\n"
    result += "        </ul>\n"
    return result


def div_summary(titles):
    style = """
    <style>
    #leftCol {
    position: -webkit-sticky;
    position: sticky;
    top: 80px;
    font-size: 0.9em;
    margin: 0.5em 0 0 0.5em;
    width: calc(250px - 0.01em);
    }

    .qc-toc {
        display: none;
    }

    .qc-report .qc-toc {
        display: flex;
    }
    .menu-vertical {
    right: 1em;
    padding: 1px;
    margin-right : 1em;
    list-style: none;
    text-align: left;
    background: #F2F2F2;
    }

    .mv-item, .mv-item a {
    display: block;
    }

    .mv-item a {
    margin: 1px 0;
    padding: 8px 20px;
    color: #666;
    background: #FFF;
    text-decoration: none;
    transition: all .3s;
    }

    .mv-item a:hover, .mv-item a:focus {
    background: rgba(var(--bs-dark-rgb), var(--bs-bg-opacity)) !important;
    color: #FFF;
    padding-left: 30px;
    }

    .mv-item a:enabled {
    font-weight: bold;
    }
    </style>
    """
    menu = """
    <div id="leftCol">
          <!--h2>Summary</h2-->
    {summary_list}
    </div>
    """.format(summary_list=_summary(titles))
    html = style+menu
    return html


def add_qc(args, tables):
    figs = sort_figures(args)
    titles = [v[1] for v in figs.values()]
    with div(style="display: flex"):
        with div(style="flex: 1"):
            raw(div_summary(titles))
        with div(style="flex: 4; overflow: auto"):
            for i,f in enumerate(figs.values()):
                with open(f[0], 'r', encoding="UTF-8") as html:
                    html_contents = html.read()
                with figure(style="float: right"):
                    with section(id=str('M'+str(i))):
                        raw(html_contents)
                        if f[1] in tables:
                            raw(tables[f[1]])