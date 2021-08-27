# Docker Services

## Installation
cd to root project folder and apply this command:
    ./makedeb.sh

That will creates directory 'deb_dist' where .deb file is located. Install it.
Also It will place service file to /usr/lib/systemd/system/, which will cause that user will be able to run this service:
    systemctl start dockerservices.service
    systemctl status dockerservices.service
    systemctl stop dockerservices.service

    systemctl enable dockerservices.service
    systemctl disable dockerservices.service

    systemctl kill dockerservices.service

## dockerservices.service
    [Unit]
    Description=Docker Services

    [Service]
    Type=simple
    ExecStart=/usr/bin/dockerservices --check-delay 30 --shell /home/commrat/Job/DockerComposeEnsure/active ./run

    [Install]
    WantedBy=multi-user.target

## Service file
### Type
The Type= directive can be one of the following:

simple: The main process of the service is specified in the start line. This is the default if the Type= and Busname= directives are not set, but the ExecStart= is set. Any communication should be handled outside of the unit through a second unit of the appropriate type (like through a .socket unit if this unit must communicate using sockets).

forking: This service type is used when the service forks a child process, exiting the parent process almost immediately. This tells systemd that the process is still running even though the parent exited.

oneshot: This type indicates that the process will be short-lived and that systemd should wait for the process to exit before continuing on with other units. This is the default Type= and ExecStart= are not set. It is used for one-off tasks.
dbus: This indicates that unit will take a name on the D-Bus bus. When this happens, systemd will continue to process the next unit.

notify: This indicates that the service will issue a notification when it has finished starting up. The systemd process will wait for this to happen before proceeding to other units.

idle: This indicates that the service will not be run until all jobs are dispatched.

## Useful links
Great docs about systemd files: https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files
Intro to systemd: https://wiki.archlinux.org/title/Systemd
Make it works: https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/
Unit files: https://fedoramagazine.org/systemd-template-unit-files/
