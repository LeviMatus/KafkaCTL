
# PyFluent

## Requirements

  - Python 3.X
  - Pip for Python 3.X
    + sudo apt-get install python3-pip
    
## Setup
  - Before running, ensure the following:
    + the `topics-to-configure.txt` and `registered-schemas.txt` files have the entities that you wish to alter.
    Check the appropriate schema registry and Kafka topics (`kafka-topics --zookeeper localhost --list`) to ensure
    be sure.
    + execute `pip3 install -r requirements.txt`

A quick CLI that wraps confluent's multiple Kafka related CLIs.

## Quick Help

using `python3 pyfluent.py -h` will give you a list of possible arguments.

## Usage
PyFluent is a Python CLI meant to wrap the multiple Kafka CLI tools (Kafka Tools, Kafka-Topics, Kafka-Configs)
so that we can take the redundant copy-pasta and lookup work out of development.

Using the tool is pretty simple, although verbose. The following is how one would add a retention.ms period of 1000 to a list
of topics in the `topics-to-configure.txt` file.

`python3 pyfluent.py --host zookeeper --env QA --retention_ms set 1000`

This is extensible to multiple config options as well!

`python3 pyfluent.py --host zookeeper --env QA --retention_ms set 1000 --cleanup_policy set compact --compaction_time delete`

This configures three configurations per topic! Its also clear what we're doing for each configuration.

The format goes like this:

  + `--host` 
    - The host type we will select, either `zookeeper` or `schema-registry`
  + `--env`
    - The env at which to find the host.  Choose one of `DEV, QA, or PROD`
    
  + configuration options
    - `--delete` : deletes topics from zookeeper despite whatever other options you provide
    - `--retention_ms` : takes up to 2 args. All configs follow this format.
      + `--retention_ms set|delete var` : add will set/add a config while delete will delete a config. Using
      `--retention_ms set` requires you to specify an additional parameter, `var`, so that you have something like
      `--retention_ms set 1000` where 1000 is the value to set retention to.
      Delete requires no other vars (it will not break if you do, however, they will be ignored).
      
 #### Schema-Registry
 To alter state stores in the Schema Registry, make sure that the file `registered-schemas.txt` contains a list of state
 stores in the format of `{topic}-value` that you wish to alter.
 
 The script will issue a URL request to following the  conventions of the 
 [Kafka API](https://docs.confluent.io/current/schema-registry/docs/api.html#post--subjects-(string-)) in order to issue
 change requests. **This means that you can run alterations for local, QA, and PROD from your desktop**, unlike zookeeper.
 
  #### Zookeeper
  To edit topics on our zookeeper host, you will need to run the script on machine equipped with the Kafka CLIs. The 
  legacy transformer vagrant box or the KC vagrant box will work for this. Alternately, you can SCP the project to the
  QA KC machine (the GNS DE API machine).
  
  To specify which topics you wish to edit, paste them in the `topics-to-configure.txt` file. 
  
  A helpful Kafka-Topics CLI command to find the topics you want to edit: `kafka-topics --zookeeper <host> --list`.