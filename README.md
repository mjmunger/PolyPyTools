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

### provision

This command helps you provision Polycom phones and maintain decent security on those phones. You can:
1. Provision a single extension defined in sip.conf.
1. Provision all extensions defined in sip.conf.
1. List all the devices that are found in sip.conf
1. Show a particular extension
1. Clean a particiular extension
1. Swap two extensiosn (really useful when Bob and Alice want to swap phones).
1. Audit passwords
1. Reset a password for an extension.

### sip

This command generates device entries for `sip.conf` and (optionally) voicemail entries for `voicemail.conf`.