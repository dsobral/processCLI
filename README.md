# processCLI

Run several commands in parallel, ideal for paired-reads (bioinformatics).
It automate several command lines based on several files to be processed. You can make the output of a command the input of the next one.

## How to install

```
$ git clone https://github.com/monsanto-pinheiro/processCLI.git
$ chmod a+x processCLI
```

## How to use

First you need to create a configuration file to define several information. You can copy a template from `example_config\config.txt`.

Edit your configuration file and there are two main sections: i) definitions; ii) commands.
 
### Definitions

Definitions that you can adjust in your configuration file:

	* processors=   -> Process commands in parallel, only Threading mode;

	* queue_name=   -> Set queue name if you want to submit the commands to SGE, only SGE mode;
	* SGE_threads=  -> Set number of cores requested for SGE, default is 1. Activate SGE tag #$ -pe smp <cores requested>", only SGE mode;
	
	* extension_1=  -> extensions of files to look;
	* extension_2=  -> extensions of files to look;
	
	* output_path=  -> global path where the data is going to be saved;
	
	* confirm_after_collect_data=  -> Set True to human confirmation after collecting all the data, otherwise does not stop;
	* log_file=  	  -> log file name;
	
	* cmd=  		  -> commands to run, can be more than one, you can have more than one. One per line;
	
	* InputDirectories -> at the end you need to define the paths where the data is; 
	
Variables that you can set in commands `cmd`:

	* FILE1	 -> reads_R1.fastq.gz/reads_R1.fastq/reads_R1.fasta.gz/reads_R1.fasta 
	* FILE2	 -> reads_R2.fastq.gz/reads_R2.fastq/reads_R2.fasta.gz/reads_R2.fasta

	* FILE1_CHANGED -> GSE96700_GSM2538511/reads_R1.fastq.gz  ->  GSE96700_GSM2538511/GSE96700_GSM2538511_R1.fastq.gz 
	* FILE2_CHANGED -> GSE96700_GSM2538511/reads_R2.fastq.gz  ->  GSE96700_GSM2538511/GSE96700_GSM2538511_R2.fastq.gz
			OR		If not identify any _R1.<extension> in directory start looking for files ended with (fastq.gz, fastq, fasta.gz or fasta) 

			1)  FILE1	-> reads.fastq.gz/reads.fastq/reads.fasta.gz/reads.fasta

	* PREFIX_FILES_OUT -> create a prefix of input files, that you can use to construct the command lie;
	* OUT_FOLDER -> <output_path> variable

	* TEMP variables -> you can create temporary files as you want.
					 only need to start with "TEMPORARY_" word. It is going to create a file where the data is going to be saved. 
					 and at the end it's is going to be remove automatically.
					 Ex: TEMPORARY_a, TEMPORARY_b, TEMPORARY_c
	* INDEX_PROCESS -> Number of set of pair of files/file to process, Ordinal Order.


Examples of configuration file with several `cmd` lines:

