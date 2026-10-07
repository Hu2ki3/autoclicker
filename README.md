# Autoclicker

Ein einfacher Autoclicker fuer Linux mit Tkinter-GUI, Hotkey-Steuerung und
randomisierten Klickintervallen.

Gedacht zur Automatisierung eigener, wiederkehrender Arbeitsschritte.

## Features

- Start/Stopp per Hotkey, ohne Fensterwechsel
- Zufaelliges Intervall zwischen einstellbarem Min- und Max-Wert
- Optionaler Pixel-Jitter (0-5 px) via `xdotool`
- Klickzaehler
- Sauberes Beenden von GUI und Threads

## Hotkeys

| Taste | Funktion |
|-------|----------|
| `F9`  | Start / Stopp |
| `F10` | Programm beenden |
| `F11` | Klickzaehler zuruecksetzen |

## Voraussetzungen

- Python 3
- `pynput`
- `xdotool` (nur fuer den Pixel-Jitter)
- Tkinter (bei manchen Distributionen ein separates Paket)

### Installation (Arch / CachyOS)

```
sudo pacman -S python xdotool tk
pip install -r requirements.txt
```

### Installation (Debian / Ubuntu)

```
sudo apt install python3 python3-tk xdotool
pip install -r requirements.txt
```

## Start

```
python autoclicker.py
```

## Hinweise und bekannte Einschraenkungen

- **Wayland:** Der Pixel-Jitter nutzt `xdotool` und damit das X11-Protokoll.
  Ob das unter Wayland funktioniert, haengt vom Compositor ab. Getestet und
  funktionsfaehig unter CachyOS/Wayland mit XWayland. Auf anderen Setups kann
  die Bewegung stillschweigend ausbleiben; die Klicks selbst funktionieren
  weiterhin. Jitter laesst sich mit Wert 0 abschalten.
- **Jitter-Drift:** Die Bewegung erfolgt relativ ohne Rueckkehr zur
  Startposition. Ueber viele Klicks wandert der Cursor dadurch langsam weg.
- Der globale Hotkey-Listener erfasst Tastendruecke systemweit, nicht nur im
  Programmfenster.

## Lizenz

MIT - siehe [LICENSE](LICENSE).
