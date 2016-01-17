SurgeTrends is a Python script to collect and plot Uber surge multipliers as a function of time.

Instructions:
* Register for an API key with Uber: [https://developer.uber.com/](https://developer.uber.com/)
* Create a file called `config.py` with a single line specifying your server token ```server_token="string you got when registering with Uber's API"```
* Define a set of location endpoints you'd like you use for your trips in the locations dictionary in the `surge.py` file
* There is example code for either hard-coding trips between selected endpoints or generating all possible trips between your defined endpoints. _Note that Uber limits you to 1000 API calls per hour so keep this in mind when specifying your trips and time between queries._
* Choose an output file to store your data in (look for the `output_file` variable)
* Run the code via `python surge.py`
* Look through the iPython notebook file `make_plots.ipynb` for examples on how to plot the results. Hopefully it's documented well enough to follow.

For running the dashboard (currently super-basic):
* You'll need to have a data file already generated from `surge.py`, e.g. called `data.txt`
* Next, convert the text file to serialized json format with `python txt_to_json.py` (you'll need to open the python script to edit the file it opens)
* Once you have a `data.json` file, edit `dashboard.html` so it knows to open it
* To view the webpage locally, you need to run a local webserver, e.g. with `python -m SimpleHTTPServer 8001`
* Open your web browser and type in `http://localhost:8001/` which will show the contents of the folder than the webserver was started in
* Navigate to your SurgeTrends folder and open up `dashboard.html` - you should see a plot of your data