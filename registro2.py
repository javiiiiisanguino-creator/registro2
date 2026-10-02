import wx

VERDE_OSCURO = "#1b5e20"
VERDE_MEDIO = "#2e7d32"
VERDE_CLARO = "#43a047"
VERDE_ACENTO = "#66bb6a"
VERDE_PALIDO = "#e8f5e9"
BLANCO = "#ffffff"
GRIS_CLARO = "#f5f5f5"
GRIS_MEDIO = "#b0bec5"
GRIS_OSCURO = "#78909c"

FUENTE = "Segoe UI"


def fuente(tamano, negrita=False):
    peso = wx.FONTWEIGHT_BOLD if negrita else wx.FONTWEIGHT_NORMAL
    return wx.Font(tamano, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                   peso, False, FUENTE)


def color(hex_color):
    return wx.Colour(hex_color)


def fondo_boton(ancho, alto, color_fondo, texto, radio=8):
    """Dibuja el fondo redondeado del boton en un bitmap."""
    bmp = wx.Bitmap(ancho, alto)
    dc = wx.MemoryDC()
    dc.SelectObject(bmp)
    dc.SetBackground(wx.Brush(color(color_fondo)))
    dc.Clear()

    gc = wx.GraphicsContext.Create(dc)
    gc.SetPen(wx.Pen(color(color_fondo), 0))
    gc.SetBrush(wx.Brush(color(color_fondo)))
    gc.DrawRoundedRectangle(0, 0, ancho, alto, radio)

    dc.SetFont(fuente(10, True))
    dc.SetTextForeground(color(BLANCO))
    dc.SetTextBackground(color(color_fondo))
    dc.DrawLabel(texto, wx.Rect(0, 0, ancho, alto),
                 wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL)

    dc.SelectObject(wx.NullBitmap)
    del dc
    return bmp


