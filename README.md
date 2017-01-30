# Configuration synchronizer to consul

The python scripts syncrhonize configuration files to consul with additional transformation:

 * Appending additional files according to the activated profiles
 * execute jinja2 template engine
 * transform key values to other format
 

The source directory should be a specific format:

 * ```configuration``` sub directory contains the configuration files
 * ```profiles.txt``` contains the activated profiles
 * ```profiles``` sub directory contains the available profiles
 * ```transformation``` contains the activa transformation (pattern transformation)
 
 Example configuration: the consul directory of the http://github.com/elek/bigdata-docker/
