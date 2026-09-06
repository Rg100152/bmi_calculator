import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Classic Java Swing Style Colors
BG_COLOR = "#d4d0c8"  # Classic Windows/Grey
BORDER = "#808080"
BLACK = "#000000"
WHITE = "#ffffff"
BLUE = "#000080"

class BMICalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("bmi")
        self.geometry("450x400")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        # Main Layout
        main_frame = tk.Frame(self, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # --- Top Row: Name and Age ---
        top_frame = tk.Frame(main_frame, bg=BG_COLOR)
        top_frame.pack(fill="x", pady=(0, 15))

        # Name
        tk.Label(top_frame, text="Name:", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.name_entry = tk.Entry(top_frame, bg=WHITE, fg=BLACK, font=("Arial", 12), width=22, bd=2, relief="sunken")
        self.name_entry.insert(0, "John Smith")
        self.name_entry.grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(5, 0))

        # Age
        tk.Label(top_frame, text="Age:", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w", padx=(0, 10))
        self.age_entry = tk.Entry(top_frame, bg=WHITE, fg=BLACK, font=("Arial", 12), width=8, bd=2, relief="sunken")
        self.age_entry.insert(0, "24")
        self.age_entry.grid(row=1, column=1, sticky="w", pady=(5, 0))

        # --- Middle Row: Units Selection and Clear Button ---
        mid_frame = tk.Frame(main_frame, bg=BG_COLOR)
        mid_frame.pack(fill="x", pady=(10, 15))

        # Units Group (Sunken Border Frame)
        units_group = tk.LabelFrame(mid_frame, text="Select Units", bg=BG_COLOR, fg=BLACK, font=("Arial", 10, "bold"), bd=2, relief="groove")
        units_group.grid(row=0, column=0, sticky="w", padx=(0, 20), pady=(5, 0))

        self.units_var = tk.StringVar(value="imperial")
        
        tk.Radiobutton(units_group, text="lbs / in", variable=self.units_var, value="imperial", bg=BG_COLOR, font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Radiobutton(units_group, text="kg / cm", variable=self.units_var, value="metric", bg=BG_COLOR, font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Clear Button (Matches the Image)
        self.clear_btn = tk.Button(mid_frame, text="Clear", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold"), bd=2, relief="raised", padx=30, command=self.clear_all)
        self.clear_btn.grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(5, 0))

        # --- Bottom Row: Weight, Height, Calculate, Save ---
        bottom_frame = tk.Frame(main_frame, bg=BG_COLOR)
        bottom_frame.pack(fill="x", pady=(10, 15))

        # Weight and Height
        weight_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
        weight_frame.grid(row=0, column=0, sticky="w", padx=(0, 30))

        tk.Label(weight_frame, text="Weight (lb):", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.weight_label = tk.Label(weight_frame, text="Weight (lb):", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold"))
        self.weight_entry = tk.Entry(weight_frame, bg=WHITE, fg=BLACK, font=("Arial", 12), width=10, bd=2, relief="sunken")
        self.weight_entry.insert(0, "156")
        self.weight_entry.grid(row=1, column=0, sticky="w", pady=(5, 0))

        height_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
        height_frame.grid(row=0, column=1, sticky="w")

        tk.Label(height_frame, text="Height (in):", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.height_entry = tk.Entry(height_frame, bg=WHITE, fg=BLACK, font=("Arial", 12), width=10, bd=2, relief="sunken")
        self.height_entry.insert(0, "76")
        self.height_entry.grid(row=1, column=0, sticky="w", pady=(5, 0))

        # Result Label
        self.result_label = tk.Label(bottom_frame, text="Result:   19 Normal", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold"))
        self.result_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(15, 0))

        # Buttons on Right
        btn_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
        btn_frame.grid(row=0, column=2, rowspan=3, sticky="n", padx=(30, 0))

        self.calc_btn = tk.Button(btn_frame, text="Calculate BMI", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold"), bd=2, relief="raised", padx=20, pady=5, command=self.calculate_bmi)
        self.calc_btn.pack(pady=(10, 15), fill="x")

        self.save_btn = tk.Button(btn_frame, text="Save to BMI.xls", bg=BG_COLOR, fg=BLACK, font=("Arial", 12, "bold"), bd=2, relief="raised", padx=20, pady=5, command=self.save_to_excel)
        self.save_btn.pack(fill="x")

    def clear_all(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.result_label.config(text="Result:")
        self.units_var.set("imperial")
        # Reset labels based on units
        self.weight_label.config(text="Weight (lb):")
        tk.Label(self, text="").pack() # Reset visibility
        # Re-setup labels
        tk.Label(self, text="").pack_forget()

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            units = self.units_var.get()

            if units == "imperial":
                # BMI = (weight in lbs * 703) / (height in inches^2)
                bmi = (weight * 703) / (height ** 2)
            else:
                # BMI = weight in kg / (height in m^2)
                # Assuming inputs are cm
                height_m = height / 100
                bmi = weight / (height_m ** 2)

            bmi = round(bmi, 1)

            # Determine Category
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                category = "Normal"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obese"

            self.result_label.config(text=f"Result:   {bmi} {category}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Weight and Height!")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Height cannot be zero!")

    def save_to_excel(self):
        try:
            name = self.name_entry.get() or "Unknown"
            age = self.age_entry.get() or "N/A"
            weight = self.weight_entry.get() or "N/A"
            height = self.height_entry.get() or "N/A"
            result_text = self.result_label.cget("text").replace("Result:", "").strip()

            # Create a simple text file (since we don't have openpyxl/xlwt installed)
            with open("BMI_Results.txt", "a") as f:
                f.write(f"Name: {name}, Age: {age}, Weight: {weight}, Height: {height}, Result: {result_text}\n")

            messagebox.showinfo("Success", "Data saved to BMI_Results.txt (Simulated .xls)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_units_change(self):
        if self.units_var.get() == "imperial":
            self.weight_label.config(text="Weight (lb):")
            # Update height label
            # (We need to find the height label)
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    for sub_child in child.winfo_children():
                        if isinstance(sub_child, tk.Frame):
                            for widget in sub_child.winfo_children():
                                if isinstance(widget, tk.Label) and "Height" in widget.cget("text"):
                                    widget.config(text="Height (in):")
        else:
            self.weight_label.config(text="Weight (kg):")
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    for sub_child in child.winfo_children():
                        if isinstance(sub_child, tk.Frame):
                            for widget in sub_child.winfo_children():
                                if isinstance(widget, tk.Label) and "Height" in widget.cget("text"):
                                    widget.config(text="Height (cm):")

if __name__ == "__main__":
    app = BMICalculator()
    app.mainloop()
