# Langtons Ant
## Usage

launch script in src folder:

`python src/langtons_ant.py`

Scripts accepts these parameters:
- **x** - start position for the x point in the initial matrix. Accept: **0** or **1** values. Default 0
- **y** - start position for the y point in the initial matrix. Accept: **0** or **1** values. Default 0
- **direction** - start direction for the ant. Accept: **up**,  **right**, **down**, **left**. Default "right"
- **iterations**: how many moves ant must to do

Example with all parameters:

`python src/langtons_ant.py -iterations=100 -x=1 -y=1 -direction=up`

Note: 
- **tested with python 3.8**.
- _os.system('clear')_ command will not work in Windows
- no validation made, so be carefull with parameters

## Testing
There are no unittests due to lack of time