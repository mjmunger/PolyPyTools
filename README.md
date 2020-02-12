# Quickstart and installation

## Dependencies
1. Python 3.6 or higher
1. `pwgen_secure` library. Install with: `pip3 install pwgen_secure`

# Configure Asterisk and Polycoms from a CSV file.


This package is designed to read a CSV file, and help you generate sip.conf device definitions, which can then be used to generate Polycom config files.
## Quick start and Order of Operations

1. Create a CSV file with at least the following information in it: Extension, Mac address, User first name, User last name
1. Run `polypy configure` to setup the polypy app.
1. Run `polypy sip configure` to setup your column definition map.
1. Run `polypy sip generate all from /path/to/csv/file`
1. Run `polypy provision` to generate the Polycom config files you need.

## Commands

### configure

This helps setup the polypy environment by telling PolyPy where to find your asterisk config path, tftp server config path and other important stuff.

#### Local configuration
In many cases, it's useful to keep a local `polypy.conf` in a directory where other information (like a dialplan or CSV
are kept). `polypy` is smart, and will check the current directory for a `polypy.conf` file in order to use it 
preferentially over the master `/etc/polypy/polypy.conf` file.

To setup a local `polypy.conf` file, execute the following receipe:
1. `polypy configure set-defaults here` to create the default `polypy.conf` file at the current path.
1. `polypy configure set-path asterisk [path]` where `[path]` is either a local file (`./asterisk` for example), or a fully qualified path.
1. `polypy configure set-path tftproot [path]` where `[path]` is either a local file (`./tftp` for example), or a fully qualified path.
1. `polypy configure show` to verify the paths and settings.


### provision

Command: `polypy provision polycom`

This command helps you provision Polycom phones and maintain decent security on those phones. You can:
1. Provision one or more extensions as defined in sip.conf to a single phone.
1. Provision all phones defined in sip.conf.
1. List all the devices that are found in sip.conf
1. Show a particular extension
1. Clean a particiular extension
1. Swap two extensiosn (really useful when Bob and Alice want to swap phones).
1. Audit passwords
1. Reset a password for an extension.

### sip

This command generates device entries for `sip.conf` and (optionally) voicemail entries for `voicemail.conf`.
See command help: `polypy sip` for more commands and details.