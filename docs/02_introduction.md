This workflow is dedicated to the quality control analyses of Oxford Nanopore runs. 

ToulligQC is adapted to RNA-Seq along with DNA-Seq and it is compatible with 1D² runs. This QC tool supports only Guppy and Dorado basecalling ouput files. It also needs a single FAST5 file (to catch the flowcell ID and the run date) if a telemetry file is not provided. Flow cells and kits version are retrieved using the telemetry file. ToulligQC can take barcoding samples by adding the barcode list as an option.

If the sequencing summary file is not available, ToulligQC can also accept FASTQ or BAM or FAST5 files.
