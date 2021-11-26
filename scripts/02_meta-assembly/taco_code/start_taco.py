import sys
from pyrpipe import pyrpipe_engine as pe
import os
import yaml

'''
[1] path to list file
[2] path to ref
[3] path to outdir

[1]tissuename



'''

#create a list file for gtfs
def create_listfile(fileslist,outname):
    f=open(outname,'w')
    for l in fileslist:
        #print(l)
        thisName=l.split('/')[-1].split('_')[0]
        if thisName:
            #print("\t".join([l,thisName,"False"]))
            f.write("\t".join([l,thisName,"False"])+'\n')

#read yml file with samples information
with open('gtex_tcga_samps.yaml') as file:
    d = yaml.load(file, Loader=yaml.FullLoader)

print ('gtex',len(d['gtex']))
print ('tcga',len(d['tcga']))
sys.exit(1)

REF='GCA_000001405.15_GRCh38_no_alt_analysis_set.fna'
REF_GTF='gencode.v33.annotation.gtf'
gtex_tissues=list(d['gtex'].keys())
tcga_tissues=list(d['tcga'].keys())
gtex_path_prefix='gtex/GTEx_GTFs_All'
tcga_path_prefix='tcga/TCGA_GTFs_All'
suff='_Aligned.out_sorted_stringtie.gtf'

thistissue=sys.argv[1]
#create list file
inlist=thistissue+'_list.txt'
if thistissue in d['gtex']:
    gtffiles=d['gtex'][thistissue]
    flist=[os.path.join(gtex_path_prefix,f+suff) for f in  gtffiles]
    create_listfile(flist,inlist)
elif thistissue in d['tcga']:
    gtffiles=d['tcga'][thistissue]
    flist=[os.path.join(tcga_path_prefix,f+suff) for f in  gtffiles]
    create_listfile(flist,inlist)
else:
    print ('EROOOORRRR')

outdir=thistissue+"_taco_out"

print('Running',inlist,REF,outdir)

taco_cmd=['taco_run', '-o', outdir, '-p', '28', '--filter-min-expr', '0.0', '--filter-min-length', '100', '--ref-genome-fasta',REF, '--assemble-unstranded', inlist]
pe.execute_command(taco_cmd)

##gtf to gff3
gff3_cmd='bash gtftogff.sh '+outdir+'/assembly.gtf '+outdir+'/assembly.gff3'
#gffread -E assembly.gtf > assembly.gff3'
pe.execute_command(gff3_cmd.split())

os.chdir(outdir)
print('cwd',os.getcwd())
##run mikado compare
comp_cmd='mikado compare -r /pylon5/mc5pl7p/usingh/urmi/human_pipeline/gtex_tcga/human_reference/gencode.v33.annotation.gtf -p assembly.gff3 -l mik_compare.log'
pe.execute_command(comp_cmd.split())










