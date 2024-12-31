# Rpi_Mass_Image_Writer_dd
Raspberry Pi 5 that writes to many USB drives in one go. Use the LCD Keypad buttons to select the stored disk image to copy as well as reboot the device. 

Up and Down buttons are used to navigate the menu, Select button is used to confirm. When given a confirmation choice the Select button confirms the choice and any other button will cancel.

Disk images are transferred to the Raspberry Pi via a Samba shared folder. The selected image is then written in to all the drives using the ```dcfldd``` command.

## How to use?

1. Login to shared folder
2. Transfer image files via samba to shared folder
3. Plug in all USB flash drives to write to
4. Hit left button to enumerate all images and drives
5. Use up/down buttons to select image
6. Press the right button to start writing to drives. You can press it again to terminate writing.
7. Press the select button (extreme left) to shutdown device properly to prevent data corruption. The words "Shutting down" will remain even after the device has completely shutdown, so just wait for the activity light to turn off before pulling the power.

## Hardware

- Raspberry Pi 5 Model B ([CE Link](https://core-electronics.com.au/raspberry-pi-5-model-b-4gb.html)) (Any Pi with USB 3.0 ports will work just as well)
- Adafruit i2c 16x2 LCD Pi Plate with keypad ([CE Link](https://core-electronics.com.au/adafruit-blue-white-16x2-lcd-keypad-kit-for-raspberry-pi.html))
- USB hubs ([Slimline USB 3.0 7 Port Hub](https://core-electronics.com.au/slimline-usb-3-0-7-port-hub.html))
- USB SD card adapters

## Setting up

Use the Raspberry Pi Imager ([Link](https://www.raspberrypi.com/software/)) to install Raspberry Pi OS (64-bit) onto an SD card that is large enough to store multiple large img files (32Gb or larger is recommended).

Use the following OS customisation settings:

GENERAL
- Username: MassImageWriter
- Password: MassImageWriter123
- Time zone: Australia/Sydney
- Keyboard layout: us

SERVICES
- Enable SSH
- Use password authentication

Once the Pi is booted with this SD card either open a terminal window on the Pi or SSD into it. Run the following commands on the Pi to install the required files:

    sudo apt update && sudo apt-get upgrade -y && sudo apt-get install -y samba samba-common-bin git

The I2C interface will need to be enabled to use the LCD display. 

    sudo raspi-config

Interface Options -> I2C -> Yes -> Ok -> Finish

More detailed instructions for enabling I2C can be found [here](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/).

Clone this github and the included python scripts:

    git clone https://github.com/samaro119/Rpi_Mass_Image_Writer_dd.git
    cd Rpi_Mass_Image_Writer_dd

Run the app:

    python3 writeImgSD.py

The LCD screen should now turn on.

Open the samba config file with the nano editor:

    sudo nano /etc/samba/smb.conf

Add/Modify the following lines of your smb.conf file:

    [global]
      workgroup = WORKGROUP
      server string = SD Duplicator
      security = user
      log file = /var/log/samba/%m.log
      max log size = 50
      dns proxy = no

    [images]
       comment= Pi Shared Image Folder
       path= /home/MassImageWriter/Rpi_Mass_Image_Writer_dd/images
       writeable=Yes

Save and exit the config file with ```ctrl + S``` and ```ctrl + X```.

Setup the samba folder:

    sudo systemctl start smbd
    sudo smbpasswd -a MassImageWriter
    
You will be prompted to create a password for this user. Use the same password as the login password "MassImageWriter123"

    sudo systemctl restart smbd
    systemctl enable smbd

The enable command will prompt you to enter the user password a few times to authenticate.

You should be able to access this folder now over the network ([link for further instructions](https://pimylifeup.com/raspberry-pi-samba/)). 

To connect to your Samba on Windows, begin by opening up the “File Explorer“. Within the “File Explorer” click the “Computer” tab then click “Map network drive”. You will now be greeted by the dialog shown below asking you to enter some details.

Within the “Folder” textbox you will want to enter the following “\\raspberrypi\images“. If for any reason the connection fails, you can switch out “raspberrypi” with your Raspberry Pi’s local IP address (find this on the Pi using ```hostname -I```)

Once done, click the “Finish” button to finalize the connection.

Copy the "WriteImgSD.py" and "mass_image_writer.service" files into this folder and create a new folder called "compressedImages".

To setup this script to run on boot, add mass_image_writer.service to the /etc/systemd/system Folder. This file can be moved over from the files current directory by using:

    sudo mv mass_image_writer.service /etc/systemd/system

Run the following commands to have this service run on boot:

    sudo systemctl daemon-reload
    
    sudo systemctl enable mass_image_writer.service
    
    sudo systemctl start mass_image_writer.service

When the last command is finished the LCD display should turn on and start the Mass Image Writer script. If you suspect an error has occured use the following command for troubleshooting:

    sudo systemctl status mass_image_writer.service

Thats it! reboot the system using the LCD display interface or with the command ```reboot```.

## References

- [Raspberry Pi config](https://www.raspberrypi.com/documentation/computers/configuration.html)
- [Core Electronics SD card](https://core-electronics.com.au/16gb-microsd-card-with-noobs-for-all-raspberry-pi-boards.html)
- [Samba installation tutorial](https://pimylifeup.com/raspberry-pi-samba/)
- [Adafruit LCD Keypad](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi/python-usage)
- [Adafruit LCD Keypad required files](https://github.com/adafruit/Adafruit_CircuitPython_CharLCD/blob/main/adafruit_character_lcd/character_lcd_rgb_i2c.py)
- [Previous Mass Image Writer Project](https://github.com/CoreElectronics/rpi-mass-image-writer)
