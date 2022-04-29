# js8msg2
version 2 of JS8msg

New features for JS8msg V2:
    1) a standard 'Menu" GUI instead of the "Notebook" GUI
    2) encoded form and encoded text are chunked into smaller pieces allowing your station to meet the regulatory requirement for station ID
    3) the configuration is now kept in a sqlite3 database
    4) The ICS-213 form is now handled with 2 separate GUI windows, one for the originator and one for the responder

Special recognition to the following for their contribution to the improvements in JS8msg:
    First, Takahide Kanatake, JE6VGZ, for allowing me to use his python code for henkankun encoding / decoding
    Second, Joseph D Lyman, KF7MIX, for allowing me to use parts of JS8spotter, http://kf7mix.com/js8spotter.html

Changes:
    The layout of JS8msg will change for both Windows and Linux. The older JS8msg used the home directory to base the support directories. 
    The Linux was a bit of a mess. With JS8msg V2, both will have a directory called JS8msg created in their respective home directory.

    Within JS8msg directory, the JS8msg V2 program will create the support directories of Doc (for documentation), HtmlTemplates (to hold the ICS forms),
    Local (for misc. items), Messages (to hold outgoing and incoming messages) and Tmp (for temporary files)

    For Windows, the executable will be installed as was previously. 
    For Linux, there will be an executable file called "js8msg2". The js8msg2 will need the executable property enabled and 
    be located where js8msg2 can be found via the shell PATH variable (like ~/bin as an example).