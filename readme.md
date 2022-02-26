Instructions

 - Clone the repository: `git clone https://github.com/cxor/dtnSimulator.git`
 - Enter into the project directory: `cd dtnSimulator`
 - Source the fish shell script: `source dots.fish`
 - Enjoy the simulation: `dots --run`
 - It is possible to specify a text file with simulation parameters, in order to avoid to manually describe the simulation details using the commandline; by default, if nothing is specified, the file "parameters.txt" will be used: `dots --run <custom_text_file>`
 - For a runtime detailed log of the simulation, use: `dots --run --verbose`
 - It is also possible to add plots of the resulting simulation; just use: `dots --run --plot`
 - All the commands above can be used together: `dots --run --plot --verbose`