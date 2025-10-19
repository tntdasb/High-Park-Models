import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import plotly.graph_objects as go

def facing_convert(f):
    out=90-f
    if out<0:
        out+=360
    return out/180*math.pi 

inps=('''
0	4	5	189
1	3.9	7	190
2	3.3	6	196
3	3.3	7	186
4	3.2	7	184
5	3.1	6	178
6	3.1	9	184
7	3.2	7	180
7.4	3.24	90	180
7.49	3.24	7	180
8.09	3.3	4	185
9.09	3.7	3	186
9.89	3.94	90	186
9.92	3.94	3	186
10.12	4	4	190
11.12	4.4	4	220
12.12	4.7	8	187
13.02	4.88	90	187
13.12	4.88	8	187
13.22	4.9	4	185
''','''
0	2.5	5	270
1	2.8	7	271
2	2.7	8	285
3	2.4	1	270
4	2.5	7	287
5	2.5	5	290
6	2.5	5	290
7	2.5	3	292
8	2.5	6	290
9	2.6	3	290
10	2.7	5	284
11	2.6	6	285
12	2.7	5	290
13	2.8	5	290
14	2.8	6	290
15	2.8	7	290
16	2.8	6	289
17	2.6	7	285
18	2.6	7	277
19	2.5	10	287
20	2.6	10	279
21	2.5	9	278
22	2.6	10	276
23	2.5	13	278
24	2.4	7	282
25	2.4	10	280
26	2.3	10	271
27	2.3	12	268
28	2.4	7	266
29	2.5	11	260
30	2.4	10	262
31	2.5	10	258
''','''
0	4	5	189
1	3.9	7	190
2	3.3	6	196
3	3.3	7	186
4	3.2	7	184
5	3.1	6	178
6	3.1	9	184
7	3.2	7	180
7.4	3.24	90	180
7.49	3.24	7	180
8.09	3.3	4	185
9.09	3.7	3	186
9.89	3.94	90	186
9.92	3.94	3	186
10.12	4	4	190
11.12	4.4	4	220
12.12	4.7	8	187
13.02	4.88	90	187
13.12	4.88	8	187
13.22	4.9	4	185
13.82	1.2	0	275
16.27	2.5	5	270
17.27	2.8	7	271
18.27	2.7	8	285
19.27	2.4	1	270
20.27	2.5	7	287
21.27	2.5	5	290
22.27	2.5	5	290
23.27	2.5	3	292
24.27	2.5	6	290
25.27	2.6	3	290
26.27	2.7	5	284
27.27	2.6	6	285
28.27	2.7	5	290
29.27	2.8	5	290
30.27	2.8	6	290
31.27	2.8	7	290
32.27	2.8	6	289
33.27	2.6	7	285
34.27	2.6	7	277
35.27	2.5	10	287
36.27	2.6	10	279
37.27	2.5	9	278
38.27	2.6	10	276
39.27	2.5	13	278
40.27	2.4	7	282
41.27	2.4	10	280
42.27	2.3	10	271
43.27	2.3	12	268
44.27	2.4	7	266
45.27	2.5	11	260
46.27	2.4	10	262
47.27	2.5	10	258
''')

choice=1

inp=list(map(float,inps[choice-1].split()))
n=0
data=[]
group=[]
for crow in inp:
    group.append(crow)
    n+=1
    if n==4:
        n=0
        data.append(tuple(group))
        group.clear()

centres=[]
lefts=[]
rights=[]
last=(0,0,0,np.array([0,0,0])) #distance elevation facing coordinates


for row in data:
    dd=row[0]-last[0]
    dho=dd*math.cos(last[1])

    ddv=np.array([dho*math.cos(last[2]), dho*math.sin(last[2]), dd*math.sin(last[1])])

    c=last[3]+ddv

    fac=facing_convert(row[3])
    el=row[2]/180*math.pi

    dls=np.array([-(row[1]/2)*math.sin(fac), (row[1]/2)*math.cos(fac), 0])
    drs=-dls

    last=(row[0], el, fac, c)
    centres.append(c)
    lefts.append(c+dls)
    rights.append(c+drs)

