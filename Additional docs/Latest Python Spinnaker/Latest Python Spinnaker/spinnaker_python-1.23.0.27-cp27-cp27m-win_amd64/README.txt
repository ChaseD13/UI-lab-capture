=============================================================================
Copyright (c) 2001-2018 FLIR Systems, Inc. All Rights Reserved.

This software is the confidential and proprietary information of FLIR
Integrated Imaging Solutions, Inc. ("Confidential Information"). You
shall not disclose such Confidential Information and shall use it only in
accordance with the terms of the license agreement you entered into
with FLIR Integrated Imaging Solutions, Inc. (FLIR).

FLIR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE, OR NON-INFRINGEMENT. FLIR SHALL NOT BE LIABLE FOR ANY DAMAGES
SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
THIS SOFTWARE OR ITS DERIVATIVES.
=============================================================================

=============================================================================
==
== README
==
=============================================================================

PySpin is a wrapper for FLIR Integrated Imaging Solutions' Spinnaker library.

FLIR Integrated Imaging Solutions' website is located at https://www.ptgrey.com

The PySpin Python extension provides a common software interface 
to control and acquire images from FLIR USB 3.0, GigE, 
and USB 2.0 cameras using the same API under 32- or 64-bit Windows.

=============================================================================
TABLE OF CONTENTS
=============================================================================
1. INSTALLATION
1.1 INSTALLATION ON WINDOWS
1.2 INSTALLATION ON LINUX
1.3 INSTALLATION ON MACOS
2. API DIFFERENCES
3. REMOVE PYSPIN

=============================================================================
1. INSTALLATION
=============================================================================

-----------------------------------------------------------------------------
1.1 WINDOWS
-----------------------------------------------------------------------------

1. Install Python. Currently we support Python 2.7, 3.5, and 3.6. To 
   download Python, visit https://www.python.org/downloads/. Note that the
   Python website defaults to 32-bit interpreters, so if you want a 64-bit
   version of Python you have to click into the specific release version.
   
2. (Optional) Set the PATH environment variable for your Python installation.
   This may have been done automatically as part of installation, but to do
   this manually you have to open Environment Variables through the following:

   My Computer > Properties > Advanced System Settings > Environment Variables

   Add your Python installation location to your PATH variable. For example, 
   if you installed Python at C:\Python36\, you would add the following entry
   to the PATH variable:

   C:\Python36\;<rest_of_path>

3. Configure your Python installation. From a command line, run the following
   commands to update and install dependencies:

   python -m ensurepip
   python -m pip install --upgrade pip numpy matplotlib

   NumPy is a hard requirement for PySpin. Matplotlib is not required for the
   library itself but is used in some of our examples.

4. To ensure prerequisites such as drivers and Visual Studio redistributables 
   are installed on the system, run the Spinnaker SDK installer that corresponds
   with the PySpin version number. For example, if installing PySpin 1.8.0.0, 
   install Spinnaker 1.8.0.0 beforehand, selecting only the Visual Studio 
   runtimes and drivers.

5. Run the following command to install PySpin to your associated Python version.
   This command assumes you have your PATH variable set correctly for Python:

   python -m pip install spinnaker_python-1.x.x.x-cp36-cp36m-win_amd64.whl

   Ensure that the wheel downloaded matches the Python version you are installing to!

After installation, PySpin examples can be ran directly from the command prompt.
For example, if PySpin is installed for Python 3.6 you can run a preinstalled example
using the following:
    
python Examples\Python3\Acquisition.py

-----------------------------------------------------------------------------
1.2 LINUX
-----------------------------------------------------------------------------

1. Check that pip is available for your respective Python versions 
   by running the following command:

   sudo apt-get install python-pip python3-pip

2. Install library dependencies for PySpin: numpy and matplotlib. Numpy is used
   for some image acquisition functionality and Matplotlib is used as part of 
   some of our examples to highlight possible usages of PySpin. Install these
   dependencies by running one of the following commands.

   - Install for Python 2.7, user only:
   python -m pip install --upgrade --user numpy matplotlib 

   - Install for Python 2.7, site wide:
   sudo python -m pip install --upgrade numpy matplotlib

   - Install for Python 3.5, user only:
   python -m pip install --upgrade --user numpy matplotlib

   - Install for Python 3.5, site wide:
   sudo python -m pip install --upgrade numpy matplotlib

   - Install for Python 3.6, user only:
   python -m pip install --upgrade --user numpy matplotlib

   - Install for Python 3.6, site wide:
   sudo python -m pip install --upgrade numpy matplotlib

3. Ensure that the corresponding version of the Spinnaker SDK Debian packages 
   and their prerequisites are installed beforehand 
   (ex. install the 1.8.0.45 packages if the wheel version is also 1.8.0.45)

4. Install wheel for specific Python version. This can be installed site-wide
   for all users or for a specific user. 

   Python 2.7, all users:
   sudo python -m pip install spinnaker_python-1.x.x.x-cp27-cp27mu-linux_x86_64.whl
   
   Python 2.7, current user:
   python -m pip install --user spinnaker_python-1.x.x.x-cp27-cp27mu-linux_x86_64.whl

   Python 3.5, all users (16.04 only):
   sudo python3.5 -m pip install spinnaker_python-1.x.x.x-cp35-cp35m-linux_x86_64.whl

   Python 3.5, current user (16.04 only):
   python3.5 -m pip install --user spinnaker_python-1.x.x.x-cp35-cp35m-linux_x86_64.whl
   
   Python 3.6, all users:
   sudo python3.6 -m pip install spinnaker_python-1.x.x.x-cp36-cp36m-linux_x86_64.whl
   
   Python 3.6, current user:
   python3.6 -m pip install --user spinnaker_python-1.x.x.x-cp36-cp36m-linux_x86_64.whl

