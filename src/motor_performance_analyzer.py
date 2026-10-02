#*****************************************************************Analysis of DC Motor************************************************************

import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, filedialog
import numpy as np
import matplotlib.pyplot as plt
import csv

# --- OOP Structure: Base and Child Classes ---

class BaseMotorTest:
    """Base class for all motor tests, demonstrating inheritance."""
    def __init__(self, root):
        self.root = root

    def get_motor_life_inference(self, efficiency_list, rated_current, line_currents):
        """Provides a qualitative idea of machine life based on test results."""
        inference = "Machine Life Expectancy Insights:\n\n"
        
        eff_list = list(efficiency_list)
        if not eff_list:
            return "Could not generate insights due to lack of data."
            
        peak_efficiency = np.max(eff_list)

        inference += f"- The machine operates with a peak efficiency of {peak_efficiency:.2f}%. Higher efficiency means less energy is wasted as heat, which generally contributes to a longer lifespan.\n\n"

        # For a generator, line_currents refers to load current.
        overload_count = sum(1 for i in line_currents if i > rated_current)
        if overload_count > 0:
            inference += f"- WARNING: The machine was operated above its rated line current ({rated_current} A) for {overload_count} reading(s). Consistently running the machine in an overloaded state generates excessive heat and mechanical stress, which will significantly shorten its operational life.\n\n"
        else:
            inference += "- The machine was operated within its rated current limits during the test, which is good practice for ensuring longevity.\n\n"

        inference += "For maximum life, operate the machine close to its peak efficiency point and always within its rated voltage and current specifications."
        return inference

    def plot_graph(self, x_data, y_data_dict, title, x_label, y_label_main):
        """Plots one or more graphs on the same axes."""
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(y_label_main)
        ax1.grid(True)
        
        colors = ['b', 'g', 'r', 'c', 'm', 'y']
        
        for i, (key, values) in enumerate(y_data_dict.items()):
            ax1.plot(x_data, values, f'{colors[i % len(colors)]}-o', label=key)

        ax1.legend(loc='best')
        fig.suptitle(title, fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    # ------------------- FILE HANDLING METHODS -------------------
    def save_results_to_file(self, data_dict, default_filename="results.csv"):
        """Saves calculated test data into a CSV file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return  # user cancelled
        
        # Save dictionary data to CSV
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            headers = list(data_dict.keys())
            writer.writerow(headers)
            rows = zip(*data_dict.values())
            for row in rows:
                writer.writerow(row)
        
        messagebox.showinfo("File Saved", f"Results successfully saved to:\n{file_path}")

    def load_results_from_file(self):
        """Loads a CSV file and returns data as a dictionary."""
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return None
        
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            data = {field: [] for field in reader.fieldnames}
            for row in reader:
                for field in reader.fieldnames:
                    try:
                        data[field].append(float(row[field]))
                    except ValueError:
                        data[field].append(row[field])
        messagebox.showinfo("File Loaded", f"Data successfully loaded from:\n{file_path}")
        return data


# -------------------------------------------------------------------

class SwinburnesTest(BaseMotorTest):
    """Handles the logic for Swinburne's Test."""
    def run_test(self):
        self.select_win = Toplevel(self.root)
        self.select_win.title("Select Operation Mode")
        
        tk.Label(self.select_win, text="Choose the operation mode to predetermine performance:").pack(padx=20, pady=10)
        
        tk.Button(self.select_win, text="Motor Operation", command=lambda: self.get_inputs("motor")).pack(pady=5, padx=20, fill=tk.X)
        tk.Button(self.select_win, text="Generator Operation", command=lambda: self.get_inputs("generator")).pack(pady=5, padx=20, fill=tk.X)

    def get_inputs(self, mode):
        self.select_win.destroy()
        
        input_win = Toplevel(self.root)
        input_win.title("Swinburne's Test - Inputs")
        
        entries = {}
        fields = [
            "Supply Voltage, VL (V)", "Field Current, If (A)", "No-Load Line Current, IL0 (A)",
            "Armature Resistance, Ra (Ω)", "Rated Line Current (A)", "Rated Speed (rpm)"
        ]
        
        for i, field in enumerate(fields):
            row = tk.Frame(input_win)
            lab = tk.Label(row, width=25, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[field] = ent

        tk.Button(input_win, text="Calculate & Plot", command=lambda: self.calculate(entries, mode, input_win)).pack(pady=10)

    def calculate(self, entries, mode, window):
        try:
            v_l = float(entries["Supply Voltage, VL (V)"].get())
            i_f = float(entries["Field Current, If (A)"].get())
            i_l0 = float(entries["No-Load Line Current, IL0 (A)"].get())
            r_a = float(entries["Armature Resistance, Ra (Ω)"].get())
            i_l_rated = float(entries["Rated Line Current (A)"].get())
            n0 = float(entries["Rated Speed (rpm)"].get())
            
            i_a0 = i_l0 - i_f 
            no_load_input = v_l * i_l0 
            no_load_cu_loss = (i_a0**2) * r_a 
            p_c = no_load_input - no_load_cu_loss
            e0 = v_l - (i_a0 * r_a) 

            if mode == "motor":
                self.calculate_motor(v_l, i_f, r_a, p_c, i_l_rated, n0, e0)
            else:
                self.calculate_generator(v_l, i_f, r_a, p_c, i_l_rated)
            
            window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {e}")

    def calculate_motor(self, v_l, i_f, r_a, p_c, i_l_rated, n0, e0):
        line_currents = np.linspace(0.1 * i_l_rated, 1.25 * i_l_rated, 10)
        p_out_vals, eff_vals, n_vals, t_vals, i_l_plot_vals = [], [], [], [], []

        for i_l in line_currents:
            if i_l <= i_f: continue
            
            i_a = i_l - i_f
            p_cu = (i_a**2) * r_a
            total_loss = p_cu + p_c
            p_in = v_l * i_l
            p_out = p_in - total_loss
            if p_in == 0: continue
            eff = (p_out / p_in) * 100
            
            e = v_l - (i_a * r_a)
            speed = (e / e0) * n0 if e0 != 0 else 0
            torque = (p_out * 60) / (2 * np.pi * speed) if speed != 0 else 0
            
            p_out_vals.append(p_out)
            eff_vals.append(eff)
            n_vals.append(speed)
            t_vals.append(torque)
            i_l_plot_vals.append(i_l)
            
        self.plot_graph(
            p_out_vals,
            {'Efficiency (%)': eff_vals, 'Speed (rpm)': n_vals, 'Torque (Nm)': t_vals, 'Line Current (A)': i_l_plot_vals},
            "Predetermined Motor Performance Characteristics (Swinburne's)",
            "Output Power (W)",
            "Value"
        )
        
        inference = self.get_motor_life_inference(eff_vals, i_l_rated, line_currents)
        messagebox.showinfo("Machine Life Inference", inference)

        # --- Save results ---
        if messagebox.askyesno("Save Results", "Would you like to save these results to a file?"):
            self.save_results_to_file({
                "Line Current (A)": i_l_plot_vals,
                "Output Power (W)": p_out_vals,
                "Efficiency (%)": eff_vals,
                "Speed (rpm)": n_vals,
                "Torque (Nm)": t_vals
            }, default_filename="swinburne_motor_results.csv")

    def calculate_generator(self, v_l, i_f, r_a, p_c, i_l_rated):
        load_currents = np.linspace(0.1 * i_l_rated, 1.25 * i_l_rated, 10)
        p_out_vals, eff_vals = [], []

        for i_l in load_currents:
            i_a = i_l + i_f
            p_cu = (i_a**2) * r_a
            total_loss = p_cu + p_c
            p_out = v_l * i_l
            p_in = p_out + total_loss
            if p_in == 0: continue
            eff = (p_out / p_in) * 100
            
            p_out_vals.append(p_out)
            eff_vals.append(eff)
        
        self.plot_graph(
            p_out_vals,
            {'Efficiency (%)': eff_vals},
            "Predetermined Generator Performance (Swinburne's)",
            "Output Power (W)",
            "Efficiency (%)"
        )
        
        inference = self.get_motor_life_inference(eff_vals, i_l_rated, load_currents)
        messagebox.showinfo("Machine Life Inference", inference)

        if messagebox.askyesno("Save Results", "Would you like to save these generator results to a file?"):
            self.save_results_to_file({
                "Load Current (A)": load_currents,
                "Output Power (W)": p_out_vals,
                "Efficiency (%)": eff_vals
            }, default_filename="swinburne_generator_results.csv")


# -------------------------------------------------------------------

class LoadTest(BaseMotorTest):
    """Parent class for common load test logic, inheriting from BaseMotorTest."""
    def __init__(self, root, motor_type):
        super().__init__(root)
        self.motor_type = motor_type
        self.entries = []

    def get_inputs(self):
        try:
            num_readings = simpledialog.askinteger("Input", "Enter number of readings (min 5):", parent=self.root, minvalue=5, maxvalue=15)
            if not num_readings: return

            self.input_win = Toplevel(self.root)
            self.input_win.title(f"{self.motor_type} Load Test - Data Entry")

            header_frame = tk.Frame(self.input_win)
            header_frame.pack()
            tk.Label(header_frame, text="Brake Drum Radius (m):").grid(row=0, column=0, padx=5, pady=5)
            self.radius_entry = tk.Entry(header_frame)
            self.radius_entry.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(header_frame, text="Rated Current (A):").grid(row=1, column=0, padx=5, pady=5)
            self.rated_current_entry = tk.Entry(header_frame)
            self.rated_current_entry.grid(row=1, column=1, padx=5, pady=5)

            table_frame = tk.Frame(self.input_win)
            table_frame.pack(pady=10)
            
            headings = ["Voltage (V)", "Current (A)", "S1 (kg)", "S2 (kg)", "Speed (rpm)"]
            for j, heading in enumerate(headings):
                tk.Label(table_frame, text=heading, font='Helvetica 10 bold').grid(row=0, column=j, padx=5, pady=2)

            for i in range(num_readings):
                row_entries = []
                for j in range(len(headings)):
                    entry = tk.Entry(table_frame, width=10)
                    entry.grid(row=i + 1, column=j)
                    row_entries.append(entry)
                self.entries.append(row_entries)
            
            tk.Button(self.input_win, text="Calculate & Plot", command=self.calculate).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def calculate(self):
        try:
            radius = float(self.radius_entry.get())
            rated_current = float(self.rated_current_entry.get())
            
            readings = []
            for row_entries in self.entries:
                row_data = [float(e.get()) for e in row_entries]
                readings.append(row_data)
            
            readings_arr = np.array(readings)
            v_l, i_l, s1, s2, n = readings_arr.T
            
            p_in = v_l * i_l
            force = s1 - s2
            torque = force * radius * 9.81
            p_out = (2 * np.pi * n * torque) / 60
            
            efficiency = np.zeros_like(p_in)
            non_zero_mask = p_in != 0
            efficiency[non_zero_mask] = (p_out[non_zero_mask] / p_in[non_zero_mask]) * 100

            self.input_win.destroy()
            
            self.plot_graph(
                p_out,
                {'Efficiency (%)': efficiency, 'Speed (rpm)': n, 'Torque (Nm)': torque, 'Line Current (A)': i_l},
                f"{self.motor_type} Motor Performance Characteristics",
                "Output Power (W)",
                "Value"
            )

            self.plot_graph(
                torque,
                {'Speed (rpm)': n},
                f"{self.motor_type} Motor Mechanical Characteristic",
                "Torque (Nm)",
                "Speed (rpm)"
            )
            
            inference = self.get_motor_life_inference(efficiency, rated_current, i_l)
            messagebox.showinfo("Machine Life Inference", inference)

            # --- Save results ---
            if messagebox.askyesno("Save Results", "Would you like to save these load test results to a file?"):
                self.save_results_to_file({
                    "Voltage (V)": v_l,
                    "Current (A)": i_l,
                    "Speed (rpm)": n,
                    "Torque (Nm)": torque,
                    "Efficiency (%)": efficiency,
                    "Output Power (W)": p_out
                }, default_filename=f"{self.motor_type.lower().replace(' ', '_')}_load_results.csv")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all data fields are filled with valid numbers.")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {e}")


class SeriesMotorLoadTest(LoadTest):
    """Specific class for Series Motor Load Test."""
    def __init__(self, root):
        super().__init__(root, "DC Series")

class ShuntMotorLoadTest(LoadTest):
    """Specific class for Shunt Motor Load Test."""
    def __init__(self, root):
        super().__init__(root, "DC Shunt")


# -------------------------------------------------------------------

class MotorTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor Performance Analyzer")
        self.root.geometry("350x200")

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(main_frame, text="Select an Experiment", font='Helvetica 12 bold').pack(pady=(0, 10))

        tk.Button(main_frame, text="Swinburne's Test", command=self.run_swinburnes).pack(fill=tk.X, pady=5)
        tk.Button(main_frame, text="Load Test on DC Series Motor", command=self.run_series_load).pack(fill=tk.X, pady=5)
        tk.Button(main_frame, text="Load Test on DC Shunt Motor", command=self.run_shunt_load).pack(fill=tk.X, pady=5)

        # --- Menu Bar for File Handling ---
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Saved Data", command=self.load_saved_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def run_swinburnes(self):
        test = SwinburnesTest(self.root)
        test.run_test()

    def run_series_load(self):
        test = SeriesMotorLoadTest(self.root)
        test.get_inputs()

    def run_shunt_load(self):
        test = ShuntMotorLoadTest(self.root)
        test.get_inputs()

    def load_saved_data(self):
        base = BaseMotorTest(self.root)
        data = base.load_results_from_file()
        if data:
            x_label = list(data.keys())[0]
            y_data = {k: v for k, v in data.items() if k != x_label}
            base.plot_graph(data[x_label], y_data, "Loaded Test Data", x_label, "Value")


# -------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorTestApp(root)
    root.mainloop() 