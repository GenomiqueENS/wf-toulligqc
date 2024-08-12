# ToulligQC Workflow 

A post sequencing QC tool for Oxford Nanopore sequencers 

## Introduction

ToulligQC is dedicated to the QC analyses of Oxford Nanopore runs, and it is adapted to RNA-Seq along with DNA-Seq. \
This QC tool supports only Guppy and Dorado basecalling ouput files. It also needs a single FAST5 file (to catch the flowcell ID and the run date) if a telemetry file is not provided. \
Flow cells and kits version are retrieved using the telemetry file. ToulligQC can take barcoding samples by adding the barcode list as a command line option. 

If the sequencing summary file is not available, ToulligQC can also accept FASTQ or BAM files.

To do so, ToulligQC deals with different file formats: gz, tar.gz, bz2, tar.bz2 and .fast5 to retrieve a FAST5 information. This tool will produce a set of graphs, statistic file in plain text format and a HTML report.

To run ToulligQC you need the Guppy/ Dorado basecaller output files : sequencing_summary.txt and sequencing_telemetry.js. or FASTQ or BAM This can be compressed with gzip or bzip2. You can use your initial Fast5 ONT file too. ToulligQC can perform analyses on your data if the directory is organised as the following:

## Quickstart

The workflow uses [nextflow](https://www.nextflow.io/) to manage compute and
software resources, as such nextflow will need to be installed before attempting
to run the workflow.

The workflow can currently be run using either
[Docker](https://www.docker.com/products/docker-desktop) or
[Singularity](https://docs.sylabs.io/guides/latest/user-guide/) to provide isolation of
the required software. Both methods are automated out-of-the-box provided
either Docker or Singularity is installed.

It is not required to clone or download the git repository in order to run the workflow.
For more information on running EPI2ME Labs workflows [visit out website](https://labs.epi2me.io/wfindex).

**Workflow options**

To obtain the workflow, having installed `nextflow`, users can run:

```
nextflow run genomiqueens/wf-toulligqc --help
```

to see the options for the workflow.

## Input parameters

### Input Options

| Nextflow parameter name  | Type | Description | Help | Default |
|--------------------------|------|-------------|------|---------|
| sequencing_summary_source | string | Basecaller sequencing summary source, can be compressed with gzip (.gz) or bzip2 (.bz2) |  |  |
| barcoding_summary_pass | string | Basecaller barcoding summary source of passed reads, can be compressed with gzip (.gz) or bzip2 (.bz2). |  |  |
| barcoding_summary_fail | string | Basecaller barcoding summary source of passed reads, can be compressed with gzip (.gz) or bzip2 (.bz2). |  |  |
| telemetry_source | string |  Basecaller telemetry file source, can be compressed with gzip (.gz) or bzip2 (.bz2) |  | |
| fast5 | string |Fast5 file source, can also be in a tar.gz/tar.bz2 archive or a directory | Necessary if no telemetry file |  |
| fastq | string | FASTQ files to use in the analysis, can also be in a .gz archive | Necessary if no sequencing summary file |  |
| bam | string | BAM or SAM files to use in the analysis, can also be a SAM format. | Necessary if no sequencing summary file |  |
| barcoding | boolean | BAM or SAM files to use in the analysis. |  | False |
| barcodes | string | Coma separated barcode list (e.g. BC05,RB09,NB01,barcode10) | ToulligQC handle the following naming schemes: BCXX, RBXX, NBXX and barcodeXX where XX is the number of the barcode |  |

### Sample Options

| Nextflow parameter name  | Type | Description | Help | Default |
|--------------------------|------|-------------|------|---------|
| report_name | string | Name to give to report |  |  |

### Miscellaneous Options

| Nextflow parameter name  | Type | Description | Help | Default |
|--------------------------|------|-------------|------|---------|
| disable_ping | boolean | Enable to prevent sending a workflow ping. |  | False |
 	 		
## Workflow outputs

| Title | File path | Description | Per sample or aggregated |
|-------|-----------|-------------|--------------------------|
| workflow report | ./wf-template-report.html | Report for all samples. | aggregated |

## Useful links

* [nextflow](https://www.nextflow.io/)
* [docker](https://www.docker.com/products/docker-desktop)
* [singularity](https://docs.sylabs.io/guides/latest/user-guide/)
