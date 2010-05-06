class Configurable(object):
    
    
    def __init__(self):
        self.connect(self, SIGNAL("settings_changed()"), self.on_reconfigure)


    def reconfigure(self, **settings):
        try:
            self.settings.update(settings)
        except AttributeError, e:
            try:
                self.settings = jdict(self.default_settings)
            except AttributeError, e:
                self.settings = jdict()
            self.settings.update(settings)
        self.emit(SIGNAL("settings_changed()"))


    def on_reconfigure(self):
        pass


class Hookable(object):
    
    
    def setup_hooks(self):
        self.state = 0
        self.commands = {}
        self.keyboard_hooks = {}
        self.mouse_press_hooks = {}
        self.mouse_double_click_hooks = {}
        self.paint_hooks = self.paint_hooks_before = {}
        self.paint_hooks_after = {}
        self.resize_hooks = {}
        self.contents_change_hooks = {}
        self.cursor_movement_hooks = {}
        self.row_change_hooks = {}
        # These variables fill be filled with hooks for current state
        self._commands = []
        self.active_paint_hooks_before = self.active_paint_hooks_after = ()
        self.active_resize_hooks = ()
        self.active_cursor_movement_hooks = ()
        self.active_row_change_hooks = ()

        
        self.state = -1
        self.installed_modes = []

        
    def prepare_hooks(self):
        for cmd in self._commands:
            self.removeAction(cmd)

        self._commands = self.commands.get(self.state, [])
        for cmd in self._commands:
            self.addAction(cmd)

        def filter_active_state(hooks):
            return list(hooks.get(self.state, []) + hooks.get(-1, []))

        self._mouse_press_hooks = filter_active_state(self.mouse_press_hooks)
        
        self._mouse_double_click_hooks = filter_active_state(self.mouse_double_click_hooks)
        self._paint_hooks_before = filter_active_state(self.paint_hooks_before)
        self._paint_hooks_after = filter_active_state(self.paint_hooks_after)
        self._contents_change_hooks = filter_active_state(self.contents_change_hooks)
        self._cursor_movement_hooks = filter_active_state(self.cursor_movement_hooks)
        self._row_change_hooks = filter_active_state(self.row_change_hooks)
        self._resize_hooks = filter_active_state(self.resize_hooks)

        h = self._keyboard_hooks = dict()
        for state in (self.state, -1):
            for keys, callbacks in self.keyboard_hooks.get(state, {}).items():
                h.setdefault(keys, []).extend(callbacks)
   

    def find_mode(self, cls):
        for mode in self.installed_modes:
            if isinstance(mode, cls):
                return mode


    def is_installed(self, mode):
        for installed in self.installed_modes:
            if installed.__class__ is mode:
                return True
        return False


    def _find_modes(self, *mode_args):
        for m in mode_args:
            mode = ModeBase.find_implementation(m)
            if not mode:
                raise ValueError, "Installing mode %r failed: Not found." % m
            yield mode


    def install(self, *mode_list):
        for mode in self._find_modes(*mode_list):
            if not self.is_installed(mode):
                mode_instance = mode(self)
                self.installed_modes.append(mode_instance)
                setattr(self, mode.__name__, mode_instance)
        self.switch_state(0)

    require = install #alias for emacs fans ;)

    
    def install_on_idle(self, *mode_list, **kwargs):
        callback = kwargs.pop("callback", None)
        self.idle_install = IdleCall(self, self.install, callback, *mode_list, **kwargs)


    def uninstall(self, *mode_list):
        for mode in self._find_modes(*mode_list):
            for instance in self.installed_modes:
                if isinstance(instance, mode):
                    instance.uninstall()
                    delattr(self, instance.__class__.__name__)
                    self.installed_modes.remove(instance)
                    break


    def switch_state(self, state):
        """
        changes the state and set hooks for current state
        """
        self.emit(SIGNAL("state_change(int)"), state)
        self.state = state
        self.prepare_hooks()
        self.update_hooks()
        self.emit(SIGNAL("new_state()"))

class Buffer(QTextDocument, Hookable, Configurable):

    killring = []
    registers = []
    instances =  []


    @classmethod
    def get(cls, idx):
        if isinstance(idx, basestring):
            for buf in cls.instances:
                if buf.filename == idx:
                    return bux
        return cls.instances[idx]


    def __init__(self, text=None, filename=None):
        QTextDocument.__init__(self)
        Hookable.__init__(self)
        Configurable.__init__(self)
        self.filename = filename
        if text is None and filename and os.path.exists(filename):
            text = open(filename).read()
        self.plain_text_layout = QPlainTextDocumentLayout(self)
        self.setDocumentLayout(self.plain_text_layout)
        if text:
            self.setPlainText(text)
        self.setModified(False)
        Buffer.instances.append(self)
        self.setup_hooks()
        #self.install("Autosave")

        
    def document(self):
        return self # work-around...


    def close(self):
        Buffer.instances.remove(self)


    def max_line_length(self):
        lines = unicode(self.toPlainText()).splitlines()
        return max([len(l) for l in lines])


    def row_col2position(self, row, col):
        """
        index starts with 0
        """
        block = self.findBlockByNumber(row)
        return block.position() + col


    def row2position(self, row):
        return self.row_col2position(row, 0)


class Idler(QObject):
    # XXX make seconds configurable?


    def __init__(self, textedit):
        QObject.__init__(self, textedit)
        self.textedit = textedit
        self.idle_timer_id = self.startTimer(1000)


    def busy(self):
        self.killTimer(self.idle_timer_id)
        self.idle_timer_id = self.startTimer(1000)


    def timerEvent(self, event):
        self.killTimer(self.idle_timer_id)
        QTimer.singleShot(0, self._emit_idle)
        self.idle_timer_id = self.startTimer(1000)


    def _emit_idle(self):
        self.textedit.emit(SIGNAL("idle()"))
        