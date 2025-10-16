import math
import urllib.request, json 
from sympy import solve,Symbol
import sympy
import sys
#altitude - float, original altitude from camera Exif calculated from sea level.
#atomic_scale - float, scale of the SfM reconstruction around the image.
#camera_parameters - array of float, focal length, k1, k2. .
#camera_type - enum, type of camera projection: "perspective", "fisheye", "equirectangular" (or equivalently "spherical")
#captured_at - timestamp, capture time.
#compass_angle - float, original compass angle of the image.
#computed_altitude - float, altitude after running image processing, from sea level.
#computed_compass_angle - float, compass angle after running image processing.
#computed_geometry - GeoJSON Point, location after running image processing.
#computed_rotation - enum, corrected orientation of the image. .
#creator - { username: string, id: string }, the username and user ID who owns and uploaded the image.
#exif_orientation - enum, orientation of the camera as given by the Exif tag. .
#geometry - GeoJSON Point geometry.
#height - int, height of the original image uploaded.
#is_pano - boolean, a true or false indicator for whether an image is 360 degree panorama.
#make - string, the manufacturer name of the camera device.
#model - string, the model or product series name of the camera device.
#thumb_256_url - string, URL to the 256px wide thumbnail.
#thumb_1024_url - string, URL to the 1024px wide thumbnail.
#thumb_2048_url - string, URL to the 2048px wide thumbnail.
#thumb_original_url - string, URL to the original wide thumbnail.
#merge_cc - int, ID of the connected component of images that were aligned together.
#mesh - { id: string, url: string } - URL to the mesh.
#sequence - string, ID of the sequence, which is a group of images captured in succession.
#sfm_cluster - { id: string, url: string } - URL to the point cloud data in JSON and compressed by zlib. See the example below.
#width - int, width of the original image uploaded.
#detections - JSON object, detections from the image including base64 encoded string of the image segmentation coordinates.

#The z-axis points forward
#The y-axis points down
#The x-axis points to the right

id=sys.argv[1]
print('id='+id)

with urllib.request.urlopen("https://graph.mapillary.com/"+id+"?access_token=MLY|4463150933761310|5995ca3757fc4f9a9c8f5e96b2efaa03&fields=camera_parameters,camera_type,exif_orientation,computed_geometry,computed_rotation,width,height,computed_compass_angle") as url:
    data = json.load(url)

print(data)
width=data['width']
height=data['height']
f=data['camera_parameters'][0]
k1=data['camera_parameters'][1]
k2=data['camera_parameters'][2]
whratio=width/height
#----------------------------------------
#xn=x/z
#yn=y/z
#r2=xn^2+yn^2
#d=1+k1*r2+k2*r2^2
#u=f*d*xn
#v=f*d*yn
xn=Symbol('xn')
result=solve(f*(1+k1*((xn**2)*(1+1/whratio)**2)+k2*(((xn**2)*(1+1/whratio)**2)**2))*xn-0.5,xn)
#math.atan2(y, x)
for i in result:
    print(type(i))
    if isinstance(i,sympy.core.numbers.Float):
        angle=math.atan2(i,1)*2 #xn faces the angle, 1 because xn is normalized. multiply by 2for the full angle.
        angle_deg=angle/math.pi*180
        print(i,angle,angle_deg)

