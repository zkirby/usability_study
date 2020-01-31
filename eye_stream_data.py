from talon import app, ui
from talon_plugins.eye_mouse import tracker
from talon.track.geom import EyeFrame

main = ui.main_screen()

# Lightweight simple recording for eye tracking.
class EyeDataStream:
    def __init__(self):        
      self.x_coords = []
      self.y_coords = []

    def on_gaze(self, b):
      l, r = EyeFrame(b, 'Left'), EyeFrame(b, 'Right')
      p = (l.gaze + r.gaze) / 2
      self.x_coords += [p.x]
      self.y_coords += [p.y]
      print(p.x, p.y)
    
    def start_recording(self):
      tracker.register('gaze', self.on_gaze)

    def save_data(self):
      # Unregister gaze to prevent further recording x/y 
      tracker.unregister('gaze', self.on_gaze)

      import csv
      with open('../s/motion_data.csv', 'w') as cvs_file:
        filewriter = csv.writer(cvs_file, delimiter=',',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(self.x_coords)):
          filewriter.writerow([str(self.x_coords[i]), str(self.y_coords[i])])

eye_stream = EyeDataStream()

def record_data(state):
  print("RECORDING DATA")
  if (state):
    eye_stream.start_recording()

def save_data(state):
  print("SAVING PLOT DATA")
  if (state):
    eye_stream.save_data()
  print("PLOT DATA SAVED")

menu = app.menu.submenu('Usability', weight=999)
app.menu.sep(weight=998)
record_motion_data = menu.toggle('Record Motion Data', cb=record_data)
save_motion_data = menu.toggle('Save Motion Data', cb=save_data)
