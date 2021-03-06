import utils
import time
import SlotsClassifier as sc
import SlotsPreprocessor as sp
import cv2

class SlotsDetector:

    def __init__(self):
        self.classifier = sc.SlotsClassifier()
        self.found = False
        self.preprocess = sp.SlotsPreprocessor()
        self.directions = [0,0]
        self.isTaskComplete = False
        self.shapes = {1: "vertical", 2: "horizontal", 3: "square"} # so we can change names quicker
        self.shape_buffer = 15
        self.shape_list = []
        self.is_direction_center = True
        self.is_red_left = False

    def get_shape(self, roi, buff):
        if roi == None:
            return None
        else:
            x, y, w, h = roi

        #if ( (h >= (w + buff) ) or (h >= (w - buff) )):
        if h - w > buff:
            return self.shapes[1] # vertical
        #elif ( (h <= (w + buff) ) or (h <= (w - buff) )):
        elif w - h > buff:    
            return self.shapes[2] # horizontal
        else:
            return self.shapes[3] # square

    def detect(self, frame):
        print 'testing slots detect'
        if frame is not None:
            height, width, ch = frame.shape
            center = (width / 2, height / 2)
            regions_of_interest = self.preprocess.get_interest_regions(frame)
            
            for x, y, w, h in regions_of_interest:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), utils.colors["red"], 2)

            gate = self.classifier.classify(frame, regions_of_interest)
            
            gate_shape = self.get_shape(gate, self.shape_buffer)

            if gate_shape == self.shapes[3] or gate_shape == self.shapes[1]:
                gate = None
                
            if (gate == None):
                self.directions = [0, 0]
                self.found = False
                gate_shape = None
                w, h = 0, 0
            else:
                x, y, w, h = gate
                cv2.rectangle(frame, (x, y), (x + w, y + h), utils.colors["blue"], 6)

                w_pad = w / 7
                h_pad = h / 7
                if self.is_direction_center:
                    self.directions = utils.get_directions(center, x, y, w, h)
                    cv2.rectangle(frame, (x + (3*w_pad), y + (3*h_pad)), (x + (4 * w_pad), y + (4 * h_pad)), utils.colors["green"], 2)
                else:
                    if self.is_red_left:
                        self.directions = utils.get_directions_left(center, x, y, w, h)
                        cv2.rectangle(frame, (x + (2*w_pad), y + (3*h_pad)), (x + (3 * w_pad), y + (4 * h_pad)), utils.colors["green"], 2)
                    else:
                        self.directions = utils.get_directions_right(center, x, y, w, h)
                        cv2.rectangle(frame, (x + (4*w_pad), y + (3*h_pad)), (x + (5 * w_pad), y + (4 * h_pad)), utils.colors["green"], 2)
                self.found = True
            return (self.found, self.directions, gate_shape, (w, h))
        else:
            print('error no frame')
            return False, None, None, None