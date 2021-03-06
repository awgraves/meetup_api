# Automatic CSV File Generator for Meetup.com API Data

**Python script**

Prompts user for an API key, zipcode, and search radius (0 - 100 miles).  
Stores api key in api_key.txt so user only needs to provide this once.
Exports a csv file containing rows with the following meetup group information:

- name of group
- group url name
- city
- latitude of meetup location
- longitude of meetup location
- meetup category (Social, Tech, Arts, etc.)
- datetime of group creation (automatically adjusted to the local timezone of the meetup location)
- status (active, grace)
- number of current members
- join mode (open, approval)
- number of previous events held
- datetime of most recently past event (adjusted to local time)
- number of 'yes' rsvps for most recently past event


## Getting Started

Once python is properly installed, simply navigate in a terminal to the repo folder and execute the python script with:
```
python meetup_csv_gen.py
```
You will be prompted for your meetup.com API key the first time you run the script. 
(Find your key at this URL: https://secure.meetup.com/meetup_api/key/)

Next, enter a zip code followed by a desired search radius.

If you gave valid inputs you will now have the requested data in a clean csv file located in the same folder as the script.


### Prerequisites

You will need the following python libraries and modules installed to run the script:

```
requests
pandas
json
datetime
time
```


### Installing

I highly recommend the [ANACONDA distribution](https://www.anaconda.com/distribution/) of python. It contains everything you will need.


## Built With

* [jupyterlab](http://jupyterlab-tutorial.readthedocs.io/en/latest/getting_started/overview.html) - Very handy tool for creating and testing scripts


## Author

* **Andrew Graves** - [awgraves](https://github.com/awgraves)


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* [dataquest.io](https://www.dataquest.io/) My main study resource for data science
* [PurpleBooth](https://github.com/purplebooth) Thanks for the readme template

