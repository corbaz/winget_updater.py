# 🚀 Guía para Compilar win-upgrade.exe

## ✅ Ejecutable Ya Creado

Tu aplicación ya está compilada en:
```
📁 C:\Bat\dist\win-upgrade.exe
```
Tamaño: ~12 MB

## 🔧 Cómo Usar el Ejecutable

1. **Ejecutar como Administrador** (IMPORTANTE):
   - Clic derecho en `win-upgrade.exe`
   - Seleccionar "Ejecutar como administrador"
   - O hacer doble clic (el programa pedirá permisos automáticamente)

2. **Distribuir**:
   - Puedes copiar `win-upgrade.exe` a cualquier PC con Windows
   - No necesita Python instalado
   - No necesita instalación

## 🔨 Recompilar (si modificas el código)

### Método 1: Script Automático (Recomendado)
```bash
# Hacer doble clic en:
build_exe.bat
```

### Método 2: Línea de Comandos
```bash
cd C:\Bat
pyinstaller --onefile --windowed --uac-admin --icon=win-upgrade.ico --name="win-upgrade" --clean --add-data="win-upgrade.ico;." winget_updater.py
```

### Método 3: Con Icono Personalizado
El icono ya está incluido (`win-upgrade.ico`). Si quieres crear uno diferente:
```bash
# 1. Edita create_icon.py para personalizar el diseño
# 2. Ejecuta:
python create_icon.py

# 3. Compila:
pyinstaller --onefile --windowed --uac-admin --icon=win-upgrade.ico --name="win-upgrade" --clean --add-data="win-upgrade.ico;." winget_updater.py
```

## 📦 Opciones de PyInstaller Usadas

| Opción | Descripción |
|--------|-------------|
| `--onefile` | Crea un solo archivo .exe (portable) |
| `--windowed` | Sin ventana de consola (GUI pura) |
| `--uac-admin` | Solicita permisos de administrador automáticamente |
| `--name="win-upgrade"` | Nombre del ejecutable |
| `--icon=win-upgrade.ico` | Añade el icono personalizado |
| `--clean` | Limpia cache antes de compilar |
| `--add-data="win-upgrade.ico;."` | Incluye el icono en el ejecutable |

## 📂 Estructura de Archivos Generados

```
C:\Bat\
├── winget_updater.py          # Código fuente
├── win-upgrade.ico            # Icono personalizado
├── create_icon.py             # Script para crear el icono
├── build_exe.bat              # Script de compilación
├── win-upgrade.spec           # Configuración de PyInstaller
├── build\                     # Archivos temporales (se puede borrar)
└── dist\
    └── win-upgrade.exe        # ✅ EJECUTABLE FINAL
```

## 🎯 Ventajas del .exe

✅ **Portable**: No necesita Python instalado
✅ **Fácil distribución**: Un solo archivo
✅ **Profesional**: Se ve como una aplicación nativa
✅ **Permisos de admin**: Se solicitan automáticamente
✅ **Sin dependencias**: Incluye todo lo necesario

## ⚠️ Notas Importantes

1. **Antivirus**: Algunos antivirus pueden marcar el .exe como sospechoso (falso positivo). Esto es normal con ejecutables empaquetados.

2. **Tamaño**: El .exe es grande (~12 MB) porque incluye:
   - Intérprete de Python
   - Tkinter y todas las librerías
   - Tu código

3. **Actualizaciones**: Si modificas `winget_updater.py`, debes recompilar el .exe.

4. **Compatibilidad**: El .exe solo funciona en Windows (compilado en Windows).

## 🔄 Crear Versión con Consola (Debug)

Si quieres ver mensajes de error:
```bash
pyinstaller --onefile --console --uac-admin --icon=win-upgrade.ico --name="win-upgrade-debug" --clean winget_updater.py
```

## 📝 Agregar Información de Versión

Puedes crear un archivo `version.txt` con información de versión:
```python
# version.txt
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Tu Nombre'),
        StringStruct(u'FileDescription', u'Win-Upgrade - Actualizador Winget'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'win-upgrade'),
        StringStruct(u'LegalCopyright', u'© 2026'),
        StringStruct(u'OriginalFilename', u'win-upgrade.exe'),
        StringStruct(u'ProductName', u'Win-Upgrade'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Luego compila con:
```bash
pyinstaller --onefile --windowed --uac-admin --version-file=version.txt --icon=win-upgrade.ico --name="win-upgrade" winget_updater.py
```

## 🆘 Solución de Problemas

### El .exe no inicia
- Prueba la versión con consola para ver errores
- Verifica que winget esté instalado en el sistema destino

### Antivirus lo bloquea
- Añade excepción en tu antivirus
- Firma el ejecutable (requiere certificado)

### Es muy grande
- Opción alternativa: `--onedir` crea una carpeta con el .exe más pequeño

## 📧 Compartir el Ejecutable

Puedes subir `win-upgrade.exe` a:
- GitHub Releases
- Google Drive
- OneDrive
- Tu propio servidor

---

**¡Listo! Tu aplicación ahora es un ejecutable profesional de Windows.** 🎉

