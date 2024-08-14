# Workflow Quality Control

A post sequencing QC tool for Oxford Nanopore sequencers 

## Introduction

This workflow is dedicated to the QC analyses of Oxford Nanopore runs, and it is adapted to RNA-Seq along with DNA-Seq.

This QC tool supports only Guppy and Dorado basecaller output : sequencing_summary.txt and sequencing_telemetry.js files. 
Flow cells and kits version are retrieved using the telemetry file, but a a single FAST5 file can be used if a telemetry file is not provided. 
If the sequencing summary file is not available, ToulligQC can also accept FAST5, FASTQ or BAM files (but it will significantly increase the running time)

ToulligQC can take barcoding samples by adding the barcode list as an option.
ToulligQC deals with different file formats: gz, tar.gz, bz2 and tar.bz2. This tool will produce a set of graphs, statistic file in plain text format and a HTML report.


## Compute requirements
Minimum requirements:

+ CPUs = 1
+ Memory = 4GB

Approximate run time: Approximately 5 minutes for 10M reads with the minimum requirements.


## Install and run
These are instructions to install and run the workflow on command line. You can also access the workflow via the
[EPI2ME Desktop application](https://labs.epi2me.io/downloads/).

The workflow uses [Nextflow](https://www.nextflow.io/) to manage compute and software resources, therefore Nextflow will need to be installed before attempting to run the workflow.

The workflow can currently be run using either
[Docker](https://www.docker.com/products/docker-desktop
or [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/index.html)
to provide isolation of the required software. Both methods are automated out-of-the-box provided either Docker or Singularity is installed.
This is controlled by the [`-profile`](https://www.nextflow.io/docs/latest/config.html#config-profiles) parameter as exemplified below.

It is not required to clone or download the git repository in order to run the workflow.
More information on running EPI2ME workflows can be found on our [website](https://labs.epi2me.io/wfindex).

The following command can be used to obtain the workflow. This will pull the repository in to the assets folder of
Nextflow and provide a list of all parameters available for the workflow as well as an example command:

```
nextflow run genomiqueens/wf-toulligqc --help
```
To update a workflow to the latest version on the command line use the following command:
```
nextflow pull genomiqueens/wf-toulligqc
```

A demo dataset is provided for testing of the workflow. It can be downloaded and unpacked using the following commands:
```
wget https://github.com/GenomiqueENS/wf-toulligqc/raw/main/demo_data/wf-toulligqc-demo.tar.gz
tar -xzvf wf-toulligqc-demo.tar.gz
```
The workflow can then be run with the downloaded demo data using:
```
nextflow run genomiqueens/wf-toulligqc \
    --input_files 'sequencing_summary + telemetry_source' \
    --sequencing_summary_source 'demo_data/sequencing_summary.txt' \
    --telemetry_source 'demo_data/sequencing_telemetry.js'
```

For further information about running a workflow on
the command line see https://labs.epi2me.io/wfquickstart/


## Related protocols

This workflow is designed to take input sequences that have been produced from [Oxford Nanopore Technologies](https://nanoporetech.com/) devices.

Find related protocols in the [Nanopore community](https://community.nanoporetech.com/docs/).


## Inputs

### Input Options

| Nextflow parameter name  | Type | Description | Help | Default |
|--------------------------|------|-------------|------|---------|
| input_files | string | Select what type/ combination of input files to be used for the analysis | Workflow can be run with only the Guppy/ Dorado basecaller output file sequencing_summary.txt, or with the additional sequencing_telemetry.js. It can also be run with only FASTQ or BAM or FAST5 files.  | sequencing_summary.txt only |

### Sample Options

| Nextflow parameter name  | Type | Description | Help | Default |
|--------------------------|------|-------------|------|---------|
| sequencing_summary_source | string | Basecaller sequencing summary source, can be compressed with gzip (.gz) or bzip2 (.bz2) |  |  |
| telemetry_source | string |  Basecaller telemetry file source, can be compressed with gzip (.gz) or bzip2 (.bz2) |  | |
| fast5 | string |Fast5 file source, can also be in a tar.gz/tar.bz2 archive or a directory | Necessary if no telemetry file |  |
| fastq | string | FASTQ files to use in the analysis, can also be in a .gz archive | Necessary if no sequencing summary file |  |
| bam | string | BAM or SAM files to use in the analysis, can also be a SAM format. | Necessary if no sequencing summary file |  |

### Barcoding Options

| Nextflow parameter name  | Type | Description | Help | Default |
|--------------------------|------|-------------|------|---------|
| barcoding | boolean | BAM or SAM files to use in the analysis. |  | False |
| barcodes | string | Coma separated barcode list (e.g. BC05,RB09,NB01,barcode10) | ToulligQC handle the following naming schemes: BCXX, RBXX, NBXX and barcodeXX where XX is the number of the barcode |  |
| barcoding_summary_pass | string | Basecaller barcoding summary source of passed reads, can be compressed with gzip (.gz) or bzip2 (.bz2). |  |  |
| barcoding_summary_fail | string | Basecaller barcoding summary source of passed reads, can be compressed with gzip (.gz) or bzip2 (.bz2). |  |  |

### Advanced Options

| Nextflow parameter name  | Type | Description | Help | Default |
|--------------------------|------|-------------|------|---------|
| report_name | string | Name to give to report |  |  |
| disable_ping | boolean | Enable to prevent sending a workflow ping. |  | False |

## Outputs

| Title | File path | Description | Per sample or aggregated |
|-------|-----------|-------------|--------------------------|
| workflow report | ./wf-template-report.html | Report for all samples. | aggregated |

## Useful links

* [toulligqc](https://github.com/GenomiqueENS/toulligQC)
* [nextflow](https://www.nextflow.io/)
* [docker](https://www.docker.com/products/docker-desktop)
* [singularity](https://docs.sylabs.io/guides/latest/user-guide/)

See the [EPI2ME website](https://labs.epi2me.io/) for lots of other resources and blog posts.
