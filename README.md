Mika Thing (Python)
===

A real-time runtime Internet of Things (IoT) data logger. Current supported devices:

* [HUM1000_0 - Humidity Phidget](https://phidgets.com/docs/HUM1000_User_Guide)
* [TMP1000_0 - Temperature Phidget](https://phidgets.com/docs/TMP1000_User_Guide)

Data logger saves all the **time-series data** locally in a ``SQLite`` database and if enabled supports remote uploading to [MikaPost](https://MikaPost.com) data repository.

The data logger has been tested and works on:

* MacOS
* Linux

## Screenshots
![Raspberry Pi + Phidgets](docs/media/pi_plus_phidget_packaging.jpeg?raw=true "Mika Thing Project")
![Mika Thing](docs/media/raspberry_pi_plus_phidgets_project.jpeg?raw=true "Mika Thing Project")

## Documentation

### Installation
* [Install on MacOS / Linux for development](/docs/Dev-1-Setup-and-Install.md)
* [Install on Raspberry Pi for production](/docs/DevOps-1-Setup-and-install-on-raspbian.md)

### Extra
* [Adding Wifi to Rasbperry Pi](/docs/DevOps-2-Adding-Wifi-to-Raspberry-Pi.md)
* [Building a Prototype Case](/docs/DevOps-3-Building-a-Prototype-Case.md)

## License
This library is licensed under the **BSD** license. See [LICENSE](LICENSE) for more information.
