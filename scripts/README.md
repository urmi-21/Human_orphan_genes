# Overview of the human orphan gene identification pipeline

<p>
    <img src="https://raw.githubusercontent.com/urmi-21/Human_orphan_genes/main/scripts/figs/Humanorphanpipeline.png" alt>
    <em>
	Workflow of the study. The alignment and quantification pipelines are implemented in <a href=https://github.com/urmi-21/pyrpipe/tree/master/case_studies/GTEx_processing>pyrpipe</a>.
For alignment, BAM files were downloaded from GTEx and converted to fastq using <a href=https://gitlab.com/german.tischler/biobambam2>biobambam2</a>. <a href=https://github.com/alexdobin/STAR>STAR</a> was run in 2-pass alignment mode to align reads to the human reference genome <a href=https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38>GRCh38 GCA_000001405.15</a>. 
	    Transcripts were assembled by <a href=https://ccb.jhu.edu/software/stringtie> Stringtie </a>. 
Individual transcriptomes were consolidated into single transcriptome using our meta-assembly pipeline, consisting of <a href=https://github.com/EI-CoreBioinformatics/mikado> Mikado </a> and <a href=https://tacorna.github.io/> Taco </a>. ORFs were identified by <a href=https://github.com/urmi-21/orfipy> orfipy </a>.
	For quantification, a <a href=https://salmon.readthedocs.io/en/latest/salmon.html> Salmon </a> index was build using human annotated and novel identified transcripts, with whole human genome sequence used as a decoy. BAM files were downloaded from <a href=https://gtexportal.org/home> GTEx </a> and <a href=https://portal.gdc.cancer.gov> TCGA </a>  , converted to fastq (using biobambam2) and passed to Salmon's \textit{quant} function for quantification. <a href=https://github.com/arendsee/phylostratr> phylostratr </a> was used to infer phylostrata of all Gencode annotated proteins and for each EB transcript.
</em>
</p>
