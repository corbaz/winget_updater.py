import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import re
import sys
import ctypes
import os
from tkinter import font as tkFont

def is_admin():
    """Verifica si el script se ejecuta como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-ejecuta el script como administrador"""
    if not is_admin():
        # Re-ejecutar con privilegios de administrador
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

class WingetUpdater:
    def __init__(self, root):
        self.root = root
        self.root.title("Actualizador de Aplicaciones - Winget [ADMIN]")
        self.root.geometry("1400x750")
        self.root.minsize(1000, 600)
        
        # Colores profesionales
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_light': '#2d2d2d',
            'accent_blue': '#0d47a1',
            'accent_green': '#2e7d32',
            'accent_red': '#c62828',
            'text_primary': '#ffffff',
            'text_secondary': '#b0bec5',
            'border': '#424242',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336'
        }
        
        # Configurar estilo
        self._setup_styles()
        
        # Configurar fondo
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Variables
        self.apps_data = []
        self.checkboxes = []
        self.checkbox_vars = []
        
        # Encabezado
        self._create_header()
        
        # Frame superior para botones
        top_frame = tk.Frame(root, bg=self.colors['bg_light'], height=70)
        top_frame.pack(fill=tk.X, padx=0, pady=0)
        top_frame.pack_propagate(False)
        
        button_container = tk.Frame(top_frame, bg=self.colors['bg_light'])
        button_container.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.scan_btn = self._create_button(button_container, "🔄 Buscar Actualizaciones", 
                                            self.scan_updates, self.colors['accent_blue'])
        self.scan_btn.pack(side=tk.LEFT, padx=8)
        
        self.select_btn = self._create_button(button_container, "✓ Seleccionar Todas", 
                                              self.select_all, self.colors['accent_green'])
        self.select_btn.pack(side=tk.LEFT, padx=8)
        
        self.deselect_btn = self._create_button(button_container, "✗ Deseleccionar Todas", 
                                                self.deselect_all, self.colors['error'])
        self.deselect_btn.pack(side=tk.LEFT, padx=8)
        
        self.update_btn = self._create_button(button_container, "⚡ Actualizar Seleccionadas", 
                                              self.update_selected, self.colors['accent_green'])
        self.update_btn.pack(side=tk.LEFT, padx=8)
        
        # Frame para la lista de aplicaciones
        list_frame = tk.Frame(root, bg=self.colors['bg_dark'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        list_label = tk.Label(list_frame, text="📦 Aplicaciones Disponibles para Actualizar", 
                              bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                              font=('Segoe UI', 12, 'bold'))
        list_label.pack(anchor='w', pady=(0, 8))
        
        # Canvas con scrollbar para los checkboxes
        canvas_frame = tk.Frame(list_frame, bg=self.colors['bg_light'], highlightthickness=1,
                                highlightbackground=self.colors['border'])
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=self.colors['bg_light'], highlightthickness=0,
                          width=1350)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=1350)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Hacer que el frame se adapte al ancho del canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind('<Configure>', on_canvas_configure)

        # Habilitar scroll con rueda del ratón
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Encabezados de columnas
        header_frame = tk.Frame(self.scrollable_frame, bg=self.colors['accent_blue'])
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        header_frame.configure(height=40)

        header_font = tkFont.Font(family='Segoe UI', size=10, weight='bold')
        
        tk.Label(header_frame, text="☑", bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'], font=header_font, width=3).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Label(header_frame, text="Aplicación", bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'], font=header_font, anchor='w').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Label(header_frame, text="Versión Actual", bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'], font=header_font, anchor='center', width=18).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="→", bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'], font=header_font, anchor='center', width=2).pack(side=tk.LEFT, padx=2)
        tk.Label(header_frame, text="Versión Nueva", bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'], font=header_font, anchor='center', width=18).pack(side=tk.LEFT, padx=5)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para el log
        log_frame = tk.Frame(root, bg=self.colors['bg_dark'])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        log_label = tk.Label(log_frame, text="📋 Log de Actualizaciones", 
                             bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 12, 'bold'))
        log_label.pack(anchor='w', pady=(0, 8))
        
        log_container = tk.Frame(log_frame, bg=self.colors['bg_light'], highlightthickness=1,
                                 highlightbackground=self.colors['border'])
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_container, height=8, wrap=tk.WORD,
                                                   bg=self.colors['bg_light'], 
                                                   fg=self.colors['text_primary'],
                                                   font=('Consolas', 9),
                                                   insertbackground=self.colors['accent_blue'],
                                                   relief=tk.FLAT, borderwidth=0)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Status bar
        self.status_var = tk.StringVar(value="Listo. Haz clic en 'Buscar Actualizaciones' para comenzar.")
        status_bar = tk.Label(root, textvariable=self.status_var, relief=tk.FLAT,
                             bg=self.colors['bg_light'], fg=self.colors['text_secondary'],
                             font=('Segoe UI', 9), padx=15, pady=8, anchor='w')
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.log("✅ Aplicación iniciada con privilegios de ADMINISTRADOR.")
        self.log("📋 Bienvenido al Actualizador de Winget Moderno.")
    
    def _setup_styles(self):
        """Configura los estilos de ttk"""
        style = ttk.Style()
        
        # Tema oscuro
        style.theme_use('clam')
        
        # Configurar colores para Scrollbar
        style.configure('Vertical.TScrollbar',
                       background=self.colors['bg_light'],
                       troughcolor=self.colors['bg_light'],
                       bordercolor=self.colors['border'],
                       darkcolor=self.colors['accent_blue'],
                       lightcolor=self.colors['accent_blue'])
    
    def _create_header(self):
        """Crea un encabezado personalizado"""
        header = tk.Frame(self.root, bg=self.colors['accent_blue'], height=50)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_font = tkFont.Font(family='Segoe UI', size=16, weight='bold')
        title_label = tk.Label(header, text="⚙️  Actualizador Winget Pro", 
                              bg=self.colors['accent_blue'], fg=self.colors['text_primary'],
                              font=title_font, padx=15)
        title_label.pack(side=tk.LEFT, pady=8)
    
    def _create_button(self, parent, text, command, color):
        """Crea un botón personalizado con colores"""
        button = tk.Button(parent, text=text, command=command,
                          bg=color, fg=self.colors['text_primary'],
                          font=('Segoe UI', 10, 'bold'),
                          padx=12, pady=8, relief=tk.FLAT,
                          cursor='hand2', activebackground=color,
                          activeforeground=self.colors['text_primary'],
                          bd=0)
        button.pack(side=tk.LEFT, padx=4)
        
        # Efecto hover
        button.bind('<Enter>', lambda e: button.config(bg=self._lighten_color(color)))
        button.bind('<Leave>', lambda e: button.config(bg=color))
        
        return button
    
    def _lighten_color(self, color):
        """Aclara un color hexadecimal"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def log(self, message):
        """Agrega un mensaje al log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def scan_updates(self):
        """Escanea las actualizaciones disponibles"""
        self.status_var.set("Escaneando actualizaciones...")
        self.log("\n" + "="*50)
        self.log("Buscando actualizaciones disponibles...")
        
        thread = threading.Thread(target=self._scan_updates_thread)
        thread.daemon = True
        thread.start()
    

    def _scan_updates_thread(self):
        """Thread para escanear actualizaciones"""
        try:
            # Ejecutar winget upgrade
            result = subprocess.run(
                ["winget", "upgrade", "--include-unknown"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Mostrar salida completa en log para debugging
            self.root.after(0, lambda: self.log("--- Salida de Winget ---"))
            output_lines = result.stdout.split('\n')
            for line in output_lines[:15]:  # Mostrar primeras 15 líneas
                if line.strip():
                    self.root.after(0, lambda l=line: self.log(l))

            # Parsear la salida
            self.apps_data = []
            lines = result.stdout.split('\n')
            
            # Encontrar tabla en la salida
            header_idx = -1
            separator_idx = -1

            # Búsqueda del encabezado
            for i, line in enumerate(lines):
                if ('Nombre' in line or 'Name' in line) and 'Id' in line:
                    header_idx = i
                    # Buscar separador en la siguiente línea
                    if i + 1 < len(lines) and re.search(r'-{20,}', lines[i + 1]):
                        separator_idx = i + 1
                    break

            if header_idx >= 0 and separator_idx >= 0:
                self.root.after(0, lambda: self.log("📊 Tabla detectada"))

                # Procesar líneas de datos
                for data_line in lines[separator_idx + 1:]:
                    line_stripped = data_line.strip()

                    if not line_stripped or any(kw in line_stripped.lower() for kw in ['actualizaciones', 'updates']):
                        continue
                    
                    # Dividir por espacios múltiples
                    parts = re.split(r'\s{2,}', line_stripped)

                    if len(parts) >= 4:
                        name, app_id, current, available = parts[0], parts[1], parts[2], parts[3]

                        # Validaciones básicas
                        if name and app_id and current and available and '.' in app_id:
                            self.apps_data.append({
                                'name': name.strip(),
                                'id': app_id.strip(),
                                'current_version': current.strip(),
                                'available_version': available.strip()
                            })
                            self.root.after(0, lambda n=name, c=current, a=available:
                                          self.log(f"  ✓ {n}: {c} → {a}"))
            else:
                self.root.after(0, lambda: self.log("⚠️  No se encontró tabla de aplicaciones"))

            # Actualizar UI
            self.root.after(0, self._update_app_list)
            
        except FileNotFoundError:
            self.root.after(0, lambda: self.log("❌ ERROR: winget no encontrado"))
            self.root.after(0, lambda: self.status_var.set("Error: winget no encontrado"))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"❌ ERROR: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Error al escanear"))


    def _update_app_list(self):
        """Actualiza la lista de aplicaciones en la UI"""
        # DEBUG
        self.log(f"\n🔍 DEBUG: _update_app_list llamado con {len(self.apps_data)} aplicaciones")

        # Limpiar lista anterior (excepto encabezados)
        for widget in self.scrollable_frame.winfo_children()[1:]:  # Saltar header
            widget.destroy()
        
        self.checkboxes = []
        self.checkbox_vars = []
        
        if not self.apps_data:
            self.log("\n⚠️  No se encontraron aplicaciones para actualizar.")
            self.log("   - Revisa que winget esté correctamente instalado")
            self.log("   - Verifica la conexión a internet")
            self.status_var.set("❌ No hay actualizaciones disponibles")

            # Mostrar mensaje en la lista
            empty_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_light'])
            empty_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

            empty_label = tk.Label(empty_frame,
                                  text="📭 No hay aplicaciones para actualizar",
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['text_secondary'],
                                  font=('Segoe UI', 12))
            empty_label.pack(expand=True)
            return
        
        # DEBUG: Mostrar las apps que se van a procesar
        self.log(f"🔧 DEBUG: Procesando {len(self.apps_data)} aplicaciones:")
        for idx, app in enumerate(self.apps_data):
            self.log(f"  [{idx}] {app.get('name', 'N/A')} - {app.get('id', 'N/A')}")

        # Crear filas para cada aplicación
        for i, app in enumerate(self.apps_data):
            # Frame para cada fila con alternancia de colores
            bg_color = self.colors['bg_light'] if i % 2 == 0 else '#252525'
            row_frame = tk.Frame(self.scrollable_frame, bg=bg_color, height=40)
            row_frame.pack(fill=tk.X, padx=0, pady=0)
            row_frame.pack_propagate(False)

            # Checkbox
            var = tk.BooleanVar()
            self.checkbox_vars.append(var)
            cb = tk.Checkbutton(row_frame, variable=var,
                               bg=bg_color, fg=self.colors['text_primary'],
                               activebackground=bg_color, activeforeground=self.colors['accent_blue'],
                               selectcolor=bg_color, relief=tk.FLAT, bd=0)
            cb.pack(side=tk.LEFT, padx=5, pady=8)
            self.checkboxes.append(cb)
            
            # Nombre de la aplicación (ancho: 500px)
            name_label = tk.Label(row_frame, text=app['name'][:50], anchor='w',
                                 bg=bg_color, fg=self.colors['text_primary'],
                                 font=('Segoe UI', 10), width=50)
            name_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            # Versión actual (ancho fijo: 150px)
            current_label = tk.Label(row_frame, text=app['current_version'], anchor='center',
                                    bg=bg_color, fg=self.colors['text_secondary'],
                                    font=('Consolas', 9), width=18)
            current_label.pack(side=tk.LEFT, padx=5)
            
            # Flecha (ancho fijo)
            arrow_label = tk.Label(row_frame, text="→", anchor='center',
                                  bg=bg_color, fg=self.colors['success'],
                                  font=('Segoe UI', 10, 'bold'), width=2)
            arrow_label.pack(side=tk.LEFT, padx=2)
            
            # Versión disponible (ancho fijo: 150px)
            available_label = tk.Label(row_frame, text=app['available_version'], anchor='center',
                                      bg=bg_color, fg=self.colors['accent_blue'],
                                      font=('Consolas', 9, 'bold'), width=18)
            available_label.pack(side=tk.LEFT, padx=5)
        
        self.log(f"\n✅ Se encontraron {len(self.apps_data)} aplicaciones para actualizar.")
        self.status_var.set(f"✅ {len(self.apps_data)} actualizaciones disponibles")

    def select_all(self):
        """Selecciona todas las aplicaciones"""
        for var in self.checkbox_vars:
            var.set(True)
        self.log("Todas las aplicaciones seleccionadas.")
    
    def deselect_all(self):
        """Deselecciona todas las aplicaciones"""
        for var in self.checkbox_vars:
            var.set(False)
        self.log("Todas las aplicaciones deseleccionadas.")
    
    def update_selected(self):
        """Actualiza las aplicaciones seleccionadas"""
        selected = []
        for i, var in enumerate(self.checkbox_vars):
            if var.get():
                selected.append(self.apps_data[i])
        
        if not selected:
            messagebox.showwarning("Advertencia", "No hay aplicaciones seleccionadas.")
            return
        
        # Confirmar
        response = messagebox.askyesno(
            "Confirmar Actualización",
            f"¿Deseas actualizar {len(selected)} aplicación(es)?\n\nEsto puede tardar varios minutos."
        )
        
        if not response:
            return
        
        self.log("\n" + "="*50)
        self.log(f"Iniciando actualización de {len(selected)} aplicación(es)...")
        self.status_var.set("Actualizando...")
        
        thread = threading.Thread(target=self._update_apps_thread, args=(selected,))
        thread.daemon = True
        thread.start()
    
    def _update_apps_thread(self, selected_apps):
        """Thread para actualizar aplicaciones"""
        success_count = 0
        fail_count = 0
        failed_apps = []

        # Primera pasada: actualizar sin --force
        self.root.after(0, lambda: self.log(f"\n🔄 PRIMERA PASADA: Actualizando {len(selected_apps)} aplicación(es)..."))

        for app in selected_apps:
            self.root.after(0, lambda a=app: self.log(f"\n📦 Actualizando: {a['name']}..."))
            
            try:
                result = subprocess.run(
                    ["winget", "upgrade", "--id", app['id'], "--accept-package-agreements", "--accept-source-agreements"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=300
                )
                
                if result.returncode == 0:
                    self.root.after(0, lambda a=app: self.log(f"✅ {a['name']} actualizado correctamente"))
                    success_count += 1
                else:
                    self.root.after(0, lambda a=app, r=result: self.log(f"❌ Error al actualizar {a['name']}: {r.stderr[:100]}"))
                    failed_apps.append(app)
                    fail_count += 1
                    
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda a=app: self.log(f"⏱️  Timeout al actualizar {a['name']}"))
                failed_apps.append(app)
                fail_count += 1
            except Exception as e:
                self.root.after(0, lambda a=app, e=e: self.log(f"❌ Error con {a['name']}: {str(e)}"))
                failed_apps.append(app)
                fail_count += 1
        
        # Segunda pasada: reintentar con --force si hubo fallos
        if failed_apps:
            self.root.after(0, lambda: self.log(f"\n{'='*50}"))
            self.root.after(0, lambda: self.log(f"🔄 SEGUNDA PASADA: Reintentando {len(failed_apps)} aplicación(es) con --force..."))
            self.root.after(0, lambda: self.log(f"{'='*50}\n"))

            retry_success = 0
            retry_fail = 0
            still_failed = []

            for app in failed_apps:
                self.root.after(0, lambda a=app: self.log(f"\n📦 Reintentando: {a['name']} (con --force)..."))

                try:
                    result = subprocess.run(
                        ["winget", "upgrade", "--id", app['id'], "--accept-package-agreements", "--accept-source-agreements", "--force"],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        timeout=300
                    )

                    if result.returncode == 0:
                        self.root.after(0, lambda a=app: self.log(f"✅ {a['name']} actualizado correctamente (reintentos)"))
                        retry_success += 1
                        success_count += 1
                        fail_count -= 1
                    else:
                        self.root.after(0, lambda a=app, r=result: self.log(f"❌ Falló nuevamente {a['name']}: {r.stderr[:100]}"))
                        still_failed.append(app)
                        retry_fail += 1

                except subprocess.TimeoutExpired:
                    self.root.after(0, lambda a=app: self.log(f"⏱️  Timeout al reintentar {a['name']}"))
                    still_failed.append(app)
                    retry_fail += 1
                except Exception as e:
                    self.root.after(0, lambda a=app, e=e: self.log(f"❌ Error reintentando {a['name']}: {str(e)}"))
                    still_failed.append(app)
                    retry_fail += 1

            # Resumen de reintentos
            self.root.after(0, lambda: self.log(f"\n{'='*50}"))
            self.root.after(0, lambda: self.log(f"📊 RESUMEN SEGUNDA PASADA:"))
            self.root.after(0, lambda: self.log(f"   ✅ Exitosas en reintento: {retry_success}"))
            self.root.after(0, lambda: self.log(f"   ❌ Aún fallidas: {retry_fail}"))

            # Tercera pasada: desinstalar e instalar si aún hay fallos
            if still_failed:
                self.root.after(0, lambda: self.log(f"\n{'='*50}"))
                self.root.after(0, lambda: self.log(f"🔄 TERCERA PASADA: Desinstalar/Reinstalar {len(still_failed)} aplicación(es)..."))
                self.root.after(0, lambda: self.log(f"{'='*50}\n"))

                third_success = 0
                third_fail = 0

                for app in still_failed:
                    self.root.after(0, lambda a=app: self.log(f"\n📦 Desinstalando: {a['name']}..."))

                    try:
                        # Desinstalar
                        uninstall_result = subprocess.run(
                            ["winget", "uninstall", "--id", app['id'], "--accept-source-agreements"],
                            capture_output=True,
                            text=True,
                            encoding='utf-8',
                            errors='replace',
                            timeout=300
                        )

                        if uninstall_result.returncode == 0:
                            self.root.after(0, lambda a=app: self.log(f"   ✅ {a['name']} desinstalado"))
                        else:
                            self.root.after(0, lambda a=app: self.log(f"   ⚠️  {a['name']} con advertencia en desinstalación"))

                        # Instalar
                        self.root.after(0, lambda a=app: self.log(f"📥 Instalando: {a['name']}..."))
                        install_result = subprocess.run(
                            ["winget", "install", "--id", app['id'], "--accept-package-agreements", "--accept-source-agreements"],
                            capture_output=True,
                            text=True,
                            encoding='utf-8',
                            errors='replace',
                            timeout=300
                        )

                        if install_result.returncode == 0:
                            self.root.after(0, lambda a=app: self.log(f"✅ {a['name']} reinstalado correctamente"))
                            third_success += 1
                            success_count += 1
                            fail_count -= 1
                        else:
                            self.root.after(0, lambda a=app, r=install_result: self.log(f"❌ Error al reinstalar {a['name']}: {r.stderr[:100]}"))
                            third_fail += 1

                    except subprocess.TimeoutExpired:
                        self.root.after(0, lambda a=app: self.log(f"⏱️  Timeout en desinstalación/instalación de {a['name']}"))
                        third_fail += 1
                    except Exception as e:
                        self.root.after(0, lambda a=app, e=e: self.log(f"❌ Error con {a['name']}: {str(e)}"))
                        third_fail += 1

                # Resumen tercera pasada
                self.root.after(0, lambda: self.log(f"\n{'='*50}"))
                self.root.after(0, lambda: self.log(f"📊 RESUMEN TERCERA PASADA:"))
                self.root.after(0, lambda: self.log(f"   ✅ Reinstaladas correctamente: {third_success}"))
                self.root.after(0, lambda: self.log(f"   ❌ Fallos en reinstalación: {third_fail}"))

        # Resumen final general
        self.root.after(0, lambda: self.log("\n" + "="*50))
        self.root.after(0, lambda: self.log(f"📊 RESUMEN FINAL:"))
        self.root.after(0, lambda: self.log(f"   ✅ Total exitosas: {success_count}"))
        self.root.after(0, lambda: self.log(f"   ❌ Total fallidas: {fail_count}"))
        self.root.after(0, lambda: self.log(f"   📈 Tasa de éxito: {(success_count / len(selected_apps) * 100):.1f}%"))
        self.root.after(0, lambda: self.status_var.set(f"Completado: {success_count} exitosas, {fail_count} fallidas"))
        
        # Mostrar resultado final
        if success_count > 0:
            self.root.after(0, lambda: messagebox.showinfo(
                "Actualización Completa",
                f"Proceso de actualización completado.\n\n✅ Exitosas: {success_count}\n❌ Fallidas: {fail_count}\n📈 Éxito: {(success_count / len(selected_apps) * 100):.1f}%"
            ))

if __name__ == "__main__":
    # Verificar y solicitar privilegios de administrador
    if not is_admin():
        print("⚠️ Ejecutando como administrador...")
        run_as_admin()
    else:
        root = tk.Tk()
        app = WingetUpdater(root)
        root.mainloop()