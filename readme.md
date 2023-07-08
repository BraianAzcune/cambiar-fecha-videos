
Icon by <a href="https://freeicons.io/profile/3484">BECRIS</a> on <a href="https://freeicons.io">freeicons.io</a>


https://doc.qt.io/qtforpython-6/quickstart.html#faq-section


`pip freeze > requirements.txt`

Activate env
`./env/Scripts/Activate.ps1`
Execute main
`python src/main.py`

Crear ejecutable
```bash
# modo productivo
pyinstaller --distpath=".\dist" --onefile --noconsole --add-data "3792137161586787349-128.png;." --name "cambiar-fechas" ".\src\main.py"
# modo con consola, para ver que hace
pyinstaller --distpath=".\dist" --onefile --icon ".\3792137161586787349-128.ico" --name "cambiar-fechas" ".\src\main.py"
```
