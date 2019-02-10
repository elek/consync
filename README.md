# !Archived!

__This project is archived. Originally it was part of the https://github.com/flokkr project, but it's no longer maintained.__

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

# Configuration synchronizer to consul

The golang script to syncrhonize configuration files to consul with additional transformation:

 * Appending additional files according to the activated profiles (wip)
 * execute go template engine
 * transform key values to other format
 

The source directory should have a specific structure.

 * ```configuration``` sub directory contains the configuration files
 * ```profiles``` sub directory contains the available profiles
 
 Example configuration: the consul directory of the https://github.com/flokkr/runtime-compose/ and https://github.com/flokkr/configuration
