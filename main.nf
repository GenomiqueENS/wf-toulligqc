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
        path seq_telemetry
        path fast5
        path seq_1dsqr
        val report_name
    output:
        path "$report_name/report.data", emit: report_data
        path "$report_name/images/*.html", emit: plots_html
        path "$report_name/images/plotly.min.js", emit: plotly_js
    script:
        //String report_name = "QC-repport"
        def telemetry_arg = seq_telemetry.name != 'No_telemetry' ? "--telemetry-source $seq_telometry" : ""
        def fast5_arg = fast5.name != 'No_fast5' ? "--fast5-source $fast5" : ""
        def seq_1dsqr_arg = seq_1dsqr.name != 'No_seq_1dsqr' ? "--sequencing-summary-1dsqr-source $seq_1dsqr" : ""
    """
    toulligqc -a ${seq_summary} \
    $telemetry_arg  $fast5_arg  $seq_1dsqr_arg \
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
        seq_telemetry
        fast5
        seq_1dsqr
        report_name
    main:
        software_versions = getVersions()

        workflow_params = getParams()

        toulligqc(seq_summary, seq_telemetry, fast5, seq_1dsqr, report_name)

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

    seq_summary = file(params.sequencing_summary_source, type: "file")
    seq_telemetry = params.telemetry_source != null ? file(params.telemetry_source, type: "file") : file("No_telemetry", type: "file")
    fast5 = params.fast5_source != null ? file(params.fast5_source, type: "file") : file("No_fast5", type: "file")
    seq_1dsqr = params.seq_1dsqr != null ? file(params.seq_1dsqr, type: "file") : file("No_seq_1dsqr", type: "file")
    report_name = params.report_name

    pipeline(seq_summary, seq_telemetry, fast5 , seq_1dsqr, report_name)
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
