import matplotlib.pyplot as plt
import plotly.offline as pyo
import pandas as pd
import plotly.graph_objects as go
from PIL import Image


def convert_to_percentile(a, b):
    return a*100/b


filename1 = str(input())
filename2 = str(input())

#C:\Users\jakub\Downloads\forcedecks-test-export-10_11_2022.csv
#C:\Users\jakub\Downloads\forcedecks-test-export-09_11_2022-4.csv

data1 = pd.read_csv(fr'{filename1}')
data2 = pd.read_csv(fr'{filename2}')
print(data1)
print(data2)

df1 = pd.DataFrame(data1, columns=['RSI-modified [m/s] ', 'Jump Height (Flight Time) [cm] ',
                                   'Eccentric Peak Power / BM [W/kg] ', 'Peak Power / BM [W/kg] ',
                                   'Eccentric Duration [ms] ', 'Eccentric Deceleration Impulse [N s] ',
                                   'Flight Time:Contraction Time ', 'Concentric Peak Force [N] '])
df2 = pd.DataFrame(data2, columns=['Peak Vertical Force [N] ', 'Peak Vertical Force / BM [N/kg] ',
                                   'Start Time to Peak Force [s] ', 'Peak Vertical Force [N] (Asym) (%)'])
print(df1)
print(df2)

pom = df1.values.tolist()
clientJumpData = [pom[0][0], pom[0][1], pom[0][2], pom[0][3], pom[0][4], pom[0][5], pom[0][6], pom[0][7]]

pom = df2.values.tolist()

imtpData = [pom[0][0], pom[0][1], pom[0][2], pom[0][3]]

print(clientJumpData)
print(imtpData)

dsi = clientJumpData[3]

labels1 = ['RSI-modified [m/s]', 'jump height [cm]', 'Eccentric Peak Power', 'Peak Power (Kg)',
           'Eccentric Duraction', 'Eccentric Decelaration Impulse (N/s)', 'FT:CT Ratio', 'Concentric Peak Force [N] ']
labels2 = ['Peak Vertical Force [N] ', 'Peak Vertical Force / BM [N/kg] ',
           'Start Time to Peak Force [s] ', 'Peak Vertical Force [N] (Asym) (%)']

collegeComparisonJumpData = [0.869, 61, 37, 77, 0.75*1000, 188.6, 1.06]

percentileClient = [0, 0, 0, 0, 0, 0, 0]
percentileCollegeAthlete = [100, 100, 100, 100, 100, 100, 100]

for i in range(0, len(clientJumpData)-1):
    percentileClient[i] = convert_to_percentile(clientJumpData[i], collegeComparisonJumpData[i])

fig = go.Figure(
    data=[
        go.Scatterpolar(r=percentileClient, theta=labels1, fill='toself', name='Daniel Barbosa'),
        go.Scatterpolar(r=percentileCollegeAthlete, theta=labels1, fill='toself', name='Reference'),
    ],
    layout=go.Layout(
        title=go.layout.Title(text='Athelete CMJ test'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True
    )
)

pyo.plot(fig)
fig.write_image("fig1.png")

dsiDf = [clientJumpData[7]/imtpData[0]]
print(dsiDf)
athlete = [input()]

fig, ax = plt.subplots()
ax.bar(athlete, dsiDf, width=0.1, color='pink')
ax.set_xlim(0, 0)
plt.axhline(0.6, color='r', linestyle='-')
plt.axhline(0.8, color='r', linestyle='-')

plt.savefig('dsi.png')
images = [Image.open(x) for x in ['dsi.png', 'fig1.png']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
    new_im.paste(im, (x_offset, 0))
    x_offset += im.size[0]

new_im.save('new1.png')