class BotonAccion(wx.BitmapButton):
    """Boton nativo con fondo de color: siempre se dibuja y siempre responde."""

    def __init__(self, parent, texto, color_normal, color_hover, on_click):
        dc = wx.MemoryDC(wx.Bitmap(1, 1))
        dc.SetFont(fuente(10, True))
        ancho_texto, alto_texto = dc.GetTextExtent(texto)
        del dc

        ancho = ancho_texto + 56
        alto = max(44, alto_texto + 24)

        self._normal = fondo_boton(ancho, alto, color_normal, texto)
        self._hover = fondo_boton(ancho, alto, color_hover, texto)

        super().__init__(parent, bitmap=self._normal)
        self.SetBitmap(self._normal)
        self.SetToolTip(texto)
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.Bind(wx.EVT_BUTTON, on_click)
        self.Bind(wx.EVT_ENTER_WINDOW, self._entrar)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._salir)

    def _entrar(self, evento):
        self.SetBitmap(self._hover)
        evento.Skip()

    def _salir(self, evento):
        self.SetBitmap(self._normal)
        evento.Skip()


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Clinica Veterinaria Patitas Felices - Registro de Mascotas")
        self.SetBackgroundColour(color(GRIS_CLARO))
        area = wx.Display().GetClientArea()
        self.SetMinSize((700, 600))
        self.SetSize(min(840, max(area.width - 80, 700)),
                     min(780, max(area.height - 90, 600)))
        self.Centre()

        panel = wx.Panel(self)
        panel.SetBackgroundColour(color(GRIS_CLARO))
        self.CreateStatusBar()
        self.SetStatusWidths([-1])

        raiz = wx.BoxSizer(wx.VERTICAL)
        raiz.Add(self._cabecera(panel), 0, wx.EXPAND | wx.ALL, 12)

        self.libro = wx.Notebook(panel)
        self.libro.SetBackgroundColour(color(GRIS_CLARO))
        self.libro.SetFont(fuente(10, True))
        self.libro.AddPage(self._pagina_mascota(), "Datos de la Mascota")
        self.libro.AddPage(self._pagina_propietario(), "Propietario")
        self.libro.AddPage(self._pagina_salud(), "Salud y Vacunas")
        self.libro.AddPage(self._pagina_observaciones(), "Observaciones")
        raiz.Add(self.libro, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 12)

        botones = wx.BoxSizer(wx.HORIZONTAL)
        botones.AddStretchSpacer(1)
        botones.Add(BotonAccion(panel, "Cancelar", GRIS_MEDIO, GRIS_OSCURO,
                                self._cancelar), 0, wx.ALL, 6)
        botones.Add(BotonAccion(panel, "Limpiar", VERDE_ACENTO, VERDE_CLARO,
                                self._limpiar), 0, wx.ALL, 6)
        botones.Add(BotonAccion(panel, "Registrar Mascota", VERDE_MEDIO, VERDE_OSCURO,
                                self._registrar), 0, wx.ALL, 6)
        botones.AddStretchSpacer(1)
        raiz.Add(botones, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)

        pie = wx.StaticText(panel, label="Realizado por Javier Sanguino - 2026")
        pie.SetFont(fuente(9))
        pie.SetForegroundColour(color(VERDE_OSCURO))
        pie.SetBackgroundColour(color(VERDE_PALIDO))
        linea_pie = wx.BoxSizer(wx.HORIZONTAL)
        linea_pie.AddStretchSpacer(1)
        linea_pie.Add(pie, 0)
        linea_pie.AddStretchSpacer(1)
        raiz.Add(linea_pie, 0, wx.EXPAND | wx.ALL, 12)

        panel.SetSizer(raiz)
        panel.Layout()

    # ── Cabecera ────────────────────────────────────────────────
    def _cabecera(self, parent):
        cabecera = wx.Panel(parent)
        cabecera.SetBackgroundColour(color(VERDE_PALIDO))

        titulo = wx.StaticText(cabecera, label="Clinica Veterinaria Patitas Felices")
        titulo.SetFont(fuente(16, True))
        titulo.SetForegroundColour(color(VERDE_OSCURO))
        titulo.SetBackgroundColour(color(VERDE_PALIDO))

        subtitulo = wx.StaticText(cabecera, label="Formulario de Registro de Mascotas")
        subtitulo.SetFont(fuente(10))
        subtitulo.SetForegroundColour(color(VERDE_MEDIO))
        subtitulo.SetBackgroundColour(color(VERDE_PALIDO))

        interna = wx.BoxSizer(wx.VERTICAL)
        interna.Add(titulo, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 4)
        interna.Add(subtitulo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        cabecera.SetSizer(interna)
        return cabecera

    # ── Utilidades de armado ─────────────────────────────────────
    def _pagina(self):
        pag = wx.ScrolledWindow(self.libro, style=wx.TAB_TRAVERSAL | wx.VSCROLL)
        pag.SetScrollRate(14, 14)
        pag.SetBackgroundColour(color(BLANCO))
        self._pagina_actual = pag
        return pag

    def _etiqueta(self, parent, texto):
        etiqueta = wx.StaticText(parent, label=texto)
        etiqueta.SetFont(fuente(10, True))
        etiqueta.SetForegroundColour(color(VERDE_OSCURO))
        return etiqueta

    def _texto(self, parent, pista):
        campo = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
        campo.SetHint(pista)
        return campo

    def _combo(self, parent, opciones):
        combo = wx.ComboBox(parent, choices=opciones,
                            style=wx.CB_DROPDOWN | wx.CB_READONLY)
        combo.SetSelection(0)
        return combo

    def _agregar(self, grid, texto, control):
        grid.Add(self._etiqueta(self._pagina_actual, texto), 0,
                 wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        grid.Add(control, 1, wx.EXPAND)

    # ── Pagina 1: Datos de la Mascota ───────────────────────────
    def _pagina_mascota(self):
        pag = self._pagina()
        vertical = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(0, 2, 10, 8)
        grid.AddGrowableCol(1, 1)

        self.txt_nombre_mascota = self._texto(pag, "Ej. Firulais")
        self._agregar(grid, "Nombre:", self.txt_nombre_mascota)

        self.txt_raza = self._texto(pag, "Ej. Mestizo")
        self._agregar(grid, "Raza:", self.txt_raza)

        self.txt_fecha_nac = self._texto(pag, "DD/MM/AAAA")
        self._agregar(grid, "Fecha de nacimiento:", self.txt_fecha_nac)

        self.txt_peso = self._texto(pag, "Ej. 12.5")
        self._agregar(grid, "Peso (kg):", self.txt_peso)

        self.txt_color = self._texto(pag, "Color y senas distintivas")
        self._agregar(grid, "Color:", self.txt_color)

        self.txt_microchip = self._texto(pag, "Opcional")
        self._agregar(grid, "N. de microchip:", self.txt_microchip)

        self.txt_apodo = self._texto(pag, "Como lo llaman en casa")
        self._agregar(grid, "Apodo:", self.txt_apodo)

        vertical.Add(grid, 0, wx.EXPAND | wx.ALL, 18)

        self.radio_especie = wx.RadioBox(pag, label="Especie:",
                                        choices=["Seleccione...", "Perro", "Gato", "Ave",
                                                 "Roedor", "Reptil", "Otro"],
                                        majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.radio_sexo = wx.RadioBox(pag, label="Sexo:",
                                      choices=["Seleccione...", "Macho", "Hembra"],
                                      majorDimension=1, style=wx.RA_SPECIFY_COLS)

        fila_radios = wx.BoxSizer(wx.HORIZONTAL)
        for caja in (self.radio_especie, self.radio_sexo):
            caja.SetForegroundColour(color(VERDE_OSCURO))
            fila_radios.Add(caja, 1, wx.RIGHT, 12)
        vertical.Add(fila_radios, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 18)

        pag.SetSizer(vertical)
        return pag

    # ── Pagina 2: Propietario ───────────────────────────────────
    def _pagina_propietario(self):
        pag = self._pagina()
        vertical = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(0, 2, 10, 8)
        grid.AddGrowableCol(1, 1)

        self.txt_propietario = self._texto(pag, "Nombre completo del dueño")
        self._agregar(grid, "Propietario:", self.txt_propietario)

        self.txt_dpi = self._texto(pag, "N. de identificacion")
        self._agregar(grid, "DPI / ID:", self.txt_dpi)

        self.txt_telefono = self._texto(pag, "+502 0000-0000")
        self._agregar(grid, "Telefono:", self.txt_telefono)

        self.txt_email = self._texto(pag, "correo@ejemplo.com")
        self._agregar(grid, "Email:", self.txt_email)

        self.txt_direccion = self._texto(pag, "Direccion completa")
        self._agregar(grid, "Direccion:", self.txt_direccion)

        self.txt_municipio = self._texto(pag, "Municipio / Ciudad")
        self._agregar(grid, "Municipio:", self.txt_municipio)

        self.cbo_departamento = self._combo(pag, [
            "Seleccione...", "Guatemala", "Alta Verapaz", "Baja Verapaz",
            "Chimaltenango", "Chiquimula", "El Progreso", "Escuintla",
            "Huehuetenango", "Izabal", "Jalapa", "Jutiapa", "Petén",
            "Quetzaltenango", "Quiché", "Retalhuleu", "Sacatepéquez",
            "San Marcos", "Santa Rosa", "Sololá", "Suchitepéquez",
            "Totonicapán", "Zacapa"
        ])
        self._agregar(grid, "Departamento:", self.cbo_departamento)

        vertical.Add(grid, 0, wx.EXPAND | wx.ALL, 18)

        self.chk_email = wx.CheckBox(pag, label="Enviar recordatorios de vacuna por email")
        self.chk_sms = wx.CheckBox(pag, label="Enviar alertas de emergencia por SMS")
        for caja in (self.chk_email, self.chk_sms):
            caja.SetForegroundColour(color(VERDE_OSCURO))
            vertical.Add(caja, 0, wx.LEFT | wx.BOTTOM, 18)

        pag.SetSizer(vertical)
        return pag

    # ── Pagina 3: Salud y Vacunas ───────────────────────────────
    def _pagina_salud(self):
        pag = self._pagina()
        vertical = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(0, 2, 10, 8)
        grid.AddGrowableCol(1, 1)

        self.cbo_condicion = self._combo(pag, [
            "Seleccione...", "Excelente", "Buena", "Regular",
            "En tratamiento", "Critica", "Emergencia"
        ])
        self._agregar(grid, "Condicion general:", self.cbo_condicion)

        self.cbo_castracion = self._combo(pag, [
            "Seleccione...", "No castrado/a", "Castrado/a", "Pendiente"
        ])
        self._agregar(grid, "Castracion:", self.cbo_castracion)

        self.txt_ultima_visita = self._texto(pag, "DD/MM/AAAA")
        self._agregar(grid, "Ultima consulta:", self.txt_ultima_visita)

        self.txt_proxima_vacuna = self._texto(pag, "DD/MM/AAAA")
        self._agregar(grid, "Proxima vacuna:", self.txt_proxima_vacuna)

        self.txt_alergias = self._texto(pag, "Alergias o intolerancias conocidas")
        self._agregar(grid, "Alergias:", self.txt_alergias)

        self.txt_medicamentos = self._texto(pag, "Medicamentos o tratamientos actuales")
        self._agregar(grid, "Medicamentos actuales:", self.txt_medicamentos)

        vertical.Add(grid, 0, wx.EXPAND | wx.ALL, 18)

        vertical.Add(self._etiqueta(pag, "Vacunas administradas:"), 0,
                     wx.LEFT | wx.RIGHT | wx.BOTTOM, 18)

        lista_vacunas = [
            ("Hepatitis", "chk_vac_hepatitis"),
            ("Rabia", "chk_vac_rabia"),
            ("Parvovirus", "chk_vac_parvovirus"),
            ("Moquillo / Distemper", "chk_vac_moquillo"),
            ("Leucemia felina", "chk_vac_leucemia"),
            ("Desparasitacion", "chk_vac_desparasitacion"),
            ("Antipulgas", "chk_vac_antipulgas"),
            ("Ninguna", "chk_vac_ninguna"),
        ]
        cuadricula = wx.GridBagSizer(4, 2)
        cuadricula.SetVGap(8)
        cuadricula.SetHGap(16)
        for indice, (texto, atributo) in enumerate(lista_vacunas):
            caja = wx.CheckBox(pag, label=texto)
            caja.SetForegroundColour(color(VERDE_OSCURO))
            setattr(self, atributo, caja)
            cuadricula.Add(caja, (indice // 2, indice % 2))
        vertical.Add(cuadricula, 0, wx.ALL, 18)

        pag.SetSizer(vertical)
        return pag

    # ── Pagina 4: Observaciones ─────────────────────────────────
    def _pagina_observaciones(self):
        pag = self._pagina()
        vertical = wx.BoxSizer(wx.VERTICAL)

        self.txt_observaciones = wx.TextCtrl(pag, style=wx.TE_MULTILINE)
        self.txt_observaciones.SetHint(
            "Escriba aqui cualquier informacion adicional relevante...\n\n"
            "- Conducta y habitos de la mascota\n"
            "- Restricciones alimentarias\n"
            "- Notas del veterinario"
        )
        self.txt_observaciones.SetMinSize((-1, 170))
        vertical.Add(self.txt_observaciones, 1, wx.EXPAND | wx.ALL, 18)

        self.chk_terminos = wx.CheckBox(pag, label="Acepto los terminos y condiciones del servicio")
        self.chk_datos = wx.CheckBox(
            pag, label="Autorizo el tratamiento de mis datos personales")
        self.chk_procedimientos = wx.CheckBox(
            pag, label="Autorizo procedimientos, anestesia y hospitalizacion")
        self.chk_veracidad = wx.CheckBox(pag, label="Declaro que la informacion es veraz")

        for caja in (self.chk_terminos, self.chk_datos,
                     self.chk_procedimientos, self.chk_veracidad):
            caja.SetForegroundColour(color(VERDE_OSCURO))
            vertical.Add(caja, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        pag.SetSizer(vertical)
        return pag

    # ── Acciones ────────────────────────────────────────────────
    def _limpiar(self, evento=None):
        for control in self._controles(self):
            if isinstance(control, wx.TextCtrl):
                control.SetValue("")
            elif isinstance(control, wx.CheckBox):
                control.SetValue(False)
            elif isinstance(control, wx.ComboBox):
                control.SetSelection(0)
            elif isinstance(control, wx.RadioBox):
                control.SetSelection(0)
        self.libro.SetSelection(0)
        self.txt_nombre_mascota.SetFocus()

    def _controles(self, padre):
        encontrados = []
        for hijo in padre.GetChildren():
            if isinstance(hijo, (wx.TextCtrl, wx.CheckBox, wx.ComboBox, wx.RadioBox)):
                encontrados.append(hijo)
            encontrados.extend(self._controles(hijo))
        return encontrados

    def _cancelar(self, evento=None):
        respuesta = wx.MessageBox("Desea salir del registro?",
                                  "Confirmar salida",
                                  wx.YES_NO | wx.ICON_QUESTION, self)
        if respuesta == wx.YES:
            self.Close()

    def _registrar(self, evento=None):
        nombre = self.txt_nombre_mascota.GetValue().strip()
        propietario = self.txt_propietario.GetValue().strip()
        dpi = self.txt_dpi.GetValue().strip()

        if not nombre or not propietario or not dpi:
            wx.MessageBox("Complete el nombre de la mascota, el propietario y el DPI/ID.",
                          "Campos obligatorios", wx.OK | wx.ICON_WARNING, self)
            return

        if self.radio_especie.GetSelection() == 0:
            wx.MessageBox("Seleccione la especie de la mascota.",
                          "Especie requerida", wx.OK | wx.ICON_WARNING, self)
            self.libro.SetSelection(0)
            return

        peso = self.txt_peso.GetValue().strip().replace(",", ".")
        if peso:
            try:
                if float(peso) <= 0:
                    raise ValueError
            except ValueError:
                wx.MessageBox("El peso debe ser un numero positivo (ej. 12.5).",
                              "Peso invalido", wx.OK | wx.ICON_WARNING, self)
                self.libro.SetSelection(0)
                self.txt_peso.SetFocus()
                return

        if not self.chk_terminos.GetValue():
            wx.MessageBox("Debe aceptar los terminos y condiciones del servicio.",
                          "Terminos", wx.OK | wx.ICON_WARNING, self)
            self.libro.SetSelection(3)
            return

        especie = self.radio_especie.GetStringSelection()
        sexo = self.radio_sexo.GetStringSelection()
        self.SetStatusText(
            "Mascota '{0}' ({1}, {2}) registrada para {3}".format(
                nombre, especie, sexo.lower(), propietario))
        wx.MessageBox(
            "Mascota '{0}' registrada correctamente.\n\n"
            "Especie: {1}  |  Sexo: {2}\n"
            "Propietario: {3}\n"
            "DPI: {4}".format(nombre, especie, sexo.lower(), propietario, dpi),
            "Registro exitoso", wx.OK | wx.ICON_INFORMATION, self)
        self._limpiar()


if __name__ == "__main__":
    app = wx.App(False)
    ventana = MainWindow()
    ventana.Show()
    app.MainLoop()
