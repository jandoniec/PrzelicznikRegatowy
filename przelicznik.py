import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class RaceResultsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Race Results App")

        self.regatta_name = ""
        self.coefficient_type_options = ["ORC", "KWR", "NHC"]

        self.tab_control = ttk.Notebook(master)
        self.tab_control.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.tab_regatta = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_regatta, text="Regatta Details")

        self.label_regatta = ttk.Label(self.tab_regatta, text="Nazwa regat:")
        self.label_regatta.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_regatta = ttk.Entry(self.tab_regatta)
        self.entry_regatta.grid(row=0, column=1, padx=10, pady=10)

        self.set_regatta_button = ttk.Button(self.tab_regatta, text="Ustaw nazwę regat", command=self.set_regatta_name)
        self.set_regatta_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.tab_results = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_results, text="Race Results")

        self.results = {ctype: [] for ctype in self.coefficient_type_options}

        self.label_boat_name = ttk.Label(self.tab_results, text="Nazwa jachtu:")
        self.label_boat_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_boat_name = ttk.Entry(self.tab_results)
        self.entry_boat_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_skipper = ttk.Label(self.tab_results, text="Skipper:")
        self.label_skipper.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_skipper = ttk.Entry(self.tab_results)
        self.entry_skipper.grid(row=1, column=1, padx=10, pady=10)

        self.label_type = ttk.Label(self.tab_results, text="Typ jachtu:")
        self.label_type.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.entry_type = ttk.Entry(self.tab_results)
        self.entry_type.grid(row=2, column=1, padx=10, pady=10)

        self.label_time = ttk.Label(self.tab_results, text="Czas wyścigu (h:min:sec):")
        self.label_time.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.entry_time = ttk.Entry(self.tab_results)
        self.entry_time.grid(row=3, column=1, padx=10, pady=10)

        self.label_factor = ttk.Label(self.tab_results, text="Przelicznik:")
        self.label_factor.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.entry_factor = ttk.Entry(self.tab_results)
        self.entry_factor.grid(row=4, column=1, padx=10, pady=10)

        self.label_coefficient_type = ttk.Label(self.tab_results, text="Typ przelicznika:")
        self.label_coefficient_type.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.coefficient_type = tk.StringVar()
        self.coefficient_type.set(self.coefficient_type_options[0])
        self.coefficient_type_menu = ttk.Combobox(self.tab_results, textvariable=self.coefficient_type, values=self.coefficient_type_options)
        self.coefficient_type_menu.grid(row=5, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(self.tab_results, text="Dodaj rekord", command=self.add_result)
        self.add_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.results_notebook = ttk.Notebook(self.tab_results)
        self.results_notebook.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.results_trees = {ctype: ttk.Treeview(self.results_notebook, columns=("Boat Name", "Skipper", "Type", "Time", "Factor", "Coefficient Type", "Total Time"))
                              for ctype in self.coefficient_type_options}

        for ctype, tree in self.results_trees.items():
            tree.heading("#0", text="ID")
            tree.heading("Boat Name", text="Nazwa Jachtu")
            tree.heading("Skipper", text="Skipper")
            tree.heading("Type", text="Typ jachtu")
            tree.heading("Time", text="Czas")
            tree.heading("Factor", text="Przelicznik")
            tree.heading("Coefficient Type", text="Typ przelicznika")
            tree.heading("Total Time", text="Całkowity czas")
            tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

            self.results_notebook.add(tree, text=ctype)
            self.delete_button = ttk.Button(self.tab_results, text="Usuń rekord", command=self.delete_selected_record)
            self.delete_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.sort_button = ttk.Button(self.tab_results, text="Sortuj i zapisz", command=self.sort_and_save)
        self.sort_button.grid(row=9, column=0, columnspan=2, pady=10)

    def set_regatta_name(self):
        self.regatta_name = self.entry_regatta.get()
        if self.regatta_name:
            self.tab_control.select(1)  # Przełącz na zakładkę z wynikami po wpisaniu nazwy regat
            self.entry_regatta.config(state="disabled")  # Wyłącz pole edycji nazwy regat
        else:
            messagebox.showerror("Błąd", "Wprowadź nazwę regat.")

    def add_result(self):
            if not self.regatta_name:
                messagebox.showerror("Błąd", "Najpierw ustaw nazwę regat.")
                return

            boat_name = self.entry_boat_name.get()
            skipper = self.entry_skipper.get()
            boat_type = self.entry_type.get()
            race_time = self.entry_time.get()
            factor = self.entry_factor.get()
            coefficient_type = self.coefficient_type.get()

            try:
                time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(race_time.split(":"))))
                factor = float(factor)
                total_time = time_seconds * factor
                self.results[coefficient_type].append((boat_name, skipper, boat_type, race_time, factor, coefficient_type, total_time))

                # Dodaj wpis do widoku Treeview
                tree = self.results_trees[coefficient_type]
                tree.insert("", "end", values=(boat_name, skipper, boat_type, race_time, factor, coefficient_type, f"{total_time:.2f}"))

                # Wyczyść pola wprowadzania danych
                self.entry_boat_name.delete(0, tk.END)
                self.entry_skipper.delete(0, tk.END)
                self.entry_type.delete(0, tk.END)
                self.entry_time.delete(0, tk.END)
                self.entry_factor.delete(0, tk.END)

                messagebox.showinfo("Sukces", "Rekord dodany poprawnie.")
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowy format czasu lub przelicznika.")
                





    def refresh_treeview(self, ctype):
        # Usuń wszystkie istniejące rekordy z widoku drzewa
        for i in self.results_trees[ctype].get_children():
            self.results_trees[ctype].delete(i)

        # Dodaj aktualne wyniki do widoku drzewa
        for result in self.results[ctype]:
            self.results_trees[ctype].insert('', 'end', values=result)

    def update_results_files(self):
        for ctype, result_list in self.results.items():
            if not result_list:
                continue

            result_list.sort(key=lambda x: x[-1])

            pdf_filename = f"{self.regatta_name}_{ctype}_race_results.pdf"
            jpg_filename = f"{self.regatta_name}_{ctype}_race_results.jpg"

    def delete_selected_record(self):
        # Pobierz identyfikator zaznaczonego rekordu
        selected_item = self.results_trees[self.coefficient_type.get()].selection()[0]

        # Sprawdź, czy zaznaczony rekord istnieje w liście wyników
        if selected_item:
            # Pobierz indeks zaznaczonego rekordu
            selected_index = self.results_trees[self.coefficient_type.get()].index(selected_item)

            # Usuń rekord z listy wyników na podstawie indeksu
            del self.results[self.coefficient_type.get()][selected_index]

            # Odśwież widok drzewa
            self.refresh_treeview(self.coefficient_type.get())

            # Zaktualizuj pliki wyników
            self.update_results_files()



    def sort_and_save(self):
        if not self.regatta_name:
            messagebox.showerror("Błąd", "Najpierw ustaw nazwę regat.")
            return

        if not any(self.results.values()):
            messagebox.showwarning("Uwaga", "Brak wyników do zapisania.")
            return

        for ctype, result_list in self.results.items():
            if not result_list:
                continue

            result_list.sort(key=lambda x: x[-1])

            pdf_filename = f"{self.regatta_name}_{ctype}_race_results.pdf"
            jpg_filename = f"{self.regatta_name}_{ctype}_race_results.jpg"

            pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)
            pdf_canvas.setFont("Helvetica-Bold", 14)  # Ustawiono na pogrubiony
            pdf_canvas.drawCentredString(300, 770, f"Wyniki regat: {self.regatta_name} - {ctype}")

            data = [["ID", "Nazwa Jachtu", "Skipper", "Typ jachtu", "Czas", "Przelicznik", "Typ przelicznika", "Calkowity czas"]]

            for i, (boat_name, skipper, boat_type, race_time, factor, coefficient_type, total_time) in enumerate(result_list, start=1):
                formatted_time = f"{int(total_time//3600):02}:{int((total_time%3600)//60):02}:{total_time%60:05.2f}"
                data.append([i, boat_name, skipper, boat_type, race_time, factor, coefficient_type, formatted_time])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Kolor tła dla nagłówka
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Kolor tekstu dla nagłówka
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Wyśrodkowanie dla całej tabeli
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Grubość linii wewnętrznych
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)  # Grubość linii zewnętrznych
            ]))

            table.wrapOn(pdf_canvas, 400, 600)  # Dopuszczalne wymiary tabeli
            table.drawOn(pdf_canvas, 100, 500)  # Położenie tabeli

            pdf_canvas.save()

            img = Image.new("RGB", (800, 400), color="white")
            draw = ImageDraw.Draw(img)

            draw.text((10, 10), f"Wyniki regat: {self.regatta_name} - {ctype}", fill="black", font="Helvetica-Bold")
            draw.text((10, 30), "=" * 40, fill="black")

            draw.text((10, 60), f"{'ID':<5} {'Nazwa Jachtu':<20} {'Skipper':<20} {'Typ jachtu':<15} {'Czas':<15} {'Przelicznik':<15} {'Typ przelicznika':<15} {'Całkowity czas':<20}", fill="black", font="Helvetica-Bold")
            draw.text((10, 65), "-" * 180, fill="black")

            for i, (boat_name, skipper, boat_type, race_time, factor, coefficient_type, total_time) in enumerate(result_list, start=1):
                formatted_time = f"{int(total_time//3600):02}:{int((total_time%3600)//60):02}:{total_time%60:05.2f}"
                draw.text((10, 80 + i * 20), f"{i:<5} {boat_name:<20} {skipper:<20} {boat_type:<15} {race_time:<15} {factor:<15} {coefficient_type:<15} {formatted_time}", fill="black")

            img.save(jpg_filename)

        self.refresh_treeview(ctype)
        messagebox.showinfo("Sukces", f"Wyniki posortowane i zapisane w plikach:\n- {pdf_filename}\n- {jpg_filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RaceResultsApp(root)
    root.mainloop()
#test g