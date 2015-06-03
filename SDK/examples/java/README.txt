The Java examples in this directory were built and tested using the following tools:
- Java SE 6
- Apache Axis 1.4
- Apache Ant 1.6

In order to build and run the examples you will need to download and install all these tools.

Building the Java examples
==========================
The build.xml file in this directory is used to compile the examples using Apache Ant.

1. Set the JAVA_HOME environment variable to path where Java is installed

2. Execute the "compile_code" target in build.xml using the command:

    <ANT_HOME>/bin/ant -Daxis.home=<AXIS_HOME> compile_code
    
		<ANT_HOME> is the path where Apache Ant is installed
		<AXIS_HOME> is the path where Apache Axis is installed
	
	The compile_code target will generate the Java stubs from the WSDL and XSD files and
	compile the generated and example files.
	
Running the Java examples
==========================
The build.xml file also has targets to run the examples using Apache Ant.

1. Set the JAVA_HOME environment variable to path where Java is installed

2. Execute the "run_xxx" targets in build.xml using the command:

    <ANT_HOME>/bin/ant -Daxis.home=<AXIS_HOME> <run_target> -Dswitch=<switch> -Dusername=<username> -Dpassword=<password>
    
		<ANT_HOME> is the path where Apache Ant is installed
		<AXIS_HOME> is the path where Apache Axis is installed
		<switch> is the switch to execute the API on
		<username> is the login to access the switch
		<password> is the password to access the switch
	
For example, to run the ExecCLIExample program use the command:
	
	<ANT_HOME>/bin/ant -Daxis.home=<AXIS_HOME> run_exec_cli_example -Dswitch=<switch> -Dusername=<username> -Dpassword=<password>
	 
The available run targets are:
	run_create_example - runs the CreateExample
	run_get_one_example - runs the GetOneExample
	run_get_all_example - runs the GetAllExample
	run_get_with_paging_example - runs the GetWithPagingExample
	run_delete_example - runs the DeleteExample
	run_set_example - runs the SetExample
	run_exec_cli_example - runs the ExecCLIExample
	run_port_utilization_example - runs the PortUtilizationExample
	run_apply_acl_example - runs the ApplyACLExample
