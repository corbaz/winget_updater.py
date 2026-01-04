# ⚙️ Win-Upgrade

<div align="center">

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Actualizador moderno y elegante para aplicaciones de Windows usando Winget**

[Descargar .exe](#-descarga-directa) • [Documentación](#-uso) • [Compilar](#-compilar-desde-código-fuente)

</div>

---

## 📋 Descripción

**Win-Upgrade** es una interfaz gráfica moderna y profesional para gestionar actualizaciones de aplicaciones en Windows usando `winget`. Olvídate de la línea de comandos y actualiza todas tus aplicaciones con un par de clics.

### ✨ Características

- 🎨 **Interfaz Moderna**: Diseño oscuro profesional con colores vibrantes
- ⚡ **Actualización Masiva**: Selecciona y actualiza múltiples aplicaciones a la vez
- 🔄 **Sistema Inteligente de Reintentos**: 3 intentos automáticos con diferentes estrategias
- 📊 **Vista Clara**: Columnas bien organizadas con versiones actual y nueva
- 🔐 **Ejecuta como Admin**: Solicita permisos automáticamente
- 📝 **Log Detallado**: Registro completo de todas las operaciones
- 🎯 **Sin Instalación**: Ejecutable portable

### 🖼️ Capturas de Pantalla

```
┌─────────────────────────────────────────────────────┐
│  ⚙️  Actualizador Winget Pro                       │
├─────────────────────────────────────────────────────┤
│  [🔄 Buscar] [✓ Seleccionar] [✗ Deseleccionar]     │
│  [⚡ Actualizar Seleccionadas]                      │
├─────────────────────────────────────────────────────┤
│ 📦 Aplicaciones Disponibles para Actualizar        │
│  ☑ | Aplicación           | Actual  → Nueva        │
│  ✓ | Google Chrome        | 120.0.1 → 120.0.2      │
│  ✓ | Visual Studio Code   | 1.85.0  → 1.85.1       │
│  ✓ | Python               | 3.11.0  → 3.12.0       │
├─────────────────────────────────────────────────────┤
│ 📋 Log de Actualizaciones                          │
│  ✅ Buscando actualizaciones...                     │
│  ✅ Se encontraron 3 aplicaciones                   │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Descarga Directa

### Opción 1: Ejecutable (.exe) - Recomendado

**📦 [Descargar win-upgrade.exe](https://github.com/corbaz/winget_updater.py/releases)**

- ✅ No requiere Python instalado
- ✅ Portable (un solo archivo)
- ✅ Listo para usar
- ✅ Icono personalizado de Windows
- 📏 Tamaño: ~12 MB

### Opción 2: Código Fuente (.py)

```bash
git clone https://github.com/corbaz/winget_updater.py.git
cd winget_updater.py
python winget_updater.py
```

**Requisitos:**
- Python 3.7+
- tkinter (incluido con Python)
- Windows 10/11 con winget instalado

---

## 💻 Uso

### Ejecutar el Programa

1. **Desde el .exe**:
   - Clic derecho en `win-upgrade.exe`
   - "Ejecutar como administrador"
   - ¡Listo!

2. **Desde el código Python**:
   ```bash
   python winget_updater.py
   ```

### Cómo Funciona

1. **Buscar Actualizaciones**: Clic en "🔄 Buscar Actualizaciones"
2. **Seleccionar Apps**: Marca las aplicaciones que quieres actualizar
3. **Actualizar**: Clic en "⚡ Actualizar Seleccionadas"
4. **Esperar**: El programa actualizará todo automáticamente

### Sistema de Reintentos Inteligente

El programa usa 3 estrategias si una actualización falla:

1. **Primera Pasada**: Actualización normal
2. **Segunda Pasada**: Actualización con `--force` (sobrescribe archivos)
3. **Tercera Pasada**: Desinstala y reinstala la aplicación

Esto maximiza las probabilidades de éxito.

---

## 🛠️ Compilar desde Código Fuente

### Requisitos

```bash
pip install pyinstaller
```

### Compilación Rápida

**Opción 1: Script Automático**
```bash
# En Windows:
build_exe.bat
```

**Opción 2: Comando Manual**
```bash
pyinstaller --onefile --windowed --uac-admin --icon=win-upgrade.ico --name="win-upgrade" --clean --add-data="win-upgrade.ico;." winget_updater.py
```

El ejecutable se generará en: `dist/win-upgrade.exe`

### Opciones de Compilación

| Opción | Descripción |
|--------|-------------|
| `--onefile` | Un solo archivo .exe |
| `--windowed` | Sin ventana de consola |
| `--uac-admin` | Pide permisos de admin |
| `--icon=icon.ico` | Añade icono personalizado |
| `--clean` | Limpia caché antes de compilar |

📖 **Guía completa**: Ver [README_EXE.md](README_EXE.md)

---

## 📁 Estructura del Proyecto

```
winget_updater.py/
│
├── winget_updater.py        # Código fuente principal
├── win-upgrade.ico          # Icono personalizado
├── create_icon.py           # Script para crear el icono
├── build_exe.bat            # Script de compilación
├── README.md                # Este archivo
├── README_EXE.md            # Guía detallada de compilación
├── .gitignore               # Archivos excluidos de Git
│
├── dist/                    # Ejecutable compilado
│   └── win-upgrade.exe
│
└── build/                   # Archivos temporales (ignorados)
```

---

## 🎨 Características Técnicas

### Interfaz de Usuario

- **Framework**: Tkinter (nativo de Python)
- **Diseño**: Material Design Dark
- **Colores**: Paleta profesional con acentos azules y verdes
- **Fuentes**: Segoe UI, Consolas
- **Responsive**: Se adapta a diferentes tamaños de ventana

### Funcionalidades

- ✅ Detección automática de actualizaciones con `winget upgrade`
- ✅ Parsing inteligente de la salida de winget
- ✅ Actualización en segundo plano con threads
- ✅ Sistema de logs en tiempo real
- ✅ Reintentos automáticos con 3 estrategias
- ✅ Manejo de errores robusto
- ✅ Indicadores de progreso y estado

### Requisitos del Sistema

- 💻 Windows 10/11 (64-bit)
- 📦 Winget instalado ([instalar aquí](https://aka.ms/getwinget))
- 🔐 Permisos de administrador

---

## 🐛 Solución de Problemas

### El programa no encuentra aplicaciones

**Causa**: Winget no está instalado o no funciona correctamente.

**Solución**:
```bash
# Verificar winget
winget --version

# Si no funciona, instalar desde:
# https://aka.ms/getwinget
```

### El .exe no inicia

**Causa**: Antivirus bloqueando el ejecutable.

**Solución**:
- Añadir excepción en el antivirus
- Usar la versión de Python directamente

### Aplicaciones no se actualizan

**Causa**: La aplicación está en uso o permisos insuficientes.

**Solución**:
- Cerrar la aplicación antes de actualizar
- Ejecutar como administrador
- El programa reintentará automáticamente

---

## 📝 Changelog

### v1.0.0 (2026-01-04)
- 🎉 Lanzamiento inicial
- ✨ Interfaz gráfica moderna
- ⚡ Sistema de actualización masiva
- 🔄 Sistema inteligente de reintentos (3 intentos)
- 📊 Vista de columnas con versiones
- 📝 Log detallado de operaciones
- 🔐 Ejecución automática como administrador

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar este proyecto:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añadir mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

### Ideas de Mejoras

- [ ] Añadir opción de actualización automática programada
- [ ] Notificaciones de escritorio
- [ ] Exportar lista de aplicaciones instaladas
- [ ] Tema claro/oscuro configurable
- [ ] Múltiples idiomas
- [ ] Integración con Chocolatey
- [ ] Historial de actualizaciones

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Corbaz**

- 🐙 GitHub: [@corbaz](https://github.com/corbaz)
- 📧 Email: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)

---

## ⭐ Agradecimientos

- A Microsoft por [Winget](https://github.com/microsoft/winget-cli)
- A la comunidad de Python
- A todos los que usan y mejoran esta herramienta

---

## 🔗 Enlaces Útiles

- [Winget Documentation](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
- [PyInstaller](https://pyinstaller.org/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐**

Made with ❤️ and Python

</div>

