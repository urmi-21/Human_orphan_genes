# Running TACO
[TACO (v0.7.3)](https://tacorna.github.io/) was run to consolidate transcriptomes for each tissues/tumor.
A python wrapper using [pyrpipe v0.0.4](https://github.com/urmi-21/pyrpipe) was written to execute TACO.
The workflow was scaled for all tissues/tumors using [snakemake](https://snakemake.readthedocs.io/en/stable/).
All tissues were consolidated into GTEx and all tumors were consolidated into TCGA transcriptome. These were then merged with mikado output.
**NOTE** Taco used all gtf files and was not limited to 200 files per tissue/tumor. TACO failed for some of the input files which were removed.

See the `start_taco.py` script to get an idea of the TACO step.