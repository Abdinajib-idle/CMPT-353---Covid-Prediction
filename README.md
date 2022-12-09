# 353-Project-Covid-Predictions

# todo: add intro from google docs here

## Set up
Install the needed packages by opening a terminal and running the following command.
```bash
pip install -r requirements.txt
```
## Generate Graphs
Run the `data_processing_monthly.py` script to process data files.
Next, run the `visualization.py` script to further process the data and generate graphs.
There are 8 graphs that can be generated. To ensure the graphs are generated properly, ensure you do not generate
the first 3 graphs at the same time (cases-by-time, death-cases-by-time-scatter,vaccination-by-time). Please comment out 
2 of the 3 before proceeding. The rest of the graphs can be generated as normal.
