# Automatic CSV File Generator for Meetup.com Data

**Python script**

Prompts user for an API key, zipcode, and search radius (0 - 100 miles).  
Stores api key in api_key.txt so user only needs to provide this once.
Exports a csv file containing rows with the following meetup group information:

- name of group
- group id
- city
- latitude of meetup location
- longitude of meetup location
- meetup category (Social, Tech, Arts, etc.)
- datetime of group creation
- status (active, grace)
- number of current members
- join mode (open, approval)
- number of previous events held
- datetime of most recently past event
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

I highly recommend the ANACONDA distro that already comes with everything you need to run this script.

```
https://www.anaconda.com/what-is-anaconda/
```


## Built With

* [jupyterlab](http://jupyterlab-tutorial.readthedocs.io/en/latest/getting_started/overview.html) - Very handy tool for creating and testing scripts


## Author

* **Andrew Graves** - [awgraves](https://github.com/awgraves)


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* [dataquest.io](https://www.dataquest.io/) My main data science self-study resource
* [PurpleBooth](https://github.com/purplebooth) For the readme template

