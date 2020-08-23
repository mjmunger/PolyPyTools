# Quickstart and installation

## Dependencies
1. Python 3.6 or higher
1. `pwgen_secure` library. Install with: `pip3 install pwgen_secure`

## Using Python Virtual Environment

1. Install Python 3.7 or higher: `apt install python3 python3-pip`
1. Install python virtual environment: `pip3 install virtualenv`
1. Source the environment `source /path/to/PolyPy/venv`
1. Install: `./install.py`

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

### Provisioning a site

Polypy expects that you create a `polypy.conf` config file that is kept in the same directory as the CSV from which you are provisioning phones. It will read that file to produce a file structure that a web server or tftp server can use to provision phones.

#### Notes on firmware:
If you have correctly added the model to your endpoint definitions, polypy will choose the appropriate firmware for loading `000000000000.cfg` and `reg-basic`. It assumes that the `APPLICATION_SPIP[MODEL]` elements and attributes of that file are not to be used except in the case of manual overrides. Therefore, it will configure `APPLICATION APP_FILE_PATH` to a value for that phone with the firmware it should be using. For example, `APPLICATION APP_FILE_PATH="org-example-east/2233-12345674-001.ld"`. 

Polypy also assumes you are using **split** firmware.   

#### How to provision a site:
1. Upload the dialplan csv to `/root/clients/org-example/`
1. Use `polypy configure` to setup the `polypy.conf` file so that polypy can:
- Know where to find the `Config` folder in the firmware for the model phone you have. It will use this to write configs for that phone. 
- Know where to save the bootstrap file (in the root of the tftp directory or www directory)
- Know how to assemble the path to the site files, which are under the root.

#### How to order registrations

Registrations are created from three sections: endpoint, auth, and aor. As the parser reads the CSV, if multiple entries have the same mac address, those entries are assumed to be for the same physical phone. As such, they will be combined into a single `endpoint` section in the resulting pjsip.conf, which will have corresponding `auth` and `aors` options.

When that endpoint is provisioned, the registrations will be generated from those `aors` and `auth` option values.

It's important to note: the order for the `auth` and `aors` options *must be the same*!

Example:

The values in the table below will produce:
- 1 endpoint record
- 2 aor records
- 2 auth records

|Extension |Voicemail |Device |MAC         |Email            |site             |callerid|label|order|
|----------|----------|-------|------------|-----------------|-----------------|--------|-----|-----|
|101       |101@testvm|SPIP670|0004f23a626f|user1@example.org|place.example.org|101     |101  |2    |
|102       |101@testvm|SPIP670|0004f23a626f|user1@example.org|place.example.org|102     |102  |1    |
 
```
[0004f23a626f]
type=endpoint
context=internal
disallow=all
allow=ulaw
auth=auth0004f23a626f102,auth0004f23a626f101
aors=0004f23a626f102,0004f23a626f101

[0004f23a626f101]
type=aor
max_contacts=1

[0004f23a626f102]
type=aor
max_contacts=1

[auth0004f23a626f101]
type=auth
auth_type=userpass
username=0004f23a626f101
password=mHQFrPS

[auth0004f23a626f102]
type=auth
auth_type=userpass
username=0004f23a626f102
password=CUzouRiNfNVRw

```
When these registrations are added to the phone configuration file (generated from `reg-basic.cfg`), they will be added in the order they are listed in the directives. (Notice the `aors` record shows the line that ends in `102` before it shows the line that ends in `101`. This is because the order in the spreadsheet shows that the `102` line should be registration #1, and the `101` line should be registration #2.)

 
