import os
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from data_manager import CocktailDataManager
from serial_manager import SerialManager

class MainPage(ttk.Frame):
    def __init__(self, parent, data_manager,serial_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.serial_manager = serial_manager 
        self.current_sort = ("Name", "Aufsteigend")
        self.theme = "light"
        self.setup_widgets()
        self.update_list()
        self.initial_selection()

    def setup_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        left_frame = ttk.Frame(self, padding=10, style="Card.TFrame")
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        self.setup_search(left_frame)
        self.setup_sort_controls(left_frame)
        self.setup_listbox(left_frame)

        self.setup_details_panel()
        self.setup_action_buttons()

    def setup_search(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=(0, 10))
        ttk.Label(frame, text="Suche:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=self.search_var)
        entry.pack(fill="x", expand=True)
        entry.bind("<KeyRelease>", self.filter_list)

    def setup_sort_controls(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=10)
        ttk.Label(frame, text="Sortieren bei:").pack(side="left", padx=(0, 5))

        self.sort_criteria = ttk.Combobox(frame, values=["Name", "Beliebtheit", "Preis", "Zutatenanzahl"], state="readonly")
        self.sort_criteria.current(0)
        self.sort_criteria.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.sort_order = ttk.Combobox(frame, values=["Aufsteigend", "Absteigend"], state="readonly")
        self.sort_order.current(0)
        self.sort_order.pack(side="left", fill="x", expand=True)

        ttk.Button(frame, text="Anwenden", command=self.apply_sorting).pack(side="left", padx=(5, 0))

    def setup_listbox(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        bg = "#333333" if self.theme == "dark" else "white"
        fg = "white" if self.theme == "dark" else "black"

        self.listbox = tk.Listbox(
            frame,
            bg=bg,
            fg=fg,
            selectbackground="#0078d4",
            selectforeground="white",
            font=("Segoe UI", 11),
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(frame, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.listbox.bind('<<ListboxSelect>>', self.show_details)

    def setup_details_panel(self):
        frame = ttk.Frame(self, padding=15, style="Card.TFrame")
        frame.grid(row=0, column=1, sticky="nsew")

        self.name_label = ttk.Label(frame, font=("Segoe UI", 18, "bold"), style="Large.TLabel")
        self.name_label.pack(anchor="w")

        ttk.Separator(frame).pack(fill="x", pady=10)

        self.notes_label = ttk.Label(frame, wraplength=400, style="Small.TLabel")
        self.notes_label.pack(anchor="w", pady=(0, 20))

        ttk.Label(frame, text="Zutaten:", font=("Segoe UI", 12, "bold"), style="Medium.TLabel").pack(anchor="w")

        container = ttk.Frame(frame)
        container.pack(fill="x", pady=(5, 0))
        canvas = tk.Canvas(container, height=200, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.ingredients_frame = ttk.Frame(canvas)

        self.ingredients_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.ingredients_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_action_buttons(self):
        frame = ttk.Frame(self, padding=(0, 10, 0, 0))
        frame.grid(row=1, column=1, sticky="se")
        self.btn_mix = ttk.Button(frame, text="Mix Drink", command=self.mix_cocktail, style="Accent.TButton", width=15)
        self.btn_mix.pack()

    def apply_sorting(self):
        self.current_sort = (self.sort_criteria.get(), self.sort_order.get())
        self.update_list()
        self.initial_selection()

    def update_list(self):
        self.data_manager.sort_data(*self.current_sort)
        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for cocktail in self.data_manager.sorted_cocktails:
            self.listbox.insert(tk.END, cocktail)

    def filter_list(self, _):
        search = self.search_var.get().lower()
        filtered = [c for c in self.data_manager.sorted_cocktails if search in c.lower()]
        self.listbox.delete(0, tk.END)
        for c in filtered:
            self.listbox.insert(tk.END, c)
        if filtered:
            self.listbox.selection_set(0)
            self.listbox.event_generate("<<ListboxSelect>>")

    def show_details(self, _):
        try:
            idx = self.listbox.curselection()
            if not idx:
                return
            name = self.listbox.get(idx)
            data = self.data_manager.get_cocktail(name)
            if not data:
                return

            self.name_label.config(text=name)
            self.notes_label.config(text=data.get("Notes", ""))

            # Clear previous ingredients
            for w in self.ingredients_frame.winfo_children():
                w.destroy()

            # Display ingredients
            for ing, amt in data.get("Ingredients", {}).items():
                row = ttk.Frame(self.ingredients_frame)
                row.pack(fill="x", pady=2, anchor="w")
                ttk.Label(row, text="•", width=2, anchor="w", style="Medium.TLabel").pack(side="left")
                ttk.Label(row, text=f"{ing}:", width=20, anchor="w", style="Medium.TLabel").pack(side="left")
                ttk.Label(row, text=f"{amt} ml" if amt != "--" else amt, style="Medium.TLabel").pack(side="left")

            # Add price display below ingredients
            price_frame = ttk.Frame(self.ingredients_frame)
            price_frame.pack(fill="x", pady=(10, 0), anchor="w")
            ttk.Label(price_frame, text="Preis:", width=20, anchor="w", 
                    style="Medium.TLabel", font=("Segoe UI", 11, "bold")).pack(side="left")
            
            # Get price from the data_manager's prices dictionary
            price = self.data_manager.prices.get(name, "N/A")
            ttk.Label(price_frame, text=f"{price} €", 
                    style="Medium.TLabel").pack(side="left")
            
        except Exception as e:
            print(f"Fehler bei Details: {e}")

    def mix_cocktail(self):

        if not self.listbox.curselection():
            messagebox.showwarning("Warunung", "Bitte ein Cocktail zuerst auswählen!")
            return

        name = self.listbox.get(self.listbox.curselection())
        data = self.data_manager.get_cocktail(name)

        if not data:
            messagebox.showerror("Fehler", "Cocktaildaten nicht gefunden.")
            return

        ingredients = {}
        for ing, amount in data.get("Ingredients", {}).items():
            try:
                if isinstance(amount, str) and amount.strip() == "--":
                    continue
                amount_ml = int(float(amount))  # Wandelt "50" oder "50.0" in int
                ingredients[ing] = amount_ml
            except:
                continue

        if not self.serial_manager or not self.serial_manager.running:
            messagebox.showerror("Fehler", "Keine serielle Verbindung aktiv.")
            return

        # Nachricht senden
        self.serial_manager.send_cocktail_recipe(name, ingredients)
        messagebox.showinfo("Info", f"{name} wird gemixt – Befehl gesendet.")
  

    def initial_selection(self):
        if self.data_manager.sorted_cocktails:
            self.listbox.selection_set(0)
            self.listbox.event_generate("<<ListboxSelect>>")

    def set_theme(self, dark_mode):
        self.theme = "dark" if dark_mode else "light"
        bg = "#333333" if dark_mode else "white"
        fg = "white" if dark_mode else "black"
        self.listbox.config(bg=bg, fg=fg)


class SettingsPage(ttk.Frame):
    def __init__(self, parent, toggle_theme_callback, serial_manager):
        super().__init__(parent)
        self.toggle_theme_callback = toggle_theme_callback
        self.serial_manager = serial_manager
        ttk.Label(self, text="⚙️ Einstellungen", font=("Segoe UI", 16)).pack(pady=20)
        self.theme_var = tk.BooleanVar()
        ttk.Checkbutton(
            self,
            text="Dunkles Theme aktivieren",
            variable=self.theme_var,
            command=self.toggle_theme,
            style="Switch.TCheckbutton"
        ).pack(pady=10)

        self.setup_serial_controls()
        self.serial_manager.register_handler('connected', self.on_serial_connected)
        self.serial_manager.register_handler('disconnected', self.on_serial_disconnected)
        self.serial_manager.register_handler('error', self.on_serial_error)
        self.serial_manager.register_handler('message_received', self.on_serial_message)

    def setup_serial_controls(self):
        frame = ttk.LabelFrame(self, text="Serielle Verbindung", padding=10)
        frame.pack(fill="x", pady=20, padx=10)

        ttk.Label(frame, text="Port:").grid(row=0, column=0, sticky="w")
        self.port_combobox = ttk.Combobox(frame, state="readonly")
        self.port_combobox.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Button(frame, text="🔃", width=3, command=self.refresh_ports).grid(row=0, column=2, padx=(5, 0))

        self.connect_btn = ttk.Button(frame, text="Verbinden", command=self.toggle_serial_connection)
        self.connect_btn.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="ew")

        self.connection_status = ttk.Label(frame, text="Status: Nicht verbunden")
        self.connection_status.grid(row=2, column=0, columnspan=3, pady=(5, 0), sticky="w")

        self.refresh_ports()

    def refresh_ports(self):
        ports = self.serial_manager.list_ports()
        self.port_combobox['values'] = ports
        if ports:
            self.port_combobox.current(0)

    def toggle_serial_connection(self):
        if self.serial_manager.running:
            self.serial_manager.disconnect()
        else:
            port = self.port_combobox.get()
            if port:
                self.serial_manager.connect(port)
            else:
                messagebox.showwarning("Warnung", "Bitte einen Port auswählen!")

    def on_serial_connected(self):
        self.connect_btn.config(text="Trennen")
        self.connection_status.config(text="Status: Verbunden")
        messagebox.showinfo("Info", "Erfolgreich verbunden!")

    def on_serial_disconnected(self):
        self.connect_btn.config(text="Verbinden")
        self.connection_status.config(text="Status: Nicht verbunden")

    def on_serial_error(self, msg):
        messagebox.showerror("Fehler", msg)

    def on_serial_message(self, msg):
        print(f"Empfangene Nachricht: {msg}")

    def toggle_theme(self):
        self.toggle_theme_callback(self.theme_var.get())


class App(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.parent = parent
        self.data_manager = data_manager

        self.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.apply_theme_styles(dark_mode=False)
        self.setup_sidebar()
        self.setup_pages()
        self.show_page("Main")

    def setup_sidebar(self):
        sidebar = ttk.Frame(self, style="Card.TFrame", padding=5, width=80)
        sidebar.grid(row=0, column=0, sticky="nsw")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        icons = {
            "Main": PhotoImage(file=os.path.join(base_dir, "icons", "file.png")),
            "Settings": PhotoImage(file=os.path.join(base_dir, "icons", "settings.png"))
        }

        for name, icon in icons.items():
            frame = ttk.Frame(sidebar)
            frame.pack(fill="x", pady=10)
            label = ttk.Label(frame, image=icon, cursor="hand2")
            label.image = icon  
            label.pack()
            label.bind("<Button-1>", lambda e, name=name: self.show_page(name))

    def setup_pages(self):
        container = ttk.Frame(self)
        container.grid(row=0, column=1, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        self.serial_manager = SerialManager() 

        self.pages = {
            "Main": MainPage(container, self.data_manager, self.serial_manager),
            "Settings": SettingsPage(container, self.set_theme, self.serial_manager)
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")



    def show_page(self, name):
        for page in self.pages.values():
            page.grid_remove()
        self.pages[name].grid()

    def set_theme(self, dark_mode):
        theme = "dark" if dark_mode else "light"
        try:
            self. parent.tk.call("set_theme", theme)
            self.apply_theme_styles(dark_mode)
            for page in self.pages.values():
                if hasattr(page, 'set_theme'):
                    page.set_theme(dark_mode)
        except Exception as e:
            messagebox.showerror("Fehler", f"Theme konnte nicht gesetzt werden: {e}")

    def apply_theme_styles(self, dark_mode):
        style = ttk.Style()
        fg_primary = "white" if dark_mode else "black"
        fg_secondary = "#a6a6a6" if dark_mode else "#5a5a5a"
        bg_card = "#252525" if dark_mode else "#f5f5f5"

        style.configure("Card.TFrame", background=bg_card)
        style.configure("Large.TLabel", foreground=fg_primary, font=("Segoe UI", 14))
        style.configure("Medium.TLabel", foreground=fg_primary, font=("Segoe UI", 11))
        style.configure("Small.TLabel", foreground=fg_secondary, font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 11))


def main():
    root = tk.Tk()
    root.title("Cocktail Mixer Pro")

    # Basisverzeichnis der Datei
    base_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        # Lade Azure-Theme relativ zum Projektordner
        theme_path = os.path.join(base_dir, "Azure-ttk-theme-main", "azure.tcl")
        root.tk.call("source", theme_path)
        root.tk.call("set_theme", "light")
    except Exception as e:
        print("Azure theme konnte nicht geladen werden:", e)


    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    data_manager = CocktailDataManager()
    app = App(root, data_manager)
    app.grid(sticky="nsew")

    root.minsize(700, 400)
    root.geometry("1000x600")
    root.mainloop()


if __name__ == "__main__":
    main()
