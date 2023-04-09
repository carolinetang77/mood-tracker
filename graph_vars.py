import numpy as np
import plotly.graph_objects as go

# mood labels
graph_text = [
    "I guess<br>that's it", "My mom<br>would be sad",
    "It's the kind<br>of tired that<br>sleep won't<br>fix...", "I hate<br>women",
    "You've got to<br>be fucking<br>kidding me", "I am a<br>genuine<br>threat<br>to society",
    "My dog<br>wouldn't<br>understand", "It's so<br>over", 
    "It's just<br>one of<br>those days...", "I don't think<br>we making it<br>out of the<br>hood bro", 
    "FUCK", "(In Minecraft)", 
    "One day<br>something<br>will kill me", "This time<br>I'm really<br>gonna do it", 
    "yeah bro,<br>I just need<br>some sleep", "*Internal<br>screaming*", 
    "Fuck it<br>we ball", "Goblin mode", 
    "Comfortably<br>numb", "Another day,<br>another dollar", 
    "It really do<br>be like that<br>sometimes", "It is<br>what it is",
    "Bitches love<br>my mustache", "Silly goose",
    "aight", "cool",
    "Straight<br>chillin", "We're gonna<br>make it bro",
    "We're so back", "Let's<br>gooooooo",
    "I'm<br>bing chillin", "We vibin",
    "neat", "Modelo time",
    "We're so<br>fucking back", "LETS<br>FUCKING<br>GOOOOO"
]

# mood colors
graph_colors = [
    ["#4B89C2", "#6178A5", "#786788", "#8E576A", "#A5464D", "#BB3530"], # col 1
    ["#5193AE", "#688695", "#80797C", "#976D62", "#AF6049", "#C65330"], # col 2
    ["#579D9A", "#6F9485", "#888B70", "#A0825A", "#B97945", "#D17030"], # col 3
    ["#5CA686", "#76A175", "#909C63", "#A99852", "#C39340", "#DD8E2F"], # col 4
    ["#62B072", "#7DAF65", "#98AE57", "#B2AD4A", "#CDAC3C", "#E8AB2F"], # col 5
    ["#68BA5E", "#84BD55", "#A0C04B", "#BBC342", "#D7C638", "#F3C92F"] # col 6
]

# Create base figure
fig = go.Figure()

fig.update_xaxes(
    range=[0,6], 
    fixedrange = True,
    showticklabels = True,
    title = dict(text = 'Unpleasant <-> Pleasant')
)
fig.update_yaxes(
    range=[0,6], 
    fixedrange = True,
    showticklabels = True,
    title = dict(text = 'Low Energy <-> High Energy')
)

for i in range(36):
    fig.add_shape(
        type="rect",
        x0 = i // 6, y0 = i % 6, x1 = (i // 6) + 1, y1 = (i % 6) + 1,
        label = dict(text = graph_text[i], font_color='black', font_size=12),
        fillcolor = graph_colors[i//6][i % 6],
        layer="below"
    )

GS=60
fig.add_trace(go.Scatter(
    x=np.repeat(np.linspace(0, 6, GS), GS), 
    y=np.tile(np.linspace(0, 6, GS), GS),
    marker_color="rgba(0,0,0,0)"
))

fig.update_layout(
    width = 600, 
    height = 600,
    margin = dict(t = 0, b = 10, l = 10, r = 10)
)
