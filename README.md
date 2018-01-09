python scripts wrapping around paramiko interactive shell module

the scripts will automate running CLI commands on network devices (cisco, juniper, nokia etc)

files:

	lib/

		read_args.py	#module to process script arguments

		readpass.py		#module to read network devices passwd information from private file
		
		runcmd.py		#module to wrap around paramiko interactive shell module
						
						#key technique here is how to process output buffers
	
	runcmd-auto-7x50.py	#a test scripts to call lib/ modules to automate commands
	
	7x50.cmds			#example commands file to be called for nokia 7750

example:
	
	./runcmd-auto-7x50.py -e edge ABFDBC01RE01 7x50.cmds

