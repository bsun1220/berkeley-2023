# Competitor GUI 

This GUI is meant to help you (the competitor) keep track of everyone's positions for Game Euclid. 

## Quickstart

Follow this setup if there are $\le 4$ teams in you game. This should be pretty much all games. 

- Install requirements: `!pip install -r requirements_competitor.txt`
- Navigate to `competitor_gui.ipynb`
- Run the first couple cells. You will notice some empty graphs appear. **You only need to run this cell once**
- The cells after are examples of how you should update the graphs.
- To get this update string, please check the #GameE-{mod_name}-{round_num} channel on slack. 

## FAQ

1. I don't see the graphs

Try uncommenting the `%matplotlib notebook` line. Then restart your kernel. The `%matplotlib widget` is for VS Code. 

2. Q: My IDE is asking me to install widgets

Yes, you have to install widgets to have interactive plots. 

3. Any other questions? 

Ask @Sandeep on slack!


