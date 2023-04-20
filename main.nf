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
        val cc
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
        --qc ${cc.join()}
    """
}

process toulligqc {
    label "wfqc"
    input:
        path seq_summary
        path seq_telometry
    output:
        path "QC-repport/report.data", emit: report_data
        path "QC-repport/images/*.html", emit: plots_html
        path "QC-repport/images/plotly.min.js", emit: plotly_js
    script:
        String report_name = "QC-repport"
    """
    toulligqc -a ${seq_summary} \
    --telemetry-source  ${seq_telometry} \
    -n $report_name \
    --force 
    """
}

// See https://github.com/nextflow-io/nextflow/issues/1636. This is the only way to
// publish files from a workflow whilst decoupling the publish from the process steps.
// The process takes a tuple containing the filename and the name of a sub-directory to
// put the file into. If the latter is `null`, puts it into the top-level directory.
process output {
    // publish inputs to output directory
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

// Creates a new directory named after the sample alias and moves the fastcat results into it.
// workflow module
workflow pipeline {
    take:
        seq_summary
        seq_telometry
    main:
        software_versions = getVersions()

        workflow_params = getParams()

        toulligqc(seq_summary, seq_telometry)

        plotly_js = toulligqc.out.plotly_js

        plots_html = toulligqc.out.plots_html.toList()

        report = makeReport(
            plots_html, toulligqc.out.report_data, software_versions.collect(), workflow_params
        )
    emit:
        plotly_js
        report
        workflow_params
        // TODO: use something more useful as telemetry
        telemetry = workflow_params
}


// entrypoint workflow
WorkflowMain.initialise(workflow, params, log)
workflow {

    if (params.disable_ping == false) {
        Pinguscript.ping_post(workflow, "start", "none", params.out_dir, params)
    }

    seq_summary = file(params.sequencing_summary, type: "file")
    seq_telometry = file(params.sequencing_telometry, type: "file")

    pipeline(seq_summary, seq_telometry)
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
