#!/usr/bin/env nextflow

// Developer notes
//
// This template workflow provides a basic structure to copy in order
// to create a new workflow. Current recommended practices are:
//     i) create a simple command-line interface.
//    ii) include an abstract workflow scope named "pipeline" to be used
//        in a module fashion
//   iii) a second concrete, but anonymous, workflow scope to be used
//        as an entry point when using this workflow in isolation.

import groovy.json.JsonBuilder
nextflow.enable.dsl = 2

OPTIONAL_FILE = file("$projectDir/data/OPTIONAL_FILE")

process getVersions {
    label "wfqc"
    cpus 1
    output:
        path "versions.txt"
    script:
    """
    toulligqc --version | sed 's/^/toulligQC,/' >> versions.txt
    """
}

process getParams {
    label "wfqc"
    cpus 1
    output:
        path "params.json"
    script:
        String paramsJSON = new JsonBuilder(params).toPrettyString()
    """
    # Output nextflow params object to JSON
    echo '$paramsJSON' > params.json
    """
}

process makeReport {
    label "wfqc"
    input:
        val plots_html
        path "QC-repport/report.data"
        path "versions/*"
        path "params.json"
    output:
        path "wf-template-*.html"
    script:
        String report_name = "wf-template-report.html"
    """
    workflow-glue report $report_name \
        --versions versions \
        --params params.json \
        --metadata QC-repport/report.data \
        --qc ${plots_html.join()}
    """
}

process toulligqc {
    //debug true 
    label "wfqc"
    input:
        path seq_summary
        path summary_pass
        path summary_fail
        path seq_telemetry
        path fast5
        path bam
        path fastq
        val report_name
        val barcodes
        val barcoding
    output:
        path "$report_name/report.data", emit: report_data
        path "$report_name/images/*.html", emit: plots_html
        path "$report_name/images/plotly.min.js", emit: plotly_js
    script:
        def seq_summary_arg = seq_summary.name != 'no_seq_summary' ? "--sequencing-summary-source $seq_summary" : ""
        def summary_pass_arg = summary_pass.name != 'no_barcoding_pass' ? "--sequencing-summary-source $summary_pass" : ""
        def summary_fail_arg = summary_fail.name != 'no_barcoding_fail' ? "--sequencing-summary-source $summary_fail" : ""
        def telemetry_arg = seq_telemetry.name != 'no_telemetry' ? "--telemetry-source $seq_telemetry" : ""
        def fast5_arg = fast5.name != 'no_fast5' ? "--fast5-source $fast5" : ""
        def bam_arg = bam.name != 'no_bam' ? "--bam $bam" : ""
        def fastq_arg = fastq.name != 'no_fastq' ? "--fastq $fastq" : ""
        def barcodes_list = barcodes != 'no_barcodes' ? "--barcodes $barcodes" : ""
        def barcoding = barcoding != 'false' ? "--barcoding" : ""
    """
    toulligqc $seq_summary_arg \
    $summary_pass_arg  $summary_fail_arg \
    $telemetry_arg  \
    $fast5_arg $fastq_arg $bam_arg\
    $barcoding  $barcodes_list \
    -n $report_name \
    --force 
    """
} 

process output {
    label "wfqc"
    publishDir (
        params.out_dir,
        mode: "copy",
        saveAs: { dirname ? "$dirname/$fname" : fname }
    )
    input:
        tuple path(fname), val(dirname)
    output:
        path fname
    """
    """
}

workflow pipeline {
    take:
        seq_summary
        summary_pass
        summary_fail
        seq_telemetry
        fast5
        bam
        fastq
        report_name
        barcodes
        barcoding
    main:
        software_versions = getVersions()

        workflow_params = getParams()

        toulligqc(seq_summary, summary_pass, summary_fail, seq_telemetry, fast5, fastq, bam, report_name, barcodes, barcoding)

        plotly_js = toulligqc.out.plotly_js

        plots_html = toulligqc.out.plots_html.toList()

        report = makeReport(
            plots_html, toulligqc.out.report_data, software_versions.collect(), workflow_params
        )
    emit:
        plotly_js
        report
        workflow_params
        telemetry = workflow_params
}

// entrypoint workflow
WorkflowMain.initialise(workflow, params, log)
workflow {

    if (params.disable_ping == false) {
        Pinguscript.ping_post(workflow, "start", "none", params.out_dir, params)
    }

    seq_summary = params.sequencing_summary_source != null ? file(params.sequencing_summary_source, type: "file") : file("no_sequencing_summary", type: "file")
    summary_pass = params.barcoding_summary_pass != null ? file(params.barcoding_summary_pass, type: "file") : file("no_barcoding_pass", type: "file")
    summary_fail = params.barcoding_summary_fail != null ? file(params.barcoding_summary_fail, type: "file") : file("no_barcoding_fail", type: "file")
    seq_telemetry = params.telemetry_source != null ? file(params.telemetry_source, type: "file") : file("no_telemetry", type: "file")
    fast5 = params.fast5_source != null ? file(params.fast5_source, type: "file") : file("no_fast5", type: "file")
    fastq = params.fastq_source != null ? file(params.fastq_source, type: "file") : file("no_fastq", type: "file")
    bam = params.bam_source != null ? file(params.bam_source, type: "file") : file("no_bam", type: "file")
    barcodes = params.barcodes != null ? params.barcodes : "no_barcodes"
    barcoding = params.barcoding
    report_name = params.report_name

    pipeline(seq_summary, summary_pass, summary_fail, seq_telemetry, fast5, fastq, bam, report_name, barcodes, barcoding)
    pipeline.out.report.concat(pipeline.out.workflow_params).concat(pipeline.out.plotly_js)
    | map { [it, null] }

    | output
}

if (params.disable_ping == false) {
    workflow.onComplete {
        Pinguscript.ping_post(workflow, "end", "none", params.out_dir, params)
    }

    workflow.onError {
        Pinguscript.ping_post(workflow, "error", "$workflow.errorMessage", params.out_dir, params)
    }
}
