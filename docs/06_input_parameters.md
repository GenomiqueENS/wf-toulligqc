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