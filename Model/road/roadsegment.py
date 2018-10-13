import statistics
from math import sqrt, degrees
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


datalist = dict()
durationlist = dict()
directlist = dict()
start_velocity=[]
end_velocity=[]

start_velocity_list={}
end_velocity_list={}

start_velocity_label =[]
end_velocity_label =[]

final = []
f = open("Road Segment Data.csv")
i = 0
for lines in f:
     i=i+1
     line = lines.strip().split(",")
     if float(line[5])!=1 and float(line[6]) != 1:
          start_velocity.append(float(line[5]))
          end_velocity.append(float(line[6]))
          start_point = (round(float(line[12]),2),round(float(line[13]),2),round(float(line[14]),2))
          end_point = (round(float(line[15]),2),round(float(line[16]),2),round(float(line[17]),2))
          coord = (start_point,end_point)
          #print(coord)
          duration = float(line[9])
          if coord not in datalist.keys():
               datalist[coord] = [float(line[7]),float(line[10]),float(line[11])]
               #print(datalist.__len__())
          if coord not in durationlist.keys():
               durationlist[coord]=[]
               durationlist[coord].append(duration)
          else:
               durationlist[coord].append(duration)
          #Ignore "1"
          if coord not in start_velocity_list.keys():
               start_velocity_list[coord]=[]
               start_velocity_list[coord].append(float(line[5]))
          else:
               start_velocity_list[coord].append(float(line[5]))
          if coord not in end_velocity_list.keys():
               end_velocity_list[coord]=[]
               end_velocity_list[coord].append(float(line[6]))
          else:
               end_velocity_list[coord].append(float(line[6]))



print("Total Lines: "+ str(i))
print("Total segment in datalist: "+ str(datalist.__len__()))
print("Total segment in duration: "+ str(durationlist.__len__()))


#Calculate STD of Duration
for dur in durationlist.keys():
     if (durationlist[dur]).__len__() > 1:
          #print("ori:"+str(durationlist[dur]))
          std = statistics.stdev(durationlist[dur])
          avg = statistics.mean(durationlist[dur])
          indicator = std*1.96
          #print("idc: "+str(indicator))
          #print("avg: " + str(avg))
          newlist = []
          for e in durationlist[dur]:
               if abs((e-avg))<=indicator:
                  newlist.append(e)
          durationlist[dur]=newlist
          durationlist[dur] = round(statistics.mean(newlist),2)
          #print("new:"+str(durationlist[dur]))
     else:
          durationlist[dur] = durationlist[dur][0]
     #print("\n")
          #print( str(dur) + "  : " + str(durationlist[dur]))


#Calculate Direct of Coord
"""
for c in datalist.keys():
     start_x = c[0][0]
     start_y = c[0][1]
     start_z = c[0][2]
     end_x = c[1][0]
     end_y = c[1][1]
     end_z = c[1][2]
     d_x = end_x - start_x
     d_y = end_y - start_y
     d_z = end_z - start_z
     cos = d_z/sqrt((d_x)**2+(d_y)**2+(d_z)**2)
     ang = degrees(cos)
     directlist[c] = ang
"""
#for k,v in sorted(durationlist.items(), key = itemgetter(1)):
     #print (k,v)
#print("")


#Clean Start length
for v in start_velocity_list.keys():
     if (start_velocity_list[v]).__len__() > 1:
          avg = statistics.mean(start_velocity_list[v])
          start_velocity_list[v]=avg
     else:
          start_velocity_list[v] = start_velocity_list[v][0]
     # --------START--------------------
     if start_velocity_list[v] >= 25:  # UP
          start_velocity_label.append(int(0))
     elif start_velocity_list[v] <= 5:  # DOWN
          start_velocity_label.append(int(2))
     else:  # FLAT
          start_velocity_label.append(int(1))

# Clean End length
for v in end_velocity_list.keys():
     if (end_velocity_list[v]).__len__() > 1:
          avg = statistics.mean(end_velocity_list[v])
          end_velocity_list[v] = avg
     else:
          end_velocity_list[v] = end_velocity_list[v][0]
     # --------END--------------------
     if end_velocity_list[v] >= 25: #UP
          end_velocity_label.append(int(0))
     elif end_velocity_list[v] <= 5: #DOWN
          end_velocity_label.append(int(2))
     else: #FLAT
          end_velocity_label.append(int(1))

print("START LABEL: "+ str(start_velocity_label.__len__()))
print("END LABEL: "+ str(end_velocity_label.__len__()))
print("\n")

#COMBINE TABLE
final_x1 = []
final_y1 = []
final_z1 = []
final_x2 = []
final_y2 = []
final_z2 = []
final_duration = []
final_EfhLength = []
final_SlopeLength = []
final_RiseHeight = []
final_startV_label = []
final_endV_label = []
ct = 0
for k in datalist.keys():
    final_x1.append(k[0][0])
    final_y1.append(k[0][1])
    final_z1.append(k[0][2])
    final_x2.append(k[1][0])
    final_y2.append(k[1][1])
    final_z2.append(k[1][2])
    final_duration.append(durationlist[k])
    final_EfhLength.append(datalist[k][0])
    final_SlopeLength.append(datalist[k][1])
    final_RiseHeight.append(datalist[k][2])
    final_startV_label.append(start_velocity_label[ct])
    final_endV_label.append(end_velocity_label[ct])
    ct=ct+1

print(str(final_x1.__len__())+","+
      str(final_x2.__len__())+","+
      str(final_y1.__len__())+","+
      str(final_y2.__len__())+","+
      str(final_z1.__len__())+","+
      str(final_z2.__len__())+","+
      str(final_duration.__len__())+","+
      str(final_EfhLength.__len__())+","+
      str(final_SlopeLength.__len__())+","+
      str(final_RiseHeight.__len__())+","+
      str(final_startV_label.__len__())+","+
      str(final_endV_label.__len__())
      )

final_list = list(zip(final_x1,final_y1, final_z1, final_x2, final_y2, final_z2,
                      final_duration, final_EfhLength, final_SlopeLength,
                      final_RiseHeight, final_startV_label, final_endV_label))
df = pd.DataFrame(data=final_list,columns=['x1', 'y1', 'z1', 'x2', 'y2','z2','duration','EfhLength','SlopeLength','RiseHeight','startV_label','endV_label'])
df.to_csv('roadSegment.csv')
#Calculate velocity
#print(velocity.__len__())
#n, bins, patches = plt.hist(start_velocity, 200, range = (0,80), color='blue', alpha=0.5)
#plt.show()

