import tkinter as tk
from tkinter import ttk, messagebox


class HydroTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HydroTrack")
        self.root.geometry("560x620")
        self.root.resizable(False, False)

        self.daily_norm = 0
        self.drunk_water = 0
        self.reminder_job = None

        self.name_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.goal_var = tk.StringVar(value="Keep healthy")
        self.glass_var = tk.StringVar(value="250")
        self.reminder_var = tk.StringVar(value="30")

        self.daily_norm_var = tk.StringVar(value="Daily norm: 0 ml")
        self.drunk_var = tk.StringVar(value="Drunk today: 0 ml")
        self.left_var = tk.StringVar(value="Left to drink: 0 ml")
        self.status_var = tk.StringVar(value="Status: Enter your data and press Calculate")
        self.tip_var = tk.StringVar(value="Tip: Drink water regularly in small portions during the day.")

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="HydroTrack",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(18, 4))

        subtitle = tk.Label(
            self.root,
            text="Water Intake Reminder App",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 14))

        form = tk.Frame(self.root, padx=18, pady=10)
        form.pack(fill="x")

        self.add_label_entry(form, "Name", self.name_var, 0)
        self.add_label_entry(form, "Weight (kg)", self.weight_var, 1)
        self.add_label_entry(form, "Age", self.age_var, 2)

        tk.Label(form, text="Goal", font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=8)
        goal_box = ttk.Combobox(
            form,
            textvariable=self.goal_var,
            state="readonly",
            values=["Keep healthy", "Lose weight", "Active lifestyle"],
            width=28
        )
        goal_box.grid(row=3, column=1, sticky="w", pady=8)

        tk.Label(form, text="Glass volume (ml)", font=("Arial", 11)).grid(row=4, column=0, sticky="w", pady=8)
        glass_box = ttk.Combobox(
            form,
            textvariable=self.glass_var,
            state="readonly",
            values=["200", "250", "300"],
            width=28
        )
        glass_box.grid(row=4, column=1, sticky="w", pady=8)

        tk.Label(form, text="Reminder (minutes)", font=("Arial", 11)).grid(row=5, column=0, sticky="w", pady=8)
        reminder_box = ttk.Combobox(
            form,
            textvariable=self.reminder_var,
            state="readonly",
            values=["15", "30", "45", "60"],
            width=28
        )
        reminder_box.grid(row=5, column=1, sticky="w", pady=8)

        btn_frame = tk.Frame(self.root, pady=12)
        btn_frame.pack()

        tk.Button(btn_frame, text="Calculate", width=16, command=self.calculate_norm).grid(row=0, column=0, padx=6, pady=6)
        tk.Button(btn_frame, text="I drank water", width=16, command=self.drink_water).grid(row=0, column=1, padx=6, pady=6)
        tk.Button(btn_frame, text="Reset", width=16, command=self.reset_data).grid(row=0, column=2, padx=6, pady=6)

        results = tk.LabelFrame(self.root, text="Results", padx=14, pady=12, font=("Arial", 11, "bold"))
        results.pack(fill="x", padx=18, pady=8)

        tk.Label(results, textvariable=self.daily_norm_var, font=("Arial", 11)).pack(anchor="w", pady=4)
        tk.Label(results, textvariable=self.drunk_var, font=("Arial", 11)).pack(anchor="w", pady=4)
        tk.Label(results, textvariable=self.left_var, font=("Arial", 11)).pack(anchor="w", pady=4)
        tk.Label(results, textvariable=self.status_var, font=("Arial", 11, "bold"), wraplength=500, justify="left").pack(anchor="w", pady=8)

        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill="x", padx=18, pady=8)

        tk.Label(progress_frame, text="Progress", font=("Arial", 11, "bold")).pack(anchor="w")
        self.progress = (ttk.
                         Progressbar(progress_frame, length=500, mode="determinate", maximum=100))
        self.progress.pack(pady=6)

        tip_frame = tk.LabelFrame(self.root, text="Personal Tip", padx=14, pady=12, font=("Arial", 11, "bold"))
        tip_frame.pack(fill="x", padx=18, pady=8)
        tk.Label(tip_frame, textvariable=self.tip_var, wraplength=500, justify="left", font=("Arial", 11)).pack(anchor="w")

        reminder_note = tk.Label(
            self.root,
            text="The app will show a reminder message after the selected time interval.",
            font=("Arial", 10)
        )
        reminder_note.pack(pady=8)

    def add_label_entry(self, parent, text, variable, row):
        tk.Label(parent, text=text, font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=8)
        tk.Entry(parent, textvariable=variable, width=31, font=("Arial", 11)).grid(row=row, column=1, sticky="w", pady=8)

    def calculate_norm(self):
        try:
            name = self.name_var.get().strip()
            weight = float(self.weight_var.get())
            age = int(self.age_var.get())

            if not name:
                messagebox.showerror("Input error", "Please enter your name.")
                return
            if weight <= 0 or age <= 0:
                messagebox.showerror("Input error", "Weight and age must be positive numbers.")
                return

            goal = self.goal_var.get()
            multiplier = 30
            if goal == "Lose weight":
                multiplier = 35
            elif goal == "Active lifestyle":
                multiplier = 40

            self.daily_norm = int(weight * multiplier)
            self.drunk_water = 0
            self.update_labels()
            self.status_var.set(f"Status: Hi, {name}! Your daily water goal has been calculated.")
            self.tip_var.set(self.generate_tip(goal, age))
            self.start_reminder()
        except ValueError:
            messagebox.showerror("Input error", "Please enter valid numbers for weight and age.")

    def drink_water(self):
        if self.daily_norm == 0:
            messagebox.showwarning("Warning", "First calculate your daily norm.")
            return

        glass_volume = int(self.glass_var.get())
        self.drunk_water += glass_volume
        if self.drunk_water > self.daily_norm:
            self.drunk_water = self.daily_norm

        left = max(self.daily_norm - self.drunk_water, 0)
        self.update_labels()

        if left == 0:
            self.status_var.set("Status: Great job! You reached your daily water goal.")
            messagebox.showinfo("HydroTrack", "Congratulations! You have reached your daily water goal.")
        elif self.drunk_water >= self.daily_norm * 0.75:
            self.status_var.set("Status: Excellent progress. You are close to your goal.")
        elif self.drunk_water >= self.daily_norm * 0.4:
            self.status_var.set("Status: Good progress. Keep drinking water regularly.")
        else:
            self.status_var.set("Status: You have started well. Keep going.")

    def reset_data(self):
        self.name_var.set("")
        self.weight_var.set("")
        self.age_var.set("")
        self.goal_var.set("Keep healthy")
        self.glass_var.set("250")
        self.reminder_var.set("30")
        self.daily_norm = 0
        self.drunk_water = 0
        self.daily_norm_var.set("Daily norm: 0 ml")
        self.drunk_var.set("Drunk today: 0 ml")
        self.left_var.set("Left to drink: 0 ml")
        self.status_var.set("Status: Enter your data and press Calculate")
        self.tip_var.set("Tip: Drink water regularly in small portions during the day.")
        self.progress["value"] = 0
        if self.reminder_job:
            self.root.after_cancel(self.reminder_job)
            self.reminder_job = None

    def update_labels(self):
        left = max(self.daily_norm - self.drunk_water, 0)
        self.daily_norm_var.set(f"Daily norm: {self.daily_norm} ml")
        self.drunk_var.set(f"Drunk today: {self.drunk_water} ml")
        (self.left_var.
         set(f"Left to drink: {left} ml"))
        progress_value = (self.drunk_water / self.daily_norm) * 100 if self.daily_norm else 0
        self.progress["value"] = progress_value

    def generate_tip(self, goal, age):
        if goal == "Lose weight":
            return "Drink water before meals and spread your intake evenly throughout the day."
        if goal == "Active lifestyle":
            return "With higher activity, your body loses more fluid, so drink water regularly."
        if age < 18:
            return "Maintain a regular drinking routine and avoid replacing water with sugary drinks."
        return "Drink water in small portions during the day to maintain a stable water balance."

    def start_reminder(self):
        if self.reminder_job:
            self.root.after_cancel(self.reminder_job)
        minutes = int(self.reminder_var.get())
        self.reminder_job = self.root.after(minutes * 60 * 1000, self.show_reminder)

    def show_reminder(self):
        messagebox.showinfo("HydroTrack Reminder", "Time to drink some water!")
        self.start_reminder()


if __name__ == "__main__":
    root = tk.Tk()
    app = HydroTrackApp(root)
    root.mainloop()