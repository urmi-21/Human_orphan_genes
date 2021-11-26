# Running Mikado
[Mikado](https://github.com/EI-CoreBioinformatics/mikado) tool was run to consolidate the transcriptome assemblies together.
A python wrapper using [pyrpipe v0.0.4](https://github.com/urmi-21/pyrpipe) was written to execute mikado.
A custom scoring file is used `mammalian_orphan.yaml` to maximize prediction of orphan genes.
First, samples from each tissue/tumor were run through mikado to get transcriptome for each tissue/tumor.
Next, all tissues were consolidated into GTEx and all tumors were consolidated into TCGA transcriptome.
Finally GTEx and TCGA transcriptome were merged with TACO and gencode reference  v33 to get final transcript assembly.
