# plantcv-thermal

DOCKER AS A FUNCTION WRITING TO RESULTS FOLDER

## Build environment
'docker compose build'

## Run anaylisis for particular image located in inputdir

'TEMP=<threshold temperature> COORDS=<x, y, w, h of roi> INPUT_FILE=<file directory> docker compose up'

### Example
'TEMP=20.9 COORDS="[50,45,140,125]" INPUT_FILE="./inputdir/B_A0_5.csv" docker compose up'
