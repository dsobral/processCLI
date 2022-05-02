#!/usr/bin/env python

import os, time
from constants.utils import Util
from datetime import datetime


# http://www.socher.org/index.php/Main/HowToInstallSunGridEngineOnUbuntu
# https://peteris.rocks/blog/sun-grid-engine-installation-on-ubuntu-server/
# http://biohpc.blogspot.pt/2016/10/sge-installation-of-son-of-grid-engine.html ## centos 7
# http://star.mit.edu/cluster/docs/0.93.3/guides/sge.html		### explain who to use SGE

# /usr/share/gridengine/scripts/init_cluster

#  => SGE_ROOT: /var/lib/gridengine
# => SGE_CELL: default
# => Spool directory: /var/spool/gridengine/spooldb
# => Initial manager user: sgeadmin

## logs
# <qmaster_spool_dir>/messages
# <qmaster_spool_dir>/schedd/messages
# <execd_spool_dir>/<hostname>/messages
# <sge_root>/<sge_cell>/common/accounting
# <sge_root>/<sge_cell>/common/statistics

## default configuration
# /etc/default/gridengine
class ProcessSGE(object):
	
	utils = Util()
	
	def __init__(self):
		pass

	###########################################
	###
	###		BEGIN main methods
	###
	###		IMPORTANT
	###			Put qsub in /usr/bin/qsub
	###
	def submitte_job(self, file_name):
		"""
		job submission
		raise exception if something wrong
		"""
		temp_file = self.utils.get_temp_file('qsub_out', ".txt")
		cmd = 'qsub {} > {}'.format(file_name, temp_file)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			if (os.path.exists(temp_file)): os.unlink(temp_file)
			raise Exception("Fail to submit qsub")
		## read output
		vect_out = self.utils.read_text_file(temp_file)
		if (os.path.exists(temp_file)): os.unlink(temp_file)
		b_found = False
		for line in vect_out:
			if (line.find("has been submitted") != -1):
				lst_line = line.split(' ')
				if (len(lst_line) > 4 and self.utils.is_integer(lst_line[2])): return int(lst_line[2])
				return None		## don't rise exception... 
		if (not b_found): raise Exception("\n".join(vect_out))


	def set_script_run_sge(self, out_dir, queue_name, sge_cores_requested, vect_cmd, file_name_out):
		"""
		:param sge_cores_requested cores resquested, default 1
		create the script to run SGE
		"""
		if (len(vect_cmd) == 0): return None
		
		with open(file_name_out, 'w') as handleSGE:
			handleSGE.write("#!/bin/bash\n")
			handleSGE.write("#$ -V\n")	# Specifies  that  all  environment  variables active
										# within the qsub utility be exported to the context of the job.
			handleSGE.write("#$ -S /bin/bash\n") 	# interpreting shell
			if sge_cores_requested > 1:
				handleSGE.write("#$ -pe smp {}\n".format(sge_cores_requested))	# cores requested to the queue
			handleSGE.write("#$ -j y\n")	# merge the standard error with standard output
			handleSGE.write("#$ -cwd\n")	# execute the job for the current work directory
			if (len(queue_name) > 0): handleSGE.write("#$ -q {}\n".format(queue_name))	# queue name
			if len(out_dir) > 0: handleSGE.write("#$ -o {}\n".format(out_dir))		# out path file
			for cline in vect_cmd: handleSGE.write("\n" + cline)
		return file_name_out
	
	def __get_sge_process__(self):
		"""
		#Job status - one of
	
		### test if all jobs submitted to the SGE are finish
		## return 0, if is end
		## return -1, error
		## other value, keeping running
		## also returns a vector with jobId already finish
		
		#	* d(eletion)
		#	* E(rror)
		#	* h(old)
		#	* r(unning)
		#	* R(estarted)
		#	* s(uspended),
		#	* S(uspended)
		#	* t(ransfering)
		#	* T(hreshold)
		#	* w(aiting)
		"""
		tagsSGERunning = ('r', 't')
		tagsSGEWaiting = ('hqw', 'qw', 'w')
		# test with qstat
		file_result = self.utils.get_temp_file('sge_stat', '.txt')
		cline = 'qstat > %s' % (file_result)
		os.system(cline)
			
		## read the FILE
		with open(file_result) as handle_result:
			vectRunning =[]
			vectWait =[]
			for line in handle_result:
				# pass header and other things
				if (line.find("job-ID") != -1 or len(line) < 3 or line.find("---") == 0): continue
				if (len(line.split()) > 0):
					## jobid is running
					if (line.split()[4] in tagsSGERunning): vectRunning.append(line.split()[0])
					elif (line.split()[4] in tagsSGEWaiting): vectWait.append(line.split()[0])
		
		## remove file
		if (os.path.exists(file_result)): os.unlink(file_result)
		return (vectRunning, vectWait)

	def get_status_process(self, n_SGE_id):
		(vectRunning, vectWait) = self.__get_sge_process__()
		if (str(n_SGE_id) in vectRunning): return self.SGE_JOB_ID_PROCESSING
		if (str(n_SGE_id) in vectWait): return self.SGE_JOB_ID_QUEUE
		return self.SGE_JOB_ID_FINISH

	def is_finished(self, n_SGE_id):
		"""
		is it finished
		"""
		return self.get_status_process(n_SGE_id) == self.SGE_JOB_ID_FINISH

	def exists_taks_running(self):
		"""
		test if there any tasks running...
		"""
		file_result = self.utils.get_temp_file('sge_stat', '.txt')
		cline = 'qstat > %s' % (file_result)
		os.system(cline)
		## read the FILE
		with open(file_result) as handle_result:
			for line in handle_result:
				if (line.find("job-ID") != -1 or len(line) < 3 or line.find("---") == 0): continue
				if len(line.strip()) > 0: 
					if (os.path.exists(file_result)): os.unlink(file_result)
					return True
		if (os.path.exists(file_result)): os.unlink(file_result)
		return False
	
	def wait_until_finished(self, vect_sge_ids):
		"""
		wait till all end
		if len(vect_sge_ids) == 0 wait till all are finished, doesn't matter the ID
		"""
		if (len(vect_sge_ids) == 0):
			while self.exists_taks_running():
				print("=" * 50 + "\n  waiting for sge\n" + str(datetime.now()))
				time.sleep(5)	## wais 5 seconds
		else:
			while len(vect_sge_ids) > 0:
				print("=" * 50)
				print("   wait for these ids: {}".format(";".join([str(_) for _ in vect_sge_ids])))
				vect_remove = []
				for sge_id in vect_sge_ids:
					if self.is_finished(sge_id): vect_remove.append(sge_id)
				
				### remove sge
				for sge_id in vect_remove: vect_sge_ids.remove(sge_id)
				
				print("=" * 50)
				if (len(vect_sge_ids) > 0): time.sleep(5)	## wais 5 seconds

	#### END MAIN files
	#############
	#############

