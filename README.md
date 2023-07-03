# Carcasonne
Since more then 15 years I wanted to create a complete rectangle out of tiles based of the germen board game called **Carcasonne** after the french city with its famous castle.

This project should end up helping me in succeeding my goal.

See also [this](https://github.com/tsaglam/Carcassonne) implementation of the game. The repo also offers some example [tiles](https://github.com/tsaglam/Carcassonne/tree/master/src/main/resources/tiles).
## Install
Create a new environment

```commandline
conda create --name carcasonne --file requirements.txt
```
activate your env
```commandline
conda activate carcasonne
```

move to source directoy
```commandline
cd src
```
## Tile Classifier
In order to know which tile can connect to which tile in order to full fill the game rules I created a simple classifier which will classify the border of each tile accordingly.
### Create a Dataset
run the annotation tool
```commandline
python tiles/annotate.py PATH/TO/YOUR/CARCASONNE/TILES/{...}.png
```

### Train a Classifier
```commandline
python tiles/train.py PATH/TO/YOUR/CARCASONNE/TILES/annotation.json
```

##