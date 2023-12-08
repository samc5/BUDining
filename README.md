# BUDining
My attempt to improve the BU Dining Hall website for people like myself with dietary restrictions

## Features
- Users can select dietary restrictions and allergens to avoid
- The site returns the daily menu at Warren, West, Marciano, and Granby Dining Halls (sorry Fenway users)
- Daily menu data is stored on Firebase
## Launch
My plan is to eventually host this either on render or a DO droplet but for now, you can clone it and
`python3 app/__init__.py`  
Navigate to `http://127.0.0.1:5000/home` or `http://127.0.0.1:5000/`

Select your dietary restrictions and submit the form.  
Updating Firebase each day takes ~30 seconds, so if you are the first user of the day you will experience a significant delay


## Preview
![](demo.gif)
