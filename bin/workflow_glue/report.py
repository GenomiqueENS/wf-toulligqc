"""Create workflow report."""
import json

from ezcharts.components import fastcat
from ezcharts.components.reports import labs
from ezcharts.layout.snippets import Tabs, Stats
from ezcharts.layout.snippets.table import DataTable
from dominate import document
from dominate.util import raw
from dominate.tags import div, figure, iframe
import pandas as pd

from .util import get_named_logger, wf_parser  # noqa: ABS101
from .filter_metadata import check_metadata

def main(args):
    """Run the entry point."""
    logger = get_named_logger("Report")
    report = labs.LabsReport(
        "Workflow QC report", "wf-QC",
        args.params, args.versions)

    sample_details = check_metadata(args.metadata)
    
    with report.add_section("Metadata", "Metadata"):
        tabs = Tabs()
        with tabs.add_tab("Sequencing"):
            df = pd.DataFrame.from_dict(sample_details, orient="index", columns=["Value"])
            df.index.name = "Key"
            DataTable.from_pandas(df)

    with report.add_section("QC report", "QC report"):
        chars_to_remove = [",", "[", "]"]
        for filename in args.qc: 
            fig = ''.join([char for char in filename if char not in chars_to_remove])
            
            with open(fig, 'r', encoding="UTF-8") as f:
                file_contents = f.read()
            with figure():
                raw(file_contents)

    report.write(args.report)
    logger.info(f"Report written to {args.report}.")


def argparser():
    """Argument parser for entrypoint."""
    parser = wf_parser("report")
    parser.add_argument("report", help="Report output file")
    parser.add_argument("--stats", nargs='*', help="Fastcat per-read stats file(s).")
    parser.add_argument(
        "--metadata", default='metadata.json',
        help="sample metadata")
    parser.add_argument(
        "--versions", required=True,
        help="directory containing CSVs containing name,version.")
    parser.add_argument(
        "--params", default=None, required=True,
        help="A JSON file containing the workflow parameter key/values")
    parser.add_argument(
        "--revision", default='unknown',
        help="git branch/tag of the executed workflow")
    parser.add_argument(
        "--commit", default='unknown',
        help="git commit of the executed workflow")
    parser.add_argument(
        "--qc", nargs='+', default='unknown',
        help="toulligQC html report file")
    return parser
