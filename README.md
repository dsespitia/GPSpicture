# GPSpicture

GPSpicture is a script written un Python that allow you get ubication data and showing into map. In order for the script to perform its work, it is mandatory that the images contain the GPSinfo field within the metadata. However, if the script doesn't contain information on the non-existence of this information.

It allows in research or audit processes to determine the exact position of where the images that are being processed were taken.


# Prerequisities

It is mandatory to have a Google API ID, which allows using the GMaps static.

To run the GPSpicture you need python 3.6 and some python libraries. You can install this with:

cd gpspicture/
pip install -r requirements.txt

# Usage

python gpspicture.py -T <type select> /path/to/pictures
  
  
#  License
This project is licensed under the GNU General Public License - see the LICENSE file for details

