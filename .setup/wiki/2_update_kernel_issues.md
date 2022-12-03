# Probleme bei Kernel-Aktualisierungen
Mögliche Auslöser:
- Defekte Stromvsorgung verursacht unterbrochenen Aktualisierungsprozess
- Neues Paket ist womöglich fehlerhaft (manchmal bei Arch-Wiki nicht rechtzeitig dokumentiert, z.B. Grub)

Das führt zu unvollständige Kernel-Installationen, die das System nicht erkennt. Entweder lädt das System das Kernel nicht oder fällt die Ramdisk Initialisierung aus.

## Arch-chroot
Mit einem Archiso-Stick den Computer neustarten. Mit 
```
lsblk
```

die Systempartitionen suchen. Für EFI-Systeme sollte auch die EFI-Partition identifiziert werden. 
```
lsblk -f 
```

kann Abhilfe leisten. Die Systempartitionen montieren und mit Arch-chroot zugreifen:
```
sudo mount /dev/nvme-main /mnt
sudo mount /dev/nvme-efi /mnt/boot/efi
arch-chroot /mnt
```

Forten wird angenommen, dass Root-Rechte und Internetzugang bestehen. 

## Erneut aktualisieren
Das System in der chroot-Umgebung aktualisieren lassen. Vor allem auf Warnungen und Hinweisen bei wiederholter Kernel-Installation achten.
```
pacman -Syyu
```

Einen anderen Kernel installieren als Failsafe (z.B. linux-lts falls nicht vorhanden, oder umgekehrt auch linux). 

# Ramdisk-Initialisierung ausfällt
Eventuell sind die preset-Dateien während fehlerhafter Aktualisierung beschädigt. 

1. Mit
    ```
    mkinitcpio -P
    ```

    überprüfen, welche Presets beschädigt bzw. leer sind. Die Ausgabe dieses Befehls offenbart auch welcher Kernel damit betroffen ist.
2. Die beschädigte Presets löschen.
3. Die entsprechende Kernel reinstallieren. Der Vorgang regeneriert die Presets.
4. Computer neu starten.

# Leere Bibliothek-Dateien
Ein unterbrochener Aktualisierungsvorgang führt eventuell zu beschädigten bzw. leeren lib-Dateien. Diese Dateien werden in der Aktualisierungsausgabe gemeldet. Die Dateien sollen gelöscht werden. 

Die Dateien befinden sich unter /usr/lib. Treten mehrere solchen Meldungen auf, die gemeldete Dateien aufnehmen und per Skript löschen. Ein Beispiel (python).
```
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
