# Remapping the Caps-Lock key
Following procedure sets up remapping of caps-lock key to escape including Wayland and TTY.

1. Install the caps2esc tool
    ```bash
    pacman -S interception-caps2esc
    ```
2. Set up the intercept rule. Copy the file udevmon.yaml to /etc/.
    ```bash
    sudo cp udevmon.yaml /etc/
    ```

To run it immediately, can use:
```bash
sudo nice -n -20 /usr/bin/udevmon -c /etc/udevmon.yaml
```

## Start-up
Set up a starting unit via systemd. Copy the file caps-to-esc.service to /etc/systemd/system.
```bash
sudo cp caps-to-esc.service /etc/systemd/system
```

Notice that the caps-to-esc.service basically wraps the above run command with systemd syntax.

Now enable and start the service.
```bash
sudo systemctl enable caps-to-esc.service
sudo systemctl start caps-to-esc.service
```
