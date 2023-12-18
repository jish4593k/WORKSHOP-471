import torch
import tkinter as tk
from tkinter import messagebox
from scipy.stats import norm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ReportGenerator:
    def __init__(self, data_tensor):
        self.data_tensor = data_tensor

    def generate_pdf_report(self, output_path):
        pdf_path = os.path.join(output_path, 'report.pdf')
        with canvas.Canvas(pdf_path, pagesize=letter) as c:
            c.drawString(72, 800, "PyTorch and SciPy Report")

            histogram_data = self.data_tensor.numpy()
            self.plot_histogram(c, histogram_data)

        return pdf_path

    def plot_histogram(self, canvas, data):
      
        bin_edges = [i for i in range(min(data), max(data) + 2)]  
        bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges) - 1)]
        probabilities = norm.pdf(bin_centers, loc=data.mean(), scale=data.std())

       
        probabilities /= probabilities.sum()

      
        for edge, prob in zip(bin_edges[:-1], probabilities):
            canvas.rect(edge * 5, 100, 5, prob * 200, fill=1)
        canvas.setStrokeColorRGB(1, 0, 0)
        canvas.setLineWidth(2)
        canvas.drawCurve(bin_centers, [prob * 200 for prob in probabilities])

class AppGUI:
    def __init__(self, master):
        self.master = master
        master.title("PyTorch and SciPy App")

        self.label = tk.Label(master, text="Enter PyTorch tensor data (comma-separated):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.generate_button = tk.Button(master, text="Generate PDF Report", command=self.generate_report)
        self.generate_button.pack()

    def generate_report(self):
        try:
            data_str = self.entry.get()
            data_list = [float(item) for item in data_str.split(',')]
            data_tensor = torch.tensor(data_list)

            report_generator = ReportGenerator(data_tensor)
            output_path = os.getcwd()
            pdf_path = report_generator.generate_pdf_report(output_path)

            messagebox.showinfo("Report Generated", f"PDF Report generated at:\n{pdf_path}")

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter comma-separated numerical values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
