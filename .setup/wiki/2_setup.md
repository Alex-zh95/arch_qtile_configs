# Arch-Linux
Nach einer frischen Installation des Arch-Linux-Systems sollte die Arco-Repositorien importiert werden. Auf der folgenden Webseite das Paket arcolinux-spices herunterladen:

[Arco-Linux Spices](https://www.arcolinux.info/arcolinux-spices-application/)

Eine Lokalinstallation durchführen:
```shell
sudo pacman -U /heruntergeladene/Datei
```

Arcolinux-spices ausführen, um die Arco-Repos zu aktivieren. Dann pacman auffrischen. 

## Pakete installieren
Voreingestellte Pakete sind in `Package_list/packages.x86_64` vorgegeben. AUR-Helper yay wird dabei mitinstalliert. 
```shell
cd /Pfad/zu/.setup/Package_list/
./installer.py
```

# Probleme bei Kernel-Aktualisierungen
Mögliche Auslöser:
- Defekte Stromvsorgung verursacht unterbrochenen Aktualisierungsprozess
- Neues Paket ist womöglich fehlerhaft (manchmal bei Arch-Wiki nicht rechtzeitig dokumentiert, z.B. Grub)

Das führt zu unvollständige Kernel-Installationen, die das System nicht erkennt. Entweder lädt das System das Kernel nicht oder fällt die Ramdisk Initialisierung aus.

## Arch-chroot
Mit einem Archiso-Stick den Computer neustarten. Mit 
```shell
lsblk
```

die Systempartitionen suchen. Für EFI-Systeme sollte auch die EFI-Partition identifiziert werden. 
```shell
lsblk -f 
```

kann Abhilfe leisten. Die Systempartitionen montieren und mit Arch-chroot zugreifen:
```shell
sudo mount /dev/nvme-main /mnt
sudo mount /dev/nvme-efi /mnt/boot/efi
arch-chroot /mnt
```

Forten wird angenommen, dass Root-Rechte und Internetzugang bestehen. 

## Erneut aktualisieren
Das System in der chroot-Umgebung aktualisieren lassen. Vor allem auf Warnungen und Hinweisen bei wiederholter Kernel-Installation achten.
```shell
pacman -Syyu
```

Einen anderen Kernel installieren als Failsafe (z.B. linux-lts falls nicht vorhanden, oder umgekehrt auch linux). 

# Ramdisk-Initialisierung ausfällt
Eventuell sind die preset-Dateien während fehlerhafter Aktualisierung beschädigt. 

1. Mit
    ```shell
    mkinitcpio -P
    ```

    überprüfen, welche Presets beschädigt bzw. leer sind. Die Ausgabe dieses Befehls offenbart auch welcher Kernel damit betroffen ist.
2. Die beschädigte Presets löschen.
3. Die entsprechende Kernel reinstallieren. Der Vorgang regeneriert die Presets.
4. Computer neu starten.

# Leere Bibliothek-Dateien
Ein unterbrochener Aktualisierungsvorgang führt eventuell zu beschädigten bzw. leeren lib-Dateien. Diese Dateien werden in der Aktualisierungsausgabe gemeldet. Die Dateien sollen gelöscht werden. 

Die Dateien befinden sich unter /usr/lib. Treten mehrere solchen Meldungen auf, die gemeldete Dateien aufnehmen und per Skript löschen. Ein Beispiel (python).
```python
import re
import subprocess

# Angenommen, dass die Dateiname bzw. Pfade in einer lokalen Textdatei namens "output.txt" gespeichert sind...
file = open('output.txt', 'r')
lines = readlines(file)

for line in lines:
    l = re.sub('\\n', '', line)
    print(f'Deleting {l}...')
    subprocess.run(['sudo', 'rm', l])

print('Done.')
file.close()
```

# Vim-Jupyter
Zweck ist, die Nutzung von VS Code und andere MS-Produkte abzunehmen. Ein Jupyter-Workflow hilft dabei Python-Skripte zu debuggen bzw. individuelle Code-Snippets zu testen.

- [Jupyter-vim](https://github.com/jupyter-vim/jupyter-vim) lässt sich in Github abrufen. Integrieren kann mit vim-plug. Überprüfe die [.vimrc-Konfigurationsdatei](~/.vimrc).
- Jede Umegebung muss mit Jupyter augestattet sein. Mit pipenv jupyter installieren, denn in einer Umgebung wird auf nicht voreingestellte Pakete nicht zugegriffen.

## Ersteinrichtung
1. Voreingestellte Konfigurationsdatei generieren.
    ```shell
    jupyter console --generate-config
    ```
2. Outputs aus anderen Clients einschalten. Dazu die folgende Zeile in die [Konfig-datei](~/.jupyter/jupyter_console_config.py)
 hinzufügen:
    ```python
    c.ZMQTerminalInteractiveShell.include_other_output = True
    ```
    
## Konsole vorbereiten
1. Eine neue Konsole-Sitzung ausführen:
    ```shell
    pipenv shell
    jupyter console 
    ```
2. Dann in einer anderen terminal-Sitzung die Python-Datei öffnen.
3. Jupyter-Vim Kurzbefehle finden sich in der [.vimrc-Datei](~/.vimrc)