5. The examples are located in the Examples folder of the extracted tarball. Run with:
   ex. "python2.7 Examples/Python2/DeviceEvents.py"

-----------------------------------------------------------------------------
1.3 MACOS
-----------------------------------------------------------------------------

1. Check that Python is installed. MacOS comes with Python 2.7 installed, 
   but it may be an older build of Python. Up-to-date Python packages
   can be downloaded from https://www.python.org/downloads.

2. Update pip for Python. Run the following command for your version of Python:

   sudo python -m ensurepip

   This will install a version of pip and allow you to update or install new wheels.

3. Install library dependencies for PySpin: numpy and matplotlib. Numpy is used
   for some image acquisition functionality and Matplotlib is used as part of 
   some of our examples to highlight possible usages of PySpin. Install these
   dependencies by running one of the following commands.

   - Install for Python 2.7, user only:
   python -m pip install --upgrade --user numpy matplotlib 

   - Install for Python 2.7, site wide:
   sudo python -m pip install --upgrade numpy matplotlib

   - Install for Python 3.5, user only:
   python -m pip install --upgrade --user numpy matplotlib

   - Install for Python 3.5, site wide:
   sudo python -m pip install --upgrade numpy matplotlib

   - Install for Python 3.6, user only:
   python -m pip install --upgrade --user numpy matplotlib

   - Install for Python 3.6, site wide:
   sudo python -m pip install --upgrade numpy matplotlib

4. Ensure that the corresponding version of the Spinnaker SDK MacOS packages
   and their prerequisites are installed beforehand. 
   (ex. install 1.17.0.19 packages if the wheel version is also 1.17.0.19)

5. Install the PySpin wheel for specific Python version.
   ex. sudo python -m pip install spinnaker_python-1.x.x.x-cp27-cp27mu-macos_x86_x64.whl" for 64-bit Python 2.7

6. The examples are located in the Examples folder of the extracted tarball. Run with:
   ex. python Examples/Python2/DeviceEvents.py

=============================================================================
2. API DIFFERENCES
=============================================================================

Except for the changes listed below, most function names are exactly the same
as the C++ API. See examples for PySpin usage!

- All methods of SpinnakerException no longer exist, please replace all 
  usages of SpinnakerException with any of the following attributes:
    message: Normal exception message.
    fullmessage: Exception message including line, file, function, 
                    build date, and time (from C++ library).
    errorcode: Integer error code of the exception.
  The SpinnakerException instance itself can be printed, as it derives from 
  the BaseException class and has a default __str__ representation. 
  See examples for usage.

- Image creation using NumPy arrays (although the int type of the array must be uint8)

- The majority of headers from the C++ API have been wrapped, with the exception of:
    - Headers with "Adapter" or "Port" in the name
    - NodeMapRef.h, NodeMapFactory.h
    - Synch.h, GCSynch.h, Counter.h, filestream.h

- INode and IValue types (esp. returned from GetNode()) have to 
  be initialized to their respective pointer types
    (ex. CFloatPtr, CEnumerationPtr) to access their functions

- CameraPtr, CameraList, InterfacePtr, InterfaceList, and SystemPtr
  have to be manually released and/or deleted before program exit (use del operator)
    - See EnumerationEvents example

- Image.GetData() returns a 1-D NumPy array of integers, the int type
  depends on the pixel format of the image

- Image.GetNDArray() returns a 2 or 3-D NumPy array of integers, only for select 
  image formats. This can be used in libraries such as PIL and/or OpenCV.

- Node callbacks take in a callback class instead of a function pointer
    - Register is now RegisterNodeCallback, Deregister is now DeregisterNodeCallback
    - See NodeMapCallback example for more details

- IImage.CalculateChannelStatistics(StatisticsChannel channel) returns 
  a ChannelStatistics object representing stats for the given channel 
  in the image. These stats are properties within the ChannelStatistics object, 
  Please see the docstring for details. This replaces ImageStatistics!

- Pass-by-reference functions now return the type and take in void
    - GetFeatures() returns a Python list of IValue, instead of taking 
      in a FeatureList_t reference
    - GetChildren() returns a Python list of INode, instead of taking 
      in a NodeList_t reference
    - Same with GetEntries(), GetNodes()
    - GetPropertyNames() returns a Python list of str, 
      instead of taking in a gcstring_vector reference
    - See DeviceEvents example for usage

- Methods Get() and Set() for IRegister and register nodes use NumPy arrays
    - Get() takes in the length of the register to read and two optional 
      bools, returns a NumPy array
    - Set() takes in a single NumPy array

=============================================================================
3. REMOVE PYSPIN
=============================================================================

Removing or updating PySpin is similar to removing or updating other wheels. 

If removing from a user-specific install, run the following command:

python -m pip uninstall spinnaker-python

For Windows, if you need to remove PySpin from a site-wide install, the following
command needs to be run from an administrator command prompt:

python -m pip uninstall spinnaker-python

For Linux or MacOS, if you need to remove PySpin from a site-wide install 
the following command needs to be run as sudo:

sudo python -m pip uninstall spinnaker-python