# import numpy as np
# import matplotlib.pyplot as plt

# from matplotlib.animation import FuncAnimation

# from matplotlib.widgets import TextBox, Button

# from skyfield.api import load, Star, wgs84, Topos

# import datetime as dt


# eph=load('de421.bsp')

# earth=eph['earth']
# sun=eph['sun']

# my_lat=26
# my_long=73

# obs=earth+Topos(latitude_degrees=my_lat,longitude_degrees=my_long)

# ts=load.timescale()
# t=ts.now()

# year=int(input('Year: '))
# month=int(input('Month: '))
# day=int(input('Day: '))
# hour=int(input('Hour (UTC): '))
# minute=int(input('Minute: '))
# second=int(input('Second: '))

# dt_now=dt.datetime(year,month,day,hour,minute,second,tzinfo=dt.timezone.utc)



# t_list=[]
# dt_list=[]

# i=0
# while i<365:
#     i+=1
#     dt_list.append(dt_now)
#     t=ts.from_datetime(dt_now)
#     t_list.append(t)
#     dt_now+=dt.timedelta(days=1)

# t_list=np.array(t_list)
# dt_list=np.array(dt_list)

# SUN_ALTAZ=[]

# GMST=[]
# MSG=[]

# for t in t_list:
#  sun_pos=obs.at(t).observe(sun).apparent().altaz()
#  SUN_ALTAZ.append(np.array([sun_pos[0].degrees,sun_pos[1].degrees]))

#  ut1_t=t.ut1
#  gmst_t=t.gmst

#  ut1_t=(ut1_t+0.5)%1*24

#  GMST.append(gmst_t)
#  MSG.append(ut1_t)

# GMST=np.array(GMST)
# MSG=np.array(MSG)


# SUN_ALTAZ=np.array(SUN_ALTAZ)

# plt.style.use('dark_background')

# fig=plt.figure()
# ax1=fig.add_subplot()


# play_button_axes=plt.axes([0.1,0.8,0.2,0.1])
# play_button=Button(play_button_axes,'Play')


# RA_SUN=[]
# DEC_SUN=[]

# for t in t_list:
#    ra,dec,_=earth.at(t).observe(sun).apparent().radec()
#    RA_SUN.append(ra.hours)
#    DEC_SUN.append(dec.degrees)

# RA_SUN=np.array(RA_SUN)
# DEC_SUN=np.array(DEC_SUN)


# E=[]
# for i in range(len(t_list)):
#     e=GMST[i]-MSG[i]-RA_SUN[i]-12
#     e=(e+12)%24-12
#     E.append(e)

# E=np.array(E)

# ax1.set_xlim(-0.3,0.3)
# ax1.set_ylim(-30,30)

# print(np.min(E))

# ax1.scatter(E[0],DEC_SUN[0],s=40,color="#FFFB03")
# ax1.grid(True,ls='dotted')


# def update(frame):
#          ax1.clear()
#          ax1.set_xlim(-0.3,0.3)
#          ax1.set_ylim(-30,30)

#          i=frame

#          ax1.scatter(E[:i+1],DEC_SUN[:i+1],s=10,color="#FFFB03",alpha=0.5)
#          ax1.scatter(E[i],DEC_SUN[i],s=40,color="#FFFB03")
#          ax1.grid(True,ls='dotted')
#          ax1.set_title(f"{dt_list[i]} UTC")
#          ax1.set_xlabel('Equation of time (hrs)')
#          ax1.set_ylabel('Declination (deg.)')



# func=None
# def play_anim(event):
#     global func
#     if func is None:
#         func=FuncAnimation(fig,update,range(len(DEC_SUN)),interval=100)
#         func.event_source.start()
#         fig.canvas.draw()

# play_button.on_clicked(play_anim)

# plt.show()

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

from matplotlib.widgets import TextBox, Button

from skyfield.api import load, Star, wgs84, Topos

import datetime as dt


# Load the JPL DE421 ephemeris and select Earth and the Sun.
eph=load('de421.bsp')

earth=eph['earth']
sun=eph['sun']

# Set the observer's latitude and longitude in degrees.
my_lat=26
my_long=73

# Combine Earth's position with the observer's location on its surface.
obs=earth+Topos(latitude_degrees=my_lat,longitude_degrees=my_long)

# Create a Skyfield timescale and obtain the current time.
ts=load.timescale()
t=ts.now()

