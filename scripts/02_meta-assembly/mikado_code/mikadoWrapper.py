'''
Use pyrpipe to build mikado pipeline

[1]-->input file with path to GTFs
[2]-->yaml file with parameters
[3]-->output directory
[4]-->samp type gtex/tcga
'''
import sys
import os
from pyrpipe import pyrpipe_engine as pe
from pyrpipe import pyrpipe_utils as pu
import yaml

def create_list_file(infile,outdir):
	'''
	create list file to be read by mikado configure
	infile is a file contating absolute paths to gtf files
	'''
	with open(infile) as f:
		temp=f.read().splitlines()
	gtfs=[]
	for l in temp:
		#print(l)
		thisName=l.split('/')[-1].split('_Aligned.out_sorted_stringtie.gtf')[0]
		if thisName:
			gtfs.append("\t".join([l,thisName,"False"]))

	f=open(os.path.join(outdir,'list.txt'),"w")
	f.write("\n".join(gtfs))
	f.close()
	if pu.check_files_exist(os.path.join(outdir,'list.txt')):
		print('list.txt contains {} GTFs'.format(len(gtfs)))
		return True
	return False

#check infile
if not pu.check_files_exist(sys.argv[1]):
	print("Please check input file {}".format(sys.argv[1]))
	sys.exit(1)

if not pu.check_files_exist(sys.argv[2]):
	print("Please check input file {}".format(sys.argv[2]))
	sys.exit(1)

#check output folder; exit if folder exists dont overwrite
if pu.check_paths_exist(sys.argv[3]):
	print("Output directory {} already exists...EXITING".format(sys.argv[3]))
	sys.exit(1)
#create the folder
outdir=sys.argv[3]
pu.mkdir(outdir)


#copy list file
pathfile=os.path.join(outdir,'gtfpaths.txt')
cmd='cp '+sys.argv[1]+' '+pathfile
pe.execute_command(cmd.split())
#write list file
if not create_list_file(pathfile,outdir):
	print('Error creating list file {}'.format(os.path.join(outdir,'list.txt')))
	sys.exit(1)

#read parameters
PATH_TO_PARAMS=sys.argv[2]
with open(PATH_TO_PARAMS) as file:
        params = yaml.full_load(file)

mikado_params=params['mikado']
gtf=params['gtf']
genome=params['genome']
tcga_juncs=params['tcga_juncs']
gtex_juncs=params['gtex_juncs']
tcga_gtex_juncs=params['tcga_gtex_juncs']

#select junctions to use
if sys.argv[4] =="gtex":
    juncs=gtex_juncs
elif sys.argv[4]=="tcga":
    juncs=tcga_juncs
else:
    print("Specify sample type gtex/tcga")
    sys.exit(1)

#change dir to output directory
os.chdir(outdir)

pu.print_green('started analysis')
#Start mikado pipelines
scoring=mikado_params['scoring']
mode=mikado_params['mode']
seed=mikado_params['seed']
threads=mikado_params['threads']
min_cdna=mikado_params['min_cdna']
config_file_name=mikado_params['config_file_name']

print('Seed:',seed)

#step 1: configure
config_cmd=['mikado','configure', '--list','list.txt','--reference', genome,'--mode',mode,'--scoring',scoring,'--junctions',juncs,'--seed',seed,'-t',threads,'--minimum-cdna-length',min_cdna,config_file_name]
#print (' '.join(config_cmd))
pe.execute_command(config_cmd)

#step2 prepare;set p 1 to avoid cuncurrency issues
prepare_cmd=['mikado','prepare','--json-conf',config_file_name,'-m',min_cdna,'-p','1','--seed',seed]
#print(' '.join(prepare_cmd))
pe.execute_command(prepare_cmd)


#step 3: find orfs
#t1cmd=['TransDecoder.LongOrfs', '-t', 'mikado_prepared.fasta']
#t2cmd=['TransDecoder.Predict', '-t', 'mikado_prepared.fasta', '--cpu',threads]

#pe.execute_command(t1cmd)
#pe.execute_command(t2cmd)

orfipycmd=['orfipy','mikado_prepared.fasta','--min','100','--outdir','orfipy_out','--bed12','orfs.bed','--include-stop','--start','ATG']
orfs_st=pe.execute_command(orfipycmd)
if not orfs_st:
    print('Orfipy failed')
    sys.exit(1)
orfs="orfipy_out/orfs.bed"

#step 4 serialise
ser_cmd=['mikado','serialise', '--json-conf',config_file_name,'--orfs',orfs,'-nsa','-p',threads,'--max-objects','1000000','--seed',seed]
#ser_cmd=['mikado','serialise', '--json-conf',config_file_name,'-nsa','-p',threads,'--max-objects','1000000','--seed',seed]
#print(' '.join(ser_cmd))
pe.execute_command(ser_cmd)

#step 4 pick
pick_cmd=['mikado','pick','--json-conf',config_file_name,'--procs',threads,'--shm','--mode',mode,'--seed',seed]
#print(' '.join(pick_cmd))
pe.execute_command(pick_cmd)

#step5 extract fasta sequences
#ex_prots_cmd=['gffread','mikado.loci.gff3','-g',genome,'-x','mikado.loci.cds.fasta','-y','mikado.loci.pep.fasta']
#ex_cdna_cmd=['gffread','mikado.loci.gff3','-g',genome,'-w','mikado.loci.cdna.fasta']
#pe.execute_command(ex_prots_cmd)
#pe.execute_command(ex_cdna_cmd)

#step6 compare with reference
#runmikado compare
#mikado compare -r $GTF -p mikado.loci.gff3 -l mik_compare.log
#comp_cmd=['mikado','compare','-r',gtf,'-p','mikado.loci.gff3','-l','mik_compare.log']
#pe.execute_command(comp_cmd)

#convert gff3 to gtf
outgtf='mikado.loci.gtf'
gtfcmd=['gffread','mikado.loci.gff3','-T','-o',outgtf]
pe.execute_command(gtfcmd)




