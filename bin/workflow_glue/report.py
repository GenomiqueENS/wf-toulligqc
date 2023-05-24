"""Create workflow report."""
import json
from ezcharts.components.reports import labs
from ezcharts.layout.snippets import Tabs
from ezcharts.layout.snippets.table import DataTable
from dominate.tags import div
import pandas as pd
from .util import get_named_logger, wf_parser 
from .filter_metadata import check_metadata, add_qc

def main(args):
    """Run the entry point."""
    logger = get_named_logger("Report")
    report = labs.LabsReport(
        "Workflow QC report", "wf-QC",
        args.params, args.versions)

    with report.add_section("Metadata", "Metadata"):
        tabs = Tabs()
        with tabs.add_tab("Overall statistics"):
            run_statistics = check_metadata(args.metadata, 'Overall statistics')
            df = pd.DataFrame.from_dict(run_statistics, orient="index", columns=["Value"])
            df.index.name = "Key"
            DataTable.from_pandas(df)

        with tabs.add_tab("Run metadata"):
            run_statistics = check_metadata(args.metadata, 'Run metadata')
            df = pd.DataFrame.from_dict(run_statistics, orient="index", columns=["Value"])
            df.index.name = "Key"
            DataTable.from_pandas(df)

        with tabs.add_tab("Device and software"):
            device_info = check_metadata(args.metadata, "Device and software")
            df = pd.DataFrame.from_dict(device_info, orient="index", columns=["Value"])
            df.index.name = "Key"
            DataTable.from_pandas(df)

    with report.add_section("QC report", "QC report"):
        #with div(style="overflow: auto; max-width: 100%"):
                add_qc(args.qc)

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
