# PyPI Mirror: Bandersnatch w/ Docker Compose & nginx

Simple setup to run a PyPI mirror using Bandersnatch w/ Docker Compose & nginx.

## Setup

1. Clone this repository:

   ```sh
   git clone https://github.com/sean-donoghue/pypi-mirror.git
   ```

2. Place pip requirements file(s) in the `requirements` directory (ensure files have the
   `.in` extension, `.txt` files are generated by the next step)

3. Run the `compile_requirements.py` script to generate pinned requirements files via
   [pip-compile](https://github.com/jazzband/pip-tools/):

   ```sh
   # Output from pip-compile can vary between environments and Python versions;
   # Run the script in a Python 3.11 container to ensure consistent results
   docker run -it --rm -v "$PWD":/app -w /app python:3.11-alpine \
       sh -c "pip install pip-tools && python compile_requirements.py"

   # Or run it directly if you still want to and have Python 3.11 installed
   pip3.11 install --user pip-tools && python3.11 compile_requirements.py
   ```

4. Start the Docker Compose stack:

   ```sh
   docker-compose up -d
   ```

5. Wait for the Bandersnatch container to sync packages and exit:

   ```sh
   docker-compose logs -f bandersnatch
   ```

Your mirror should now be available at: `http://localhost/simple/`  
Your requirements files should also be served at: `http://localhost:81/`

## Usage

To use the mirror instead of PyPI, use the `--index-url` or `-i` option with pip:

```sh
pip install requests --index http://localhost/simple/
```

You can also directly use the mirror for requirements files:

```sh
pip install -r http://localhost:81/requirements-example.txt -i http://localhost/simple/
```

If you left the example requirements files in the `requirements` directory, the above
commands should work as-is.

## Setting up a portable mirror on a Raspberry Pi

This setup can be used to create a portable PyPI mirror on a Raspberry Pi, provided you
have the necessary hardware.

### Recommended Hardware

- Raspberry Pi 4 or newer (incl. microSD card, power supply, case, etc.)
- USB 3.0 external drive (for package storage)
- USB Wi-Fi adapter (to provide Wi-Fi access point)
- Powered USB hub (to power the external drive and Wi-Fi adapter)

### Steps

1. Download & install [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

2. Flash the microSD card with Raspberry Pi OS Lite, with the following options:

   - Enable SSH
   - Set up Wi-Fi (if not using Ethernet for internet access)
   - Set the hostname to `pypi-mirror`

3. Install [RaspAP](https://docs.raspap.com/), saying no to:

   - OpenVPN
   - REST API
   - Ad blocking
   - WireGuard

   ```sh
   curl -sL https://install.raspap.com | bash
   ```

   When installation is complete, **do not** reboot yet.

4. Change the default port for the RaspAP web GUI to 90, avoiding conflicts with Nginx:

   ```bash
   sudo sed -i "s/^\(server\.port *= *\)[0-9]*/\190/g" /etc/lighttpd/lighttpd.conf
   sudo systemctl restart lighttpd.service
   ```

5. By default, RaspAP will configure itself to use the onboard Wi-Fi adapter (wlan0). If
   you are using a USB Wi-Fi adapter and require wlan0 to be used for internet access,
   run the following commands:

   ```bash
   sudo rm /etc/NetworkManager/system-connections/preconfigured.nmconnection
   sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
   sudo head -n 12 /etc/dhcpcd.conf | sudo tee /etc/dhcpcd.conf > /dev/null
   ```

   This will remove the preconfigured network connection, remove the default Wi-Fi
   configuration, and undo the changes made by RaspAP to the dhcpcd configuration for
   wlan0.

6. Install [Docker](https://docs.docker.com/engine/install/debian/), following the
   instructions for Debian or using the convenience script below:

   ```sh
   curl -fsSL https://get.docker.com | bash
   ```
