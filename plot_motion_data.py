import csv
import matplotlib.pyplot as plt

# We must name this session
session_name = input('Session Name: ')

SCREEN_SCALE_FACTOR = 1.6
DOT_COLOR = (0.173, 0.992, 0.996)

x_coords = []
y_coords = []
circle_coords = [[0.448, 0.495], [0.526, 0.495], [0.754, 0.495], [0.972, 0.495], [1.048, 0.495], [0.754, 0.606], [0.753, 0.372]]
num_coords = 0
enclosed_coords = 0
correctness = 0

# Test if the dot is enclosed within a circle
def is_enclosed(x, y):
  for coord in circle_coords:
    if ((x - coord[0])**2 + (y - coord[1])**2 <= 0.022**2):
      return 1
  return 0

# Read in the motion data and write to the session
with open('./motion_data.csv', newline='') as csvfile:
  data = csv.reader(csvfile, delimiter=' ', quotechar='|')
  for row in data:
    x_coord, y_coord = map(float, row[0].split(','))
    # Grab only those coords that are near the tooltip
    if (y_coord > 0.3):
      x_coord = x_coord * SCREEN_SCALE_FACTOR # offset by screen resolution scale
      x_coords += [x_coord]
      y_coords += [y_coord]
      enclosed_coords += is_enclosed(x_coord, y_coord)
      num_coords+=1
  correctness = str(round(enclosed_coords/num_coords * 100, 3))

# Write the session results
with open('./motion_results.csv', 'a') as csvfile:
  filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  filewriter.writerow([session_name, correctness])

# Scale the access to match coord system
fig, ax = plt.subplots()
axs = plt.gca()
axs.set_ylim(ax.get_ylim()[::-1])        
axs.xaxis.tick_top()                   
axs.yaxis.tick_left()

img = plt.imread("./usability_test.png")
ax.imshow(img, extent=[0, 1 * SCREEN_SCALE_FACTOR, 0, 1], origin='lower')

for coord in circle_coords:
  ax.add_artist(plt.Circle(coord, 0.022, color=DOT_COLOR))

plt.scatter(x_coords, y_coords, color='red', zorder=3)
plt.title('Eye Tracking Data')
plt.text(0.05, 0.12, 'Correctness: ' + correctness + '%', color='red', fontweight=800)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
