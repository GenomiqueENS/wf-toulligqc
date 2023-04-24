from dominate.tags import figure, div, section, h2
from dominate.util import raw
import datetime

#str(datetime.timedelta(seconds = sec))

metadata = {'Run statistics':[
        'toulligqc.info.report.name',
        'sequencing.telemetry.extractor.sample.id',
        'sequencing.telemetry.extractor.run.id',
        'sequencing.telemetry.extractor.exp.start.time',
        'sequencing.telemetry.extractor.flowcell.version',
        'sequencing.telemetry.extractor.kit.version',
        'sequencing.telemetry.extractor.barcode.kits.version',
        'basecaller.sequencing.summary.1d.extractor.yield',
        'basecaller.sequencing.summary.1d.extractor.n50',
        'basecaller.sequencing.summary.1d.extractor.l50',
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


def check_metadata(data, info, metadata=metadata):
    dico = dict()
    sample_details = {}
    with open(data,'r') as f:
        for line in f:
            (key, val) = line.split('=')
            dico[key] = val
    for meta in metadata[info]:
        key = ' '.join(meta.split('.')[3:]).capitalize()
        val = dico[meta].strip()
        if len(val) == 0:
            sample_details[key] = 'Unknown'
        else :
            sample_details[key] = val
    return sample_details


order=["Read_count_histogram.html",
    "Distribution_of_read_lengths.html",
    "Yield_plot_through_time.html",
    "PHRED_score_distribution.html",
    "PHRED_score_density_distribution.html",
    "Correlation_between_read_length_and_PHRED_score.html"
    "1D²_Correlation_between_1D²_read_length_and_PHRED_score.html",
    "Channel_occupancy_of_the_flowcell.html",
    "Read_length_over_time.html",
    "PHRED_score_over_time.html",
    "Translocation_speed.html",
    "Tead_pass_barcode_distribution.html",
    "Tead_fail_barcode_distribution.html",
    "Tead_size_distribution_for_barcodes.html",
    "PHRED_score_distribution_for_barcodes.html"]


def find_index(lst, element):
    if element in lst:
        return lst.index(element)
    else:
        return False


def clean_name(name):
    chars_to_remove = [",", "[", "]"]
    return ''.join([char for char in name if char not in chars_to_remove])


def resize_figure(rawText):
    # rawText.replace('height":562','height":500').replace('width":1000', 'width":850')
    # rawText.replace('height:562','height:500').replace('width:1000', 'width:850')
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
            figures[idx] = [f,ftitle]
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
    margin: 0.5em 0 0 0.5em;
    width: calc(366px - 0.5em);
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


def add_qc(args):
    figs = sort_figures(args)
    titles = [v[1] for v in figs.values()]
    with div(id = 'ma_division', style="display: flex"):
        with div(style="flex: 1"):
            raw(div_summary(titles))
        with div(style="flex: 1"):
            for i,f in enumerate(figs.values()):
                with open(f[0], 'r', encoding="UTF-8") as html:
                    html_contents = html.read()
                with figure(style="float: right"):
                    with section(id=str('M'+str(i))):
                        raw(html_contents.replace('562','500').replace('1000', '850'))