# Read the starting date and time in UTC.
year=int(input('Year: '))
month=int(input('Month: '))
day=int(input('Day: '))
hour=int(input('Hour (UTC): '))
minute=int(input('Minute: '))
second=int(input('Second: '))

# Construct a timezone-aware datetime for the starting observation.
dt_now=dt.datetime(year,month,day,hour,minute,second,tzinfo=dt.timezone.utc)



# Store each observation time in both Skyfield and datetime formats.
t_list=[]
dt_list=[]

# Generate 365 observations, separated by one day at the same UTC time.
i=0
while i<365:
    i+=1
    dt_list.append(dt_now)
    t=ts.from_datetime(dt_now)
    t_list.append(t)
    dt_now+=dt.timedelta(days=1)

t_list=np.array(t_list)
dt_list=np.array(dt_list)

# Store the Sun's apparent altitude and azimuth for each observation.
SUN_ALTAZ=[]

# Store Greenwich mean sidereal time and the UT1 time of day.
GMST=[]
MSG=[]

for t in t_list:
 # Calculate the Sun's apparent position relative to the observer.
 sun_pos=obs.at(t).observe(sun).apparent().altaz()
 SUN_ALTAZ.append(np.array([sun_pos[0].degrees,sun_pos[1].degrees]))

 # Obtain the UT1 Julian date and Greenwich mean sidereal time in hours.
 ut1_t=t.ut1
 gmst_t=t.gmst

 # Julian dates begin at noon; adding 0.5 shifts the day boundary
 # to midnight. Extract the fractional day and convert it to hours.
 ut1_t=(ut1_t+0.5)%1*24

 GMST.append(gmst_t)
 MSG.append(ut1_t)

GMST=np.array(GMST)
MSG=np.array(MSG)


SUN_ALTAZ=np.array(SUN_ALTAZ)

# Apply a dark background and create the plotting axes.
plt.style.use('dark_background')

fig=plt.figure()
ax1=fig.add_subplot()


# Create an axes region for the animation's Play button.
play_button_axes=plt.axes([0.1,0.8,0.2,0.1])
play_button=Button(play_button_axes,'Play')


# Store the Sun's apparent geocentric right ascension and declination.
RA_SUN=[]
DEC_SUN=[]

for t in t_list:
   # With no epoch supplied, radec() uses the ICRF/J2000-oriented axes.
   ra,dec,_=earth.at(t).observe(sun).apparent().radec()
   RA_SUN.append(ra.hours)
   DEC_SUN.append(dec.degrees)

RA_SUN=np.array(RA_SUN)
DEC_SUN=np.array(DEC_SUN)


# Estimate the equation of time in hours using sidereal time,
# UT1 time of day, and the Sun's right ascension.
# For precision work, the sidereal-time and right-ascension
# reference conventions would need to be made consistent.
E=[]
for i in range(len(t_list)):
    e=GMST[i]-MSG[i]-RA_SUN[i]-12

    # Wrap the time difference into the interval [-12, 12) hours.
    e=(e+12)%24-12
    E.append(e)

E=np.array(E)

# Set the horizontal range in hours and the vertical range in degrees.
ax1.set_xlim(-0.3,0.3)
ax1.set_ylim(-30,30)

# Print the minimum calculated equation-of-time value, in hours.
print(np.min(E))

# Display the first observation before starting the animation.
ax1.scatter(E[0],DEC_SUN[0],s=40,color="#FFFB03")
ax1.grid(True,ls='dotted')


# Redraw the accumulated observations and highlight the current one.
def update(frame):
         ax1.clear()
         ax1.set_xlim(-0.3,0.3)
         ax1.set_ylim(-30,30)

         i=frame

         # Smaller, translucent points trace the observations so far.
         ax1.scatter(E[:i+1],DEC_SUN[:i+1],s=10,color="#FFFB03",alpha=0.5)

         # A larger point marks the current observation.
         ax1.scatter(E[i],DEC_SUN[i],s=40,color="#FFFB03")
         ax1.grid(True,ls='dotted')
         ax1.set_title(f"{dt_list[i]} UTC")
         ax1.set_xlabel('Equation of time (hrs)')
         ax1.set_ylabel('Declination (deg.)')



# Keep a reference to the animation so it is not garbage-collected.
func=None
def play_anim(event):
    global func

    # Create the animation only on the first click of the Play button.
    if func is None:
        func=FuncAnimation(fig,update,range(len(DEC_SUN)),interval=100)
        func.event_source.start()
        fig.canvas.draw()

# Connect the button to its callback and open the plot window.
play_button.on_clicked(play_anim)

plt.show()