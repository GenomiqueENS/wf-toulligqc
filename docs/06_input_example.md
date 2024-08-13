This workflow accepts Guppy/ Dorado basecaller output files : sequencing_summary.txt and sequencing_telemetry.js or FASTQ or BAM or FAST5.
This can be compressed with gzip or bzip2. 

ToulligQC can perform analyses on your data if the directory is organised as the following:

```
RUN_ID
├── sequencing_summary.txt
└── sequencing_telemetry.js
```