centres=np.vstack(centres)
lefts=np.vstack(lefts)
rights=np.vstack(rights)

cxyz = np.split(centres,3,axis=1)
lxyz=np.split(lefts,3,axis=1)
rxyz=np.split(rights,3,axis=1)


mode=1
if mode==0:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.computed_zorder = False

    pre_pair=np.array([])
    faces=[]
    lines=[]
    for i in range(len(centres)):
        cur_pair=np.vstack((lefts[i],rights[i]))
        lines.append(cur_pair.copy())
        if pre_pair.size>0:
            faces.append(np.vstack((pre_pair.copy(),np.flipud(cur_pair))))
        pre_pair=cur_pair.copy()

    ax.add_collection3d(Poly3DCollection(faces, alpha=0.2, facecolor='yellow', zorder=1))
    ax.add_collection3d(Line3DCollection(lines, colors='orange', linewidths=1, zorder=2))

    ax.plot(*lxyz, color='green', linewidth=1,zorder=3)

    ax.plot(*rxyz, color='green', linewidth=1,zorder=3)

    ax.plot(*cxyz, color='red', linewidth=2,zorder=4)
    ax.scatter(*cxyz, color='blue', s=15,zorder=5)

    plt.axis('scaled')

    ax.set_xlabel('East')
    ax.set_ylabel('North')
    ax.set_zlabel('Up')

    plt.show()
else:
    fig = go.Figure()

    pre_pair=np.array([])
    lines=[]
    for i in range(len(centres)):
        cur_pair=np.vstack((lefts[i],rights[i]))
        lines.append(np.vstack((cur_pair,[None]*3)))
        if pre_pair.size>0:
            face=np.vstack((pre_pair,np.flipud(cur_pair)))      
            fig.add_trace(go.Mesh3d(
                x=face[:,0], y=face[:,1], z=face[:,2],
                i=[0, 0],j=[1, 2],k=[2, 3],
                color="lime",
                opacity=0.2,
                name=f"Face {i}",
                flatshading=True
            ))
        pre_pair=cur_pair.copy()

    lines=np.vstack(lines)
    fig.add_trace(go.Scatter3d(
        x=lines[:,0],y=lines[:,1],z=lines[:,2],
        mode='lines',
        line=dict(width=3, color='orange'),
        name=f'Perpendicular Lines'
    ))

    fig.add_trace(go.Scatter3d(
        x=lefts[:,0],y=lefts[:,1],z=lefts[:,2],
        mode='lines',
        line=dict(width=3, color='purple'),
        name=f'Left Boundary'
    ))

    fig.add_trace(go.Scatter3d(
        x=rights[:,0],y=rights[:,1],z=rights[:,2],
        mode='lines',
        line=dict(width=3, color='purple'),
        name=f'Right Boundary'
    ))

    fig.add_trace(go.Scatter3d(
        x=centres[:,0],y=centres[:,1],z=centres[:,2],
        mode='lines+markers',
        line=dict(width=6, color='red'),
        marker=dict(size=6, color='blue'),
        name=f'Centre Line'
    ))

    
    #fig.update_layout(scene=dict(xaxis_title='East (m)',yaxis_title='North (m)',zaxis_title='Up (m)',aspectmode='data'),title_text=f"Combination of Section 1&2")
    fig.update_layout(scene=dict(xaxis_title='East (m)',yaxis_title='North (m)',zaxis_title='Up (m)',aspectmode='data'),title_text=f"Section {choice}")
    
    out=""
    if out=="w":
        fig.write_html(f"models/model{choice}.html")
        #fig.write_html(f"models/combined_model.html")
    else:
        fig.show()
    
