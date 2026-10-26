import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

# --------------------------------------------------
# PROJECT SETTINGS
# --------------------------------------------------

APP_TITLE = "Patient Record Management System"
DATA_FILE = "patient_records.json"


# --------------------------------------------------
# CLASS 1: PATIENT
# --------------------------------------------------

class Patient:
    def __init__(self, patient_id, name, age, gender, phone):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.medical_records = []

    def add_medical_record(self, record):
        self.medical_records.append(record)

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "medical_records": [
                record.to_dict() for record in self.medical_records
            ]
        }

    @classmethod
    def from_dict(cls, data):
        patient = cls(
            data["patient_id"],
            data["name"],
            data["age"],
            data["gender"],
            data["phone"]
        )

        for record_data in data.get("medical_records", []):
            patient.add_medical_record(
                MedicalRecord.from_dict(record_data)
            )

        return patient


# --------------------------------------------------
# CLASS 2: MEDICAL RECORD
# --------------------------------------------------

class MedicalRecord:
    def __init__(self, record_date, symptoms, diagnosis, treatment):
        self.record_date = record_date
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.treatment = treatment

    def to_dict(self):
        return {
            "record_date": self.record_date,
            "symptoms": self.symptoms,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["record_date"],
            data["symptoms"],
            data["diagnosis"],
            data["treatment"]
        )


# --------------------------------------------------
# CLASS 3: MAIN APPLICATION
# --------------------------------------------------

class PatientRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1150x750")
        self.root.minsize(900, 600)

        self.patients = {}
        self.selected_patient_id = None

        self.setup_style()
        self.load_data()
        self.create_interface()
        self.refresh_patient_table()

    # ---------------- STYLE ----------------

    def setup_style(self):
        self.root.configure(bg="#F3F6FA")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TFrame",
            background="#F3F6FA"
        )

        style.configure(
            "TLabel",
            background="#F3F6FA",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold"),
            foreground="#16324F",
            background="#F3F6FA"
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10),
            foreground="#526579",
            background="#F3F6FA"
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=8
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.configure(
            "TLabelframe",
            background="#F3F6FA"
        )

        style.configure(
            "TLabelframe.Label",
            font=("Segoe UI", 11, "bold"),
            foreground="#16324F",
            background="#F3F6FA"
        )

    # ---------------- DATA STORAGE ----------------

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                patient = Patient.from_dict(item)
                self.patients[patient.patient_id] = patient

        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            messagebox.showerror(
                "Data Loading Error",
                f"Could not load patient data:\n{error}"
            )

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    [patient.to_dict() for patient in self.patients.values()],
                    file,
                    indent=4
                )
            return True

        except (OSError, TypeError, ValueError) as error:
            messagebox.showerror(
                "Saving Error",
                f"Could not save the records:\n{error}"
            )
            return False

    # ---------------- MAIN INTERFACE ----------------

    def create_interface(self):
        header = ttk.Frame(self.root, padding=(20, 18))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Patient Record Management System",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Healthcare patient registration and medical record management",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(5, 0))

        self.stats_label = ttk.Label(
            header,
            text="Registered Patients: 0",
            font=("Segoe UI", 10, "bold")
        )
        self.stats_label.pack(anchor="w", pady=(10, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        self.patient_tab = ttk.Frame(self.notebook, padding=15)
        self.record_tab = ttk.Frame(self.notebook, padding=15)
        self.view_tab = ttk.Frame(self.notebook, padding=15)

        self.notebook.add(
            self.patient_tab,
            text="  Register Patient  "
        )
        self.notebook.add(
            self.record_tab,
            text="  Medical Records  "
        )
        self.notebook.add(
            self.view_tab,
            text="  View Patients  "
        )

        self.create_patient_form()
        self.create_record_form()
        self.create_patient_list()

        footer = ttk.Label(
            self.root,
            text="OOP1 Academic Project | Use fictional data for demonstrations",
            anchor="center",
            padding=8
        )
        footer.pack(fill="x")

    # ---------------- PATIENT REGISTRATION ----------------

    def create_patient_form(self):
        form = ttk.LabelFrame(
            self.patient_tab,
            text="Patient Information",
            padding=20
        )
        form.pack(fill="x", anchor="n")

        self.patient_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        ttk.Label(form, text="Patient ID").grid(
            row=0, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.patient_id_var,
            width=35
        ).grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Full Name").grid(
            row=1, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.name_var,
            width=35
        ).grid(row=1, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Age").grid(
            row=2, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.age_var,
            width=35
        ).grid(row=2, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Gender").grid(
            row=3, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Combobox(
            form,
            textvariable=self.gender_var,
            values=("Female", "Male", "Other", "Prefer not to say"),
            state="readonly",
            width=32
        ).grid(row=3, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Phone Number").grid(
            row=4, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.phone_var,
            width=35
        ).grid(row=4, column=1, sticky="ew", padx=8, pady=8)

        form.columnconfigure(1, weight=1)

        buttons = ttk.Frame(self.patient_tab)
        buttons.pack(fill="x", pady=15)

        ttk.Button(
            buttons,
            text="Register Patient",
            command=self.register_patient
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            buttons,
            text="Clear Form",
            command=self.clear_patient_form
        ).pack(side="left")

        ttk.Label(
            self.patient_tab,
            text=(
                "Enter the patient's details and select Register Patient. "
                "Each patient must have a unique ID."
            ),
            wraplength=800
        ).pack(anchor="w", pady=10)

    def register_patient(self):
        patient_id = self.patient_id_var.get().strip()
        name = self.name_var.get().strip()
        age_text = self.age_var.get().strip()
        gender = self.gender_var.get().strip()
        phone = self.phone_var.get().strip()

        if not all((patient_id, name, age_text, gender, phone)):
            messagebox.showwarning(
                "Missing Information",
                "Please complete all patient fields."
            )
            return

        if patient_id in self.patients:
            messagebox.showerror(
                "Duplicate ID",
                "This patient ID already exists. Please use another ID."
            )
            return

        try:
            age = int(age_text)
            if not 0 <= age <= 130:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Age",
                "Age must be a whole number between 0 and 130."
            )
            return

        patient = Patient(
            patient_id, name, age, gender, phone
        )

        self.patients[patient_id] = patient

        if not self.save_data():
            del self.patients[patient_id]
            return

        self.refresh_patient_table()
        self.clear_patient_form()

        messagebox.showinfo(
            "Success",
            f"Patient {name} has been registered successfully."
        )

    def clear_patient_form(self):
        self.patient_id_var.set("")
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.phone_var.set("")

    # ---------------- MEDICAL RECORDS ----------------

    def create_record_form(self):
        form = ttk.LabelFrame(
            self.record_tab,
            text="Add a Medical Record",
            padding=20
        )
        form.pack(fill="x", anchor="n")

        self.record_patient_var = tk.StringVar()
        self.record_date_var = tk.StringVar(
            value=date.today().isoformat()
        )
        self.symptoms_var = tk.StringVar()
        self.diagnosis_var = tk.StringVar()

        ttk.Label(form, text="Patient ID").grid(
            row=0, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.record_patient_var
        ).grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Visit Date (YYYY-MM-DD)").grid(
            row=1, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.record_date_var
        ).grid(row=1, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Symptoms").grid(
            row=2, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.symptoms_var
        ).grid(row=2, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Diagnosis").grid(
            row=3, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(
            form,
            textvariable=self.diagnosis_var
        ).grid(row=3, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="Treatment Notes").grid(
            row=4, column=0, sticky="nw", padx=8, pady=8
        )

        self.treatment_text = tk.Text(
            form,
            height=5,
            width=40,
            font=("Segoe UI", 10),
            wrap="word"
        )
        self.treatment_text.grid(
            row=4, column=1, sticky="ew", padx=8, pady=8
        )

        form.columnconfigure(1, weight=1)

        buttons = ttk.Frame(self.record_tab)
        buttons.pack(fill="x", pady=15)

        ttk.Button(
            buttons,
            text="Save Medical Record",
            command=self.add_medical_record
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            buttons,
            text="Clear Form",
            command=self.clear_record_form
        ).pack(side="left")

        ttk.Label(
            self.record_tab,
            text="The patient must already be registered before adding a medical record.",
            wraplength=800
        ).pack(anchor="w", pady=8)

    def add_medical_record(self):
        patient_id = self.record_patient_var.get().strip()
        record_date = self.record_date_var.get().strip()
        symptoms = self.symptoms_var.get().strip()
        diagnosis = self.diagnosis_var.get().strip()
        treatment = self.treatment_text.get(
            "1.0", "end"
        ).strip()

        if not all((
            patient_id, record_date,
            symptoms, diagnosis, treatment
        )):
            messagebox.showwarning(
                "Missing Information",
                "Please complete all medical record fields."
            )
            return

        if patient_id not in self.patients:
            messagebox.showerror(
                "Patient Not Found",
                "Register the patient first or check the patient ID."
            )
            return

        try:
            datetime.strptime(record_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Enter a valid date in YYYY-MM-DD format."
            )
            return

        record = MedicalRecord(
            record_date, symptoms, diagnosis, treatment
        )

        patient = self.patients[patient_id]
        patient.add_medical_record(record)

        if not self.save_data():
            patient.medical_records.pop()
            return

        self.clear_record_form()

        messagebox.showinfo(
            "Success",
            "Medical record saved successfully."
        )

    def clear_record_form(self):
        self.record_patient_var.set("")
        self.record_date_var.set(date.today().isoformat())
        self.symptoms_var.set("")
        self.diagnosis_var.set("")
        self.treatment_text.delete("1.0", "end")

    # ---------------- VIEW AND SEARCH PATIENTS ----------------

    def create_patient_list(self):
        search_frame = ttk.Frame(self.view_tab)
        search_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(
            search_frame,
            text="Search by Patient ID or Name:"
        ).pack(side="left", padx=(0, 8))

        self.search_var = tk.StringVar()

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        )
        search_entry.pack(side="left", padx=(0, 8))

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_patient_table()
        )

        ttk.Button(
            search_frame,
            text="Clear Search",
            command=self.clear_search
        ).pack(side="left")

        table_frame = ttk.Frame(self.view_tab)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "patient_id", "name", "age",
            "gender", "phone", "records"
        )

        self.patient_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "patient_id": "Patient ID",
            "name": "Full Name",
            "age": "Age",
            "gender": "Gender",
            "phone": "Phone",
            "records": "Medical Records"
        }

        widths = {
            "patient_id": 110,
            "name": 200,
            "age": 60,
            "gender": 100,
            "phone": 140,
            "records": 120
        }

        for column in columns:
            self.patient_table.heading(
                column, text=headings[column]
            )
            self.patient_table.column(
                column,
                width=widths[column],
                anchor="w"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.patient_table.yview
        )
        self.patient_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.patient_table.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        self.patient_table.bind(
            "<Double-1>",
            self.show_patient_details
        )

        buttons = ttk.Frame(self.view_tab)
        buttons.pack(fill="x", pady=12)

        ttk.Button(
            buttons,
            text="View Patient Details",
            command=self.show_patient_details
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            buttons,
            text="Add Medical Record for Selected Patient",
            command=self.use_selected_patient
        ).pack(side="left")

        ttk.Label(
            self.view_tab,
            text="Double-click a patient to view their medical records.",
            wraplength=800
        ).pack(anchor="w", pady=5)

    def refresh_patient_table(self):
        if not hasattr(self, "patient_table"):
            return

        for item in self.patient_table.get_children():
            self.patient_table.delete(item)

        query = (
            self.search_var.get().strip().lower()
            if hasattr(self, "search_var") else ""
        )

        for patient in self.patients.values():
            if (
                query
                and query not in patient.patient_id.lower()
                and query not in patient.name.lower()
            ):
                continue

            self.patient_table.insert(
                "",
                "end",
                values=(
                    patient.patient_id,
                    patient.name,
                    patient.age,
                    patient.gender,
                    patient.phone,
                    len(patient.medical_records)
                )
            )

        if hasattr(self, "stats_label"):
            self.stats_label.config(
                text=f"Registered Patients: {len(self.patients)}"
            )

    def clear_search(self):
        self.search_var.set("")
        self.refresh_patient_table()

    def get_selected_patient(self):
        selected = self.patient_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a patient from the table."
            )
            return None

        values = self.patient_table.item(
            selected[0], "values"
        )

        return self.patients.get(values[0])

    def use_selected_patient(self):
        patient = self.get_selected_patient()

        if patient is None:
            return

        self.record_patient_var.set(patient.patient_id)
        self.notebook.select(self.record_tab)

    def show_patient_details(self, event=None):
        patient = self.get_selected_patient()

        if patient is None:
            return

        window = tk.Toplevel(self.root)
        window.title(f"Patient Details - {patient.patient_id}")
        window.geometry("650x550")
        window.minsize(450, 350)
        window.configure(bg="#F3F6FA")

        ttk.Label(
            window,
            text="Patient Details",
            style="Title.TLabel"
        ).pack(anchor="w", padx=20, pady=(20, 10))

        details = (
            f"Patient ID: {patient.patient_id}\n"
            f"Name: {patient.name}\n"
            f"Age: {patient.age}\n"
            f"Gender: {patient.gender}\n"
            f"Phone: {patient.phone}\n"
            f"Number of Medical Records: {len(patient.medical_records)}"
        )

        ttk.Label(
            window,
            text=details,
            justify="left",
            font=("Segoe UI", 11)
        ).pack(anchor="w", padx=20, pady=10)

        ttk.Label(
            window,
            text="Medical History",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        history = tk.Text(
            window,
            wrap="word",
            font=("Segoe UI", 10),
            padx=10,
            pady=10
        )
        history.pack(
            fill="both", expand=True, padx=20, pady=(0, 20)
        )

        if not patient.medical_records:
            history.insert(
                "end", "No medical records have been added yet."
            )
        else:
            for index, record in enumerate(
                patient.medical_records, start=1
            ):
                history.insert(
                    "end",
                    f"RECORD {index}\n"
                    f"Date: {record.record_date}\n"
                    f"Symptoms: {record.symptoms}\n"
                    f"Diagnosis: {record.diagnosis}\n"
                    f"Treatment: {record.treatment}\n"
                    f"{'-' * 45}\n\n"
                )

        history.config(state="disabled")


# --------------------------------------------------
# RUN THE APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientRecordApp(root)
    root.mainloop()