```
$ more my_config.txt

##### IMPORTANT
## avoid spaces in the description of the identities: 
## like this "cmd = my commad"
## instead use in this form "cmd=my commad"

####

### number of threads available to run the files
### don't put more than the processors available in your machine
## IMPORTANT, the command line can have threadings to, so need to limit the number of threadings here.
processors=6

#######################
### if you want to run all in SGE enviroment set a queue name, like -ibimed-single.q-
#queue_name=ibimed-single.q
## default cores to run in cluster, if more than 1 activate "#$ -pe smp <cores requested>", ibimed-nodes.q
## The queue must be configured with "smp", like "pe_list     make smp"
#SGE_cores_requested=4

#######################
## extensions to look. It can be empty. If empty look for the regular fastq files out by illumina
## You can put value only on "extension_1=" like ".txt". It's going to process all the files ended with ".txt" and the file names are going to appear in FILE1 variable
## You you want to activate both variables, FILE1 and FILE2, you can put like:
##  "extension_1=_1P.fastq" and "extension_2=_2P.fastq"
extension_1=_1P_trim.fastq.gz
extension_2=_2P_trim.fastq.gz

## If the file/s are inside a folder data/GSE96700_GSM2538511/Neocortex_Diestrus2.fa.gz
##	the name is going to be replaced by  '<output_path>/GSE96700_GSM2538511/GSE96700_GSM2538511.fa.gz
###  replace files names by folder name
###  default is FALSE
replace_file_name_by_folder_name=False


### If true need human confirmation after collecting all the data
### Set this to false if is used in a pipeline
confirm_after_collect_data=yes


### global path where the data is going to be saved
output_path=4_results_bwa

### if all fasta/fastq files are expecting to be paired
##
expecting_all_paired_files=yes

###Log file, where the progression of process are going o be saved
log_file=config_bwa.log

### command line with variables
##
##  	'cmd' can have three variations, first run cmd, then cmd_one_file and for last cmd_two_files
##		At least one 'cmd' need to have something to run.
##			1) cmd -> is a regular command, it's going to run with one or two 'fasta/fastq' files
##			2) cmd_one_file -> only run when has one 'fasta/fastq' file
##			3) cmd_two_files -> only run when has two 'fasta/fastq' files
##
## 		VARIABLES
##		1)	FILE1					-> reads_1P_trim.fastq.gz/reads_1P_trim.fastq/reads_1P_trim.fasta.gz/reads_1P_trim.fasta 
##		2)	FILE2					-> reads_2P_trim.fastq.gz/reads_2P_trim.fastq/reads_2P_trim.fasta.gz/reads_2P_trim.fasta
##		

##		1)	FILE1_CHANGED			-> GSE96700_GSM2538511/reads_R1P_trim.fastq.gz  ->  GSE96700_GSM2538511/GSE96700_GSM2538511_R1P_trim.fastq.gz 
##		2)	FILE2_CHANGED			-> GSE96700_GSM2538511/reads_R2P_trim.fastq.gz  ->  GSE96700_GSM2538511/GSE96700_GSM2538511_R2P_trim.fastq.gz

##
##		OR		If not identify any _R1.<extension> in directory start looking for files ended with (fastq.gz, fastq, fasta.gz or fasta)
##
##		1)  FILE1					-> reads_P_trim.fastq.gz/reads_P_trim.fastq/reads_P_trim.fasta.gz/reads_trim.fasta
##
##		3)	PREFIX_FILES_OUT		-> reads
##		4)	OUT_FOLDER				-> outData/reads/....

##		TEMP variables				-> you can create temporary files as you want
##   								-> only need to start with "TEMPORARY_" word. It is going to create a file where the data is going to be saved. 
									-> at the end it's is going to be remove automatically

### first read the modules
#cmd=module load bwa samtools picard_tools

### process data
cmd=bwa mem -t 8 /home/databases/references/yeast/S288C/pipeline/S288C_reference_sequence_R64-2-1_20150113.fna FILE1 FILE2 | samtools sort -n - | samtools fixmate -m - OUT_FOLDER/PREFIX_FILES_OUT_fixmate.bam
cmd=samtools sort OUT_FOLDER/PREFIX_FILES_OUT_fixmate.bam | samtools markdup - OUT_FOLDER/PREFIX_FILES_OUT_markdup.bam
cmd=picard_tools.sh AddOrReplaceReadGroups I=OUT_FOLDER/PREFIX_FILES_OUT_markdup.bam O=OUT_FOLDER/PREFIX_FILES_OUT_markdupRG.bam SORT_ORDER=coordinate RGLB=bar RGPL=illumina RGSM=PREFIX_FILES_OUT RGPU=unit1
cmd=picard_tools.sh ValidateSamFile MODE=SUMMARY I=OUT_FOLDER/PREFIX_FILES_OUT_markdupRG.bam IGNORE=MISMATCH_MATE_CIGAR_STRING IGNORE=MATE_CIGAR_STRING_INVALID_PRESENCE > OUT_FOLDER/PREFIX_FILES_OUT_validation.txt
cmd=samtools flagstat OUT_FOLDER/PREFIX_FILES_OUT_markdupRG.bam > OUT_FOLDER/PREFIX_FILES_OUT_flagstat.txt
cmd=samtools idxstats OUT_FOLDER/PREFIX_FILES_OUT_markdupRG.bam > OUT_FOLDER/PREFIX_FILES_OUT_idxstats.txt
cmd=santools index OUT_FOLDER/PREFIX_FILES_OUT_markdupRG.bam
cmd=rm OUT_FOLDER/PREFIX_FILES_OUT_fixmate.bam
cmd=rm OUT_FOLDER/PREFIX_FILES_OUT_markdup.bam


## description of several files that lie in a directory or directories
### read all files and try to find pairs of files
## if not find any pairs try to find only files ended with this extension (fastq.gz, fastq, fasta.gz or fasta) 
InputDirectories
2fastq_trim

$ processCLI -i my_config.txt
```

There are more examples in `example_config` diretory.

## How to run

```
$ processCLI -i your_config_file.txt
```


