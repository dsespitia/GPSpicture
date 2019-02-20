# GPSpicture

GPSpicture is a script written in Python that allows you to obtain geolocation data of several images and then display this information on a map. For the script to work, it is mandatory that the images contain the GPSinfo field within the metadata.

GPSpicture can be useful in the investigation or audit process to determine the exact location where the images being analyzed were taken.


# Prerequisities

It is mandatory to have a Google API ID, which allows using the GMaps static.

To run the GPSpicture you need python 3.6 and some python libraries. You can install this with:

pip install -r requirements.txt

# Usage

python gps_picture.py -T type_map /path/to/pictures
  
  
#  License
This project is licensed under the GNU General Public License - see the LICENSE file for details

