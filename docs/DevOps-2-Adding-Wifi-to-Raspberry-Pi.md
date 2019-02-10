# Adding Wifi to Raspberry Pi
The following article is used to explain how to setup Wifi for your **Raspberry Pi**.

![Raspberry Pi plus Wifi](media/devops-2-1-wifi.jpeg)

The USB Wifi Adapter device we will be using is: ``TP-Link 300Mbps High Gain Wireless USB Adapter (TL-WN822N)``.

## Instructions

1. Check to see what USB devices are connected to your **Raspberry Pi**.

    ```
    lsusb
    ```

2. The output you would get would look something like this. From the list you should see seomthing like ``WLAN Adapter``, this is good! This is our Wifi.

    ```
    Bus 001 Device 005: ID 06c2:003f Phidgets Inc. (formerly GLAB)
    Bus 001 Device 004: ID 0bda:8178 Realtek Semiconductor Corp. RTL8192CU 802.11n WLAN Adapter
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
    Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. SMC9514 Hub
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    ```

3. Next run the command to scan all the available wifi signals.

    ```
    sudo iwlist wlan0 scan
    ```

4. Search through the list of sign until you find the one you are looking for and write down the details somewhere. Please look at the ``ESSID`` line to find the name of the WIFI endpoint you are using.

5. Next, open ``wpa_supplicant.conf``:

    ```
    sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
    ```

6. Append the file with the following contents - please change to suite your needs:

    ```
    network={
        ssid="SSID"
        psk="WIFI PASSWORD"
    }
    ```

7. Wireless connectivity should start immediately; if not, use

    ```
    sudo ifdown wlan0
    sudo ifup wlan0
    ```

8. Now disconnect the ethernet cable and restart the **Raspberry Pi** using the following command:

    ```
    sudo reboot
    ```

9. (Optional) Now while you are running on your **MacOS** computer, run the following code which scan all the connect computers on the network. Once the command was run, look through and find the IP address of the **Raspberry Pi**.

    ```
    arp -a
    ```

10. This may involve random guessing, but write the following command and change the IP address until you find the correct device.

    ```
    ssh -l pi 192.160.0.29
    ```

11. If you finally find the correct one, congradulations! Your **Raspberry Pi** now has support for wifi.

Special Thanks:

* https://www.makeuseof.com/tag/setup-wi-fi-bluetooth-raspberry-pi-3/

## Alternative Instructions
If the USB Wifi adapter option is too complicated, you have other options! If you purchase a **Dlink DIR 505**, you can set it as [extending your network router](https://eu.dlink.com/uk/en/support/faq/routers/mobile-routers/dir-series/dir-505/how-do-i-configure-my-dir-505-to-work-as-a-wireless-extender) and all you'll have to do is simple connect an ethernet cable from the **Raspberry Pi** to this device and you have Wifi!

![Raspberry Pi plus Wifi](media/devops-2-2-wifi.jpeg)
