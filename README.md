# Carcasonne
Since more then 15 years I wanted to create a complete rectangle out of tiles based of the germen board game called **Carcasonne** after the french city with its famous castle.

This project should end up helping me in succeeding my goal.
## Install
Create a new environment

```commandline
conda create --name carcasonne --file requirements.txt
```
activate your env
```commandline
conda activate carcasonne
```
## Tile Classifier
In order to now which tile can connect to which tile in order to full fill the game rules I created a simple classifier which will classify the border of each tile accordingly.
### Create a Dataset
run the annotation tool
```commandline
(carcasonne) python tiles/annotate.py PATH/TO/YOUR/CARCASONNE/TILES/{...}.png
```

### Train a Classifier
```commandline
(carcasonne) python tiles/train.py PATH/TO/YOUR/CARCASONNE/TILES/annotation.json
```