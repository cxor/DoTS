function dots --description 'Fish function wrapper for the DoTS simulator'
    set --local options "r/run" "p/plot" "v/verbose"
	set --local run_input "parameters.txt"
    argparse --name="dots" $options -- $argv > /dev/null 2>&1
    if set --query _flag_run
		test -f "$argv"; and set run_input $argv
		set --query _flag_plot; and set plot "--plot"
		set --query _flag_verbose; and set verbose "--verbose"
		python3 dots.py $plot $verbose (cat $run_input | \
			while read --local line; \
				echo "--$line" | string trim | \
				string split -- \t | string match --regex ".+" | \
				string trim; end); return 
	end; python3 src/core.py $argv
end
