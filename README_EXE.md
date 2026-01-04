# 🚀 Guía para Compilar WingetUpdater.exe

## ✅ Ejecutable Ya Creado

Tu aplicación ya está compilada en:
```
📁 C:\Bat\dist\WingetUpdater.exe
```
Tamaño: ~12 MB

## 🔧 Cómo Usar el Ejecutable

1. **Ejecutar como Administrador** (IMPORTANTE):
   - Clic derecho en `WingetUpdater.exe`
   - Seleccionar "Ejecutar como administrador"
   - O hacer doble clic (el programa pedirá permisos automáticamente)

2. **Distribuir**:
   - Puedes copiar `WingetUpdater.exe` a cualquier PC con Windows
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
pyinstaller --onefile --windowed --uac-admin --name="WingetUpdater" --clean winget_updater.py
```

### Método 3: Con Icono Personalizado
```bash
# 1. Consigue un archivo .ico (por ejemplo: icon.ico)
# 2. Colócalo en C:\Bat\
# 3. Ejecuta:
pyinstaller --onefile --windowed --uac-admin --icon=icon.ico --name="WingetUpdater" --clean winget_updater.py
```

## 📦 Opciones de PyInstaller Usadas

| Opción | Descripción |
|--------|-------------|
| `--onefile` | Crea un solo archivo .exe (portable) |
| `--windowed` | Sin ventana de consola (GUI pura) |
| `--uac-admin` | Solicita permisos de administrador automáticamente |
| `--name="WingetUpdater"` | Nombre del ejecutable |
| `--clean` | Limpia cache antes de compilar |
| `--icon=archivo.ico` | Añade un icono personalizado |

## 📂 Estructura de Archivos Generados

```
C:\Bat\
├── winget_updater.py          # Código fuente
├── build_exe.bat              # Script de compilación
├── WingetUpdater.spec         # Configuración de PyInstaller
├── build\                     # Archivos temporales (se puede borrar)
└── dist\
    └── WingetUpdater.exe      # ✅ EJECUTABLE FINAL
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
pyinstaller --onefile --console --uac-admin --name="WingetUpdater_Debug" --clean winget_updater.py
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
        StringStruct(u'FileDescription', u'Actualizador Winget Pro'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'WingetUpdater'),
        StringStruct(u'LegalCopyright', u'© 2026'),
        StringStruct(u'OriginalFilename', u'WingetUpdater.exe'),
        StringStruct(u'ProductName', u'Winget Updater'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Luego compila con:
```bash
pyinstaller --onefile --windowed --uac-admin --version-file=version.txt --name="WingetUpdater" winget_updater.py
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

Puedes subir `WingetUpdater.exe` a:
- GitHub Releases
- Google Drive
- OneDrive
- Tu propio servidor

---

**¡Listo! Tu aplicación ahora es un ejecutable profesional de Windows.** 🎉

