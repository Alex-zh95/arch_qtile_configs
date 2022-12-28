# Vim-Anpassungen
Die Mehrheit der vim-Anpassungen befinden sich in der .vimrc-Datei. Auf sonstige Änderungen wird hier detaillierter eingegangen.

## Conquer of Completion (Coc)
Siehe [neoclide/coc.nvim](https://github.com/neoclide/coc.nvim).

### Einrichtungsschritte
1. Abhängigkeit 'nodejs' installieren. Erwriterungen zu Coc brauchen javascript.
2. Coc lässt sich wie üblich in vim hinzufügen. Mittels vim-plug die Zeile
    ```vimL
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
    ```
    in der .vimrc-Datei hinzufügen.

Voreingestellt sind keine weiteren Tastenkürzeln verfügbar. Aktuelle .vimrc-Datei enthält vorgeschlagene Betätigungen.

Jede Code-Sprache braucht eigene LSP-Engines - für einige Sprachen sind vorgefertigte Pakete bereitgestellt:
```shell
# Python
:CocInstall coc-pyright

# LaTeX
:CocInstall coc-vimtex
```

Für andere Sprachen kann LSPs manuall verlinkt werden. Folgendes Beispiel für C++:
1. Sprachenserver installieren ("ccls" oder "clangd")
2. Config-Datei auto-generieren und zugreifen mittels
    ```
    :CocConfig
    ```
3. Den folgenden JSON-Code in die Config-Datei einfügen:
    ```json
    {
        "languageserver": {
          "ccls": {
            "command": "ccls",
            "filetypes": ["c", "cc", "cpp", "c++", "objc", "objcpp"],
            "rootPatterns": [".ccls", "compile_commands.json", ".git/", ".hg/"],
            "initializationOptions": {
                "cache": {
                  "directory": "/tmp/ccls"
                }
              }
          }
        }
    }
    ```
4. In der Projektverzeichnis eine .ccls-Datei erstellen und dazu:
    ```shell
    clang++
    %h %cpp -std=c++17
    ```
    Das schaltet C++17 ein.
