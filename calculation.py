import math
import numpy as np
import cv2

# back cameras: 31.5 in
# front cameras: 36 in

# height of camera in meters

# ejector-side, shooter-side (meters)
cam_height = 0.8
#vertical angle
cam_angle = 23

# horizontal & vertical fields of view
hfov = 52
vfov = 39


def angleToObject(bbox_xyxy, imdim):
     # image resolution (x, y)
    resolution = (imdim[1], imdim[0])
    # center of image
    center = (resolution[0]/2, resolution[1]/2)

    # center of bounding box
    # TODO center pixel should be relative to polygon not bounding box
    center_pixel = ((bbox_xyxy[0] + bbox_xyxy[2]) / 2, (bbox_xyxy[1] + bbox_xyxy[3]) / 2)

    # angle to center pixel in X and Y directions
    angle_x = (center_pixel[0] / resolution[0]) * hfov
    angle_y = (center_pixel[1] / resolution[1]) * vfov

    return angle_x, angle_y

# depth is in centimeters, convert to meters. depth is also the hypotenuse of triangle
# angle to ball is in degrees, angle between height and hypotenuse
# get base of triangle
def getDepthFromRobotBase(depth, angleToObj):
    # convert to radians
    angleToObj = math.radians(angleToObj)
    # get base of triangle
    base = depth * math.sin(angleToObj)
    return base


def doMath(object, object_type, im):

    # xyxy format
    bbox = object["bounding_box"]

    # m = cv2.moments(cone_polygon)
    # cx = int(m["m10"] / m["m00"])
    # cy = int(m["m01"] / m["m00"])
    # cv2.circle(im, (int(cx), int(cy)), 5, (0, 0, 255), -1)

    # image resolution
    resolution = (im.shape[1], im.shape[0])
    # center of image
    center = (resolution[0]/2, resolution[1]/2)

    # bounding width and height
    bounding_width = bbox[2] - bbox[0]
    bounding_height = bbox[3] - bbox[1]

    bounding_top_left_x = bbox[0]
    bounding_top_left_y = bbox[1]
    bounding_btm_right_x = bbox[2]
    bounding_btm_right_y = bbox[3]


    # center of bounding box
    center_pixel = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
    cv2.circle(im, (int(center_pixel[0]), int(center_pixel[1])), 5, (0, 0, 255), -1)

    # angle to center pixel in X and Y directions
    angle_x = (center_pixel[0] / resolution[0]) * hfov
    angle_y = (center_pixel[1] / resolution[1]) * vfov
    
    # error checking (if bounding box is 0, dividng by 0)
    if bounding_width > 0 and bounding_height > 0 and np.sin(angle_x * np.pi/180) != 0 and np.sin(angle_y * np.pi/180) != 0:

        distance = 0

        clipped_x = False
        clipped_y = False

        cone_height = 12.8125
        cone_width = 8.375
        cube_height_width = 9.5

        selected_dim_height = 0
        selected_dim_width = 0


        if(object_type == "cone"):
            selected_dim_height = cone_height
            selected_dim_width = cone_width
        elif(object_type == "cube"):
            selected_dim_height = cube_height_width
            selected_dim_width = cube_height_width

        # if object clipped into left edge, use height for distance. use inches for real obj. dimension
        if bounding_top_left_x - 2 <= 0:
            distance = (center_pixel[1] / np.sin(angle_y * np.pi/180)) * (selected_dim_height / bounding_height)
            clipped_x = True
        # if object is clipped into right edge, use height for distance
        elif bounding_btm_right_x + 2 >= resolution[0]:
            distance = (center_pixel[1] / np.sin(angle_y * np.pi/180)) * (selected_dim_height / bounding_height)
            clipped_x = True
        # if object is clipped into bottom edge, use width for distance
        if bounding_top_left_y - 2 <= 0:
            distance = (center_pixel[0] / np.sin(angle_x * np.pi/180)) * (selected_dim_width / bounding_width)
            clipped_y = True
        # if object is clipped into top edge, use width for distance
        elif bounding_btm_right_y + 2 >= resolution[1]:
            distance = (center_pixel[0] / np.sin(angle_x * np.pi/180)) * (selected_dim_width / bounding_width)
            clipped_y = True

        # if object is in a corner, ignore
        if clipped_x and clipped_y:
            return ""

        # if object is anywhere else, average height and width
        if not clipped_x and not clipped_y:
            distance_x = (center_pixel[0] / np.sin(angle_x * np.pi/180)) * (selected_dim_width / bounding_width)
            distance_y = (center_pixel[1] / np.sin(angle_y * np.pi/180)) * (selected_dim_height / bounding_height)

            distance = (distance_x + distance_y) / 2

        # convert to meters
        distance *= 0.0254

        ground_distance = 0

        # calculate ground distance using pythagorean theorem
        if(distance**2 - cam_height**2 >= 0):
            ground_distance = math.sqrt(distance**2 - cam_height**2)
        else:
            ground_distance = distance
            
        
        # # return string with ball data          
        # dat = str(ballid) + "," + str(ground_distance) + "," + str(angle_x) + "," + ballcolor + f",{conf:.2f}," + str(cam) + " "
        # # print(dat)
        # return dat

        # put ground distance, anglex, angley on image
        cv2.putText(im, f"ground distance: {ground_distance:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(im, f"angle x: {angle_x:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(im, f"angle y: {angle_y:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return ground_distance, angle_x, angle_y
    # ball not detected, return nothing
    return ""