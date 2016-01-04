SurgeTrends is a pyton script to collect and plot Uber surge multipliers as a function of time.

Instructions:
* Register for an API key with Uber: [https://developer.uber.com/](https://developer.uber.com/)
* Create a file called `config.py` with a single line specifying your server token: `server_token="string you got when registering with Uber's API"`
* Define a set of location endpoints you'd like you use for your trips in the locations dictionary in the `surge.py` file
* There is example code for either hard-coding trips between selected endpoints or generating all possible trips between your defined endpoints. Note that Uber limits you to 1000 API calls per hour so keep this in mind when specifying your trips and time between queries.
* Choose an output file to store your data in (look for the `output_file` variable)
* Run the code via `python surge.py`
* Look through the iPython notebook file `make_plots.ipynb` for examples on how to plot the results. Hopefully it's documented well enough to follow.