
"""Notification Studio — Tkinter demo of the Bridge design pattern."""

import tkinter as tk
from tkinter import ttk

from bridge import CHANNELS, NOTIFICATIONS, dispatch


# Application colors
BG = '#0d1220'
PANEL = '#161e2e'
FIELD = '#202b3d'
LINE = '#2d3c51'
TEXT = '#edf3fc'
MUTED = '#9eafc7'
ACCENT = '#8a91ff'
SUCCESS = '#5fe0ad'


class Studio(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Notification Studio  •  Bridge Pattern')
        self.geometry('1060x725')
        self.minsize(870, 640)
        self.configure(bg=BG)

        # Application state
        self.type_var = tk.StringVar(value='Standard')
        self.channel_var = tk.StringVar(value='Email')
        self.recipient_var = tk.StringVar(value='alex@example.com')
        self.subject_var = tk.StringVar(value='Service update')

        self.count = 0

        # Push popup state
        self._toast = None
        self._toast_timer = None

        self._style()
        self._build()
        self._update_bridge()
        self._update_preview()

    # -------------------------------------------------------
    # STYLING
    # -------------------------------------------------------

    def _style(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure(
            'Studio.TCombobox',
            fieldbackground=FIELD,
            background=FIELD,
            foreground=TEXT,
            arrowcolor=TEXT,
            padding=7,
            bordercolor=LINE
        )

        style.map(
            'Studio.TCombobox',
            fieldbackground=[('readonly', FIELD)],
            foreground=[('readonly', TEXT)],
            selectbackground=[('readonly', FIELD)],
            selectforeground=[('readonly', TEXT)]
        )

        self.option_add('*TCombobox*Listbox.background', FIELD)
        self.option_add('*TCombobox*Listbox.foreground', TEXT)
        self.option_add('*TCombobox*Listbox.selectBackground', '#535da5')
        self.option_add('*TCombobox*Listbox.selectForeground', 'white')

    def _label(
        self,
        parent,
        text,
        size=11,
        color=TEXT,
        weight='normal',
        **kw
    ):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget('bg'),
            fg=color,
            font=('DejaVu Sans', size, weight),
            **kw
        )

    def _panel(self, parent):
        return tk.Frame(
            parent,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=LINE
        )

    def _input_label(self, parent, text, row, col):
        self._label(
            parent, text, 9, MUTED, 'bold'
        ).grid(
            row=row,
            column=col,
            sticky='w',
            padx=(0, 8)
        )

    def _entry(self, parent, var):
        return tk.Entry(
            parent,
            textvariable=var,
            bg=FIELD,
            fg=TEXT,
            insertbackground=TEXT,
            font=('DejaVu Sans', 10),
            relief='flat',
            highlightthickness=1,
            highlightbackground=LINE,
            highlightcolor=ACCENT
        )

    def _button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground='#adb3ff',
            activeforeground='#0a1020',
            relief='flat',
            padx=14,
            pady=12,
            cursor='hand2',
            font=('DejaVu Sans', 9, 'bold')
        )

    # -------------------------------------------------------
    # MAIN WINDOW
    # -------------------------------------------------------

    def _build(self):
        outer = tk.Frame(
            self,
            bg=BG,
            padx=28,
            pady=23
        )
        outer.pack(fill='both', expand=True)

        heading = tk.Frame(outer, bg=BG)
        heading.pack(fill='x', pady=(0, 23))

        self._label(
            heading,
            '◈  NOTIFICATION STUDIO',
            19,
            TEXT,
            'bold'
        ).pack(anchor='w')

        self._label(
            heading,
            'Bridge design pattern  /  interactive simulator',
            10,
            MUTED
        ).pack(anchor='w', pady=(6, 0))

        tk.Frame(
            outer,
            bg=ACCENT,
            height=2
        ).pack(fill='x', pady=(0, 20))

        columns = tk.Frame(outer, bg=BG)
        columns.pack(fill='both', expand=True)

        columns.grid_columnconfigure(0, weight=3)
        columns.grid_columnconfigure(1, weight=2)
        columns.grid_rowconfigure(0, weight=1)

        left = self._panel(columns)
        left.grid(
            row=0,
            column=0,
            sticky='nsew',
            padx=(0, 10)
        )

        right = self._panel(columns)
        right.grid(
            row=0,
            column=1,
            sticky='nsew',
            padx=(10, 0)
        )

        self._composer(left)
        self._inspector(right)

        bottom = tk.Frame(outer, bg=BG)
        bottom.pack(fill='x', pady=(14, 0))

        self.status = self._label(
            bottom,
            '●  Ready to simulate delivery',
            10,
            SUCCESS
        )
        self.status.pack(side='left')

        self.counter = self._label(
            bottom,
            '0 messages simulated',
            10,
            MUTED
        )
        self.counter.pack(side='right')

    # -------------------------------------------------------
    # NOTIFICATION COMPOSER
    # -------------------------------------------------------

    def _composer(self, parent):
        content = tk.Frame(
            parent,
            bg=PANEL,
            padx=22,
            pady=18
        )
        content.pack(fill='both', expand=True)

        self._label(
            content,
            'COMPOSE NOTIFICATION',
            13,
            TEXT,
            'bold'
        ).pack(anchor='w', pady=(0, 5))

        self._label(
            content,
            'Choose a notification and a delivery mechanism.',
            9,
            MUTED
        ).pack(anchor='w', pady=(0, 17))

        choices = tk.Frame(content, bg=PANEL)
        choices.pack(fill='x')

        choices.grid_columnconfigure(0, weight=1)
        choices.grid_columnconfigure(1, weight=1)

        self._input_label(
            choices, 'NOTIFICATION TYPE', 0, 0
        )
        self._input_label(
            choices, 'DELIVERY CHANNEL', 0, 1
        )

        types = ttk.Combobox(
            choices,
            values=list(NOTIFICATIONS),
            textvariable=self.type_var,
            state='readonly',
            style='Studio.TCombobox'
        )
        types.grid(
            row=1,
            column=0,
            sticky='ew',
            padx=(0, 8),
            pady=(7, 14)
        )

        methods = ttk.Combobox(
            choices,
            values=list(CHANNELS),
            textvariable=self.channel_var,
            state='readonly',
            style='Studio.TCombobox'
        )
        methods.grid(
            row=1,
            column=1,
            sticky='ew',
            padx=(8, 0),
            pady=(7, 14)
        )

        types.bind(
            '<<ComboboxSelected>>',
            self._selection_changed
        )
        methods.bind(
            '<<ComboboxSelected>>',
            self._selection_changed
        )

        self._label(
            content,
            'RECIPIENT / DEVICE',
            9,
            MUTED,
            'bold'
        ).pack(anchor='w', pady=(0, 5))

        self._entry(
            content,
            self.recipient_var
        ).pack(fill='x', pady=(0, 15))

        self._label(
            content,
            'SUBJECT',
            9,
            MUTED,
            'bold'
        ).pack(anchor='w', pady=(0, 5))

        self._entry(
            content,
            self.subject_var
        ).pack(fill='x', pady=(0, 15))

        self._label(
            content,
            'MESSAGE BODY',
            9,
            MUTED,
            'bold'
        ).pack(anchor='w', pady=(0, 5))

        self.message = tk.Text(
            content,
            bg=FIELD,
            fg=TEXT,
            insertbackground=TEXT,
            selectbackground='#525e9f',
            relief='flat',
            padx=11,
            pady=10,
            font=('DejaVu Sans', 10),
            wrap='word',
            height=7,
            highlightthickness=1,
            highlightbackground=LINE
        )

        self.message.insert(
            '1.0',
            'We will perform a scheduled maintenance window '
            'tonight at 23:00. Services may briefly be unavailable.'
        )

        self.message.pack(
            fill='both',
            expand=True,
            pady=(0, 18)
        )

        buttons = tk.Frame(content, bg=PANEL)
        buttons.pack(fill='x')

        self._button(
            buttons,
            'SEND SIMULATED NOTIFICATION',
            self._send,
            ACCENT,
            '#0a1020'
        ).pack(
            side='left',
            fill='x',
            expand=True,
            padx=(0, 9)
        )

        self._button(
            buttons,
            'Clear',
            self._clear,
            FIELD,
            TEXT
        ).pack(side='left')

    # -------------------------------------------------------
    # BRIDGE INSPECTOR
    # -------------------------------------------------------

    def _inspector(self, parent):
        c = tk.Frame(
            parent,
            bg=PANEL,
            padx=19,
            pady=18
        )
        c.pack(fill='both', expand=True)

        self._label(
            c,
            'BRIDGE INSPECTOR',
            13,
            TEXT,
            'bold'
        ).pack(anchor='w')

        self._label(
            c,
            'See how two hierarchies connect.',
            9,
            MUTED
        ).pack(anchor='w', pady=(5, 15))

        self._label(
            c,
            'ABSTRACTION',
            9,
            ACCENT,
            'bold'
        ).pack(anchor='w')

        self.abstraction = self._label(
            c, '', 11, TEXT, 'bold'
        )
        self.abstraction.pack(
            anchor='w',
            pady=(4, 10)
        )

        self._label(
            c,
            '    │',
            13,
            MUTED
        ).pack(anchor='w')

        self._label(
            c,
            '    └── delegates to ──▶',
            10,
            MUTED
        ).pack(anchor='w')

        self._label(
            c,
            'IMPLEMENTATION',
            9,
            SUCCESS,
            'bold'
        ).pack(anchor='w', pady=(10, 0))

        self.implementation = self._label(
            c, '', 11, TEXT, 'bold'
        )
        self.implementation.pack(
            anchor='w',
            pady=(4, 13)
        )

        tk.Frame(
            c,
            height=1,
            bg=LINE
        ).pack(fill='x', pady=12)

        self._label(
            c,
            'DELIVERY PREVIEW',
            10,
            TEXT,
            'bold'
        ).pack(anchor='w', pady=(0, 10))

        self.preview = tk.Text(
            c,
            bg=FIELD,
            fg=TEXT,
            relief='flat',
            padx=10,
            pady=10,
            font=('DejaVu Sans Mono', 9),
            wrap='word',
            height=10,
            highlightthickness=1,
            highlightbackground=LINE,
            state='disabled'
        )
        self.preview.pack(
            fill='both',
            expand=True
        )

        self._label(
            c,
            'SIMULATED — no real emails or messages are sent.',
            8,
            MUTED
        ).pack(anchor='w', pady=(10, 0))

    # -------------------------------------------------------
    # SELECTION AND PREVIEW
    # -------------------------------------------------------

    def _selection_changed(self, _event=None):
        defaults = {
            'Email': 'alex@example.com',
            'SMS': '+37060000000',
            'Push': 'device-042'
        }

        self.recipient_var.set(
            defaults[self.channel_var.get()]
        )

        self._update_bridge()
        self._update_preview()

    def _update_bridge(self):
        self.abstraction.config(
            text=self.type_var.get() + 'Notification'
        )

        self.implementation.config(
            text=self.channel_var.get() + 'Channel'
        )

    def _set_preview(self, text):
        self.preview.config(state='normal')
        self.preview.delete('1.0', 'end')
        self.preview.insert('1.0', text)
        self.preview.config(state='disabled')

    def _update_preview(self):
        try:
            result = dispatch(
                self.type_var.get(),
                self.channel_var.get(),
                self.recipient_var.get(),
                self.subject_var.get(),
                self.message.get('1.0', 'end-1c')
            )

            self._set_preview(
                result.rendered_message
            )

        except (KeyError, tk.TclError):
            pass

    # -------------------------------------------------------
    # SENDING NOTIFICATIONS
    # -------------------------------------------------------

    def _send(self):
        destination = self.recipient_var.get().strip()
        subject = self.subject_var.get().strip()
        body = self.message.get('1.0', 'end-1c').strip()

        if not destination or not subject or not body:
            self.status.config(
                text='●  Please fill in recipient, subject and message',
                fg='#ffb981'
            )
            return

        # Bridge pattern processes the notification
        result = dispatch(
            self.type_var.get(),
            self.channel_var.get(),
            destination,
            subject,
            body
        )

        # Show the result in the inspector
        self._set_preview(
            result.rendered_message
        )

        # Update statistics
        self.count += 1

        self.counter.config(
            text=f'{self.count} message(s) simulated'
        )

        self.status.config(
            text=(
                f'●  {result.channel} delivery simulated '
                f'at {result.delivered_at}'
            ),
            fg=SUCCESS
        )

        # Only Push notifications produce a popup
        if result.channel == 'Push':
            self._show_push_popup(
                subject,
                result.rendered_message
            )

    # -------------------------------------------------------
    # PUSH NOTIFICATION POPUP
    # -------------------------------------------------------

    def _dismiss_push_popup(self):
        """Remove the current push popup."""

        if self._toast_timer is not None:
            self.after_cancel(self._toast_timer)
            self._toast_timer = None

        if self._toast is not None:
            self._toast.destroy()
            self._toast = None

    def _show_push_popup(self, subject: str, message: str):
        """Display an in-app push notification."""

        # Remove previous notification
        self._dismiss_push_popup()

        # Main popup frame
        toast = tk.Frame(
            self,
            bg='#273650',
            highlightbackground=ACCENT,
            highlightthickness=2
        )

        self._toast = toast

        # Position in upper-right corner
        toast.place(
            relx=1.0,
            x=-23,
            y=76,
            anchor='ne',
            width=350
        )

        toast.lift()

        # Popup header
        header = tk.Frame(
            toast,
            bg='#273650'
        )

        header.pack(
            fill='x',
            padx=14,
            pady=(12, 5)
        )

        tk.Label(
            header,
            text='●  NEW PUSH NOTIFICATION',
            bg='#273650',
            fg=SUCCESS,
            font=('DejaVu Sans', 9, 'bold')
        ).pack(side='left')

        # Close button
        tk.Button(
            header,
            text='✕',
            command=self._dismiss_push_popup,
            bg='#273650',
            fg=TEXT,
            activebackground=FIELD,
            activeforeground=TEXT,
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            font=('DejaVu Sans', 11)
        ).pack(side='right')

        # Notification subject
        tk.Label(
            toast,
            text=subject,
            bg='#273650',
            fg=TEXT,
            font=('DejaVu Sans', 11, 'bold'),
            anchor='w',
            wraplength=315,
            justify='left'
        ).pack(
            fill='x',
            padx=14,
            pady=(3, 6)
        )

        # Notification message
        tk.Label(
            toast,
            text=message,
            bg='#273650',
            fg='#c6d4e7',
            font=('DejaVu Sans', 9),
            anchor='w',
            justify='left',
            wraplength=315
        ).pack(
            fill='x',
            padx=14,
            pady=(0, 14)
        )

        # Dismiss automatically after 5.5 seconds
        self._toast_timer = self.after(
            5500,
            self._dismiss_push_popup
        )

    # -------------------------------------------------------
    # CLEAR COMPOSER
    # -------------------------------------------------------

    def _clear(self):
        self.subject_var.set('')
        self.message.delete('1.0', 'end')
        self._set_preview('')

        self.status.config(
            text='●  Composer cleared',
            fg=MUTED
        )


# -----------------------------------------------------------
# APPLICATION ENTRY POINT
# -----------------------------------------------------------

if __name__ == '__main__':
    Studio().mainloop()
