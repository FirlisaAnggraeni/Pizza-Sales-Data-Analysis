import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PizzaSales:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Sales Data Analysis")
        self.root.geometry("600x450")
        
        # Set colors
        self.bg_color = "#003366"  
        self.button_bg_color = "#00bcd4"  
        self.button_fg_color = "#000000" 
        self.plot_bg_color = "#ffffff"  
        self.line_color = "#059995" 
        
        
        self.root.configure(bg=self.bg_color)
        
        # Define DataFrame
        self.df = pd.DataFrame()
        
        
        self.create_widgets()
        
        # load data
        self.load_data()

    def create_widgets(self):
        
        self.button_frame = tk.Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        self.button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Show top 10 pizzas
        self.show_top_pizzas_button = tk.Button(self.button_frame, text="Show Top 10 Most Popular Pizzas", command=self.show_top_pizzas, bg=self.button_bg_color, fg=self.button_fg_color, font=("Helvetica", 12, "bold"))
        self.show_top_pizzas_button.pack(pady=5, fill=tk.X)

        # Show 10 most unpopular pizzas
        self.show_unpop_pizzas_button = tk.Button(self.button_frame, text="Show 10 Most Unpopular Pizzas", command=self.show_unpop_pizzas, bg=self.button_bg_color, fg=self.button_fg_color, font=("Helvetica", 12, "bold"))
        self.show_unpop_pizzas_button.pack(pady=5, fill=tk.X)
        
        # Plot total orders by month
        self.plot_orders_button = tk.Button(self.button_frame, text="Plot Total Orders by Month", command=self.plot_orders_by_month, bg=self.button_bg_color, fg=self.button_fg_color, font=("Helvetica", 12, "bold"))
        self.plot_orders_button.pack(pady=5, fill=tk.X)
        
        # Plot total income by month
        self.plot_income_button = tk.Button(self.button_frame, text="Plot Total Income by Month", command=self.plot_income_by_month, bg=self.button_bg_color, fg=self.button_fg_color, font=("Helvetica", 12, "bold"))
        self.plot_income_button.pack(pady=5, fill=tk.X)
        
        # Show most and least popular pizza categories
        self.show_pop_least_pop_categories_button = tk.Button(self.button_frame, text="Show Most and Least Popular Pizza Categories", command=self.show_pop_least_pop_categories, bg=self.button_bg_color, fg=self.button_fg_color, font=("Helvetica", 12, "bold"))
        self.show_pop_least_pop_categories_button.pack(pady=5, fill=tk.X)
        
        # Quit button
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.root.quit, bg="#f44336", fg="#000000", font=("Helvetica", 12, "bold"))  # Red background for Quit button
        self.quit_button.pack(pady=5, fill=tk.X)

    def load_data(self):
        try:
            # Connect database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="finalproject"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pizza_sales")
            rows = cursor.fetchall()
            conn.close()
            
            # Convert data to DataFrame
            self.df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
            
            print("Data loaded successfully")  
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error connecting to database:\n{err}")

    def plot_orders_by_month(self):
        if 'order_date' in self.df.columns and 'quantity' in self.df.columns:
            self.df['order_date'] = pd.to_datetime(self.df['order_date'])
            self.df['month'] = self.df['order_date'].dt.to_period('M')
            orders_by_month = self.df.groupby('month')['quantity'].sum()
            
            # Create a new window for the plot
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Total Orders")
            plot_window.geometry("600x400")
            plot_window.configure(bg=self.plot_bg_color)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            orders_by_month.plot(kind='line', marker='o', ax=ax, color=self.line_color)
            ax.set_title('Total Orders', fontsize=14, fontweight='bold')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Total Orders', fontsize=12)
            ax.grid(True)
            
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Warning", "Columns 'order_date' and 'quantity' must be present in data.")

    def plot_income_by_month(self):
        if 'order_date' in self.df.columns and 'total_price' in self.df.columns:
            self.df['order_date'] = pd.to_datetime(self.df['order_date'])
            self.df['month'] = self.df['order_date'].dt.to_period('M')
            income_by_month = self.df.groupby('month')['total_price'].sum()
            
            # Create a new window for the plot
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Total Income")
            plot_window.geometry("600x400")
            plot_window.configure(bg=self.plot_bg_color)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            income_by_month.plot(kind='line', marker='o', ax=ax, color=self.line_color)
            ax.set_title('Total Income', fontsize=14, fontweight='bold')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Total Income', fontsize=12)
            ax.grid(True)
            
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Warning", "Columns 'order_date' and 'total_price' must be present in data.")

    def show_top_pizzas(self):
        if 'pizza_name' in self.df.columns and 'quantity' in self.df.columns:
            top_pizzas = self.df.groupby('pizza_name')['quantity'].sum().sort_values(ascending=False).head(10)
            
            # Create a new window for the table
            top_window = tk.Toplevel(self.root)
            top_window.title("Top 10 Most Popular Pizzas")
            top_window.geometry("400x300")
            top_window.configure(bg=self.bg_color)
            
            top_tree = ttk.Treeview(top_window, columns=("Pizza Name", "Total Sales"), show='headings')
            top_tree.heading("Pizza Name", text="Pizza Name")
            top_tree.heading("Total Sales", text="Total Sales")
            top_tree.pack(fill=tk.BOTH, expand=True)
            
            for pizza, sales in top_pizzas.items():
                top_tree.insert("", tk.END, values=(pizza, sales))
        else:
            messagebox.showwarning("Warning", "Columns 'pizza_name' and 'quantity' must be present in data to show top pizzas.")
    
    def show_unpop_pizzas(self):
        if 'pizza_name' in self.df.columns and 'quantity' in self.df.columns:
            unpop_pizzas = self.df.groupby('pizza_name')['quantity'].sum().sort_values(ascending=True).head(10)
            
            # Create a new window for the table
            unpop_window = tk.Toplevel(self.root)
            unpop_window.title("10 Most Unpopular Pizzas")
            unpop_window.geometry("400x300")
            unpop_window.configure(bg=self.bg_color)
            
            unpop_tree = ttk.Treeview(unpop_window, columns=("Pizza Name", "Total Sales"), show='headings')
            unpop_tree.heading("Pizza Name", text="Pizza Name")
            unpop_tree.heading("Total Sales", text="Total Sales")
            unpop_tree.pack(fill=tk.BOTH, expand=True)
            
            for pizza, sales in unpop_pizzas.items():
                unpop_tree.insert("", tk.END, values=(pizza, sales))
        else:
            messagebox.showwarning("Warning", "Columns 'pizza_name' and 'quantity' must be present in data to show unpopular pizzas.")
    
    def show_pop_least_pop_categories(self):
        if 'pizza_category' in self.df.columns and 'quantity' in self.df.columns:
            category_sales = self.df.groupby('pizza_category')['quantity'].sum()
            most_pop_category = category_sales.idxmax()
            least_pop_category = category_sales.idxmin()
            most_pop_sales = category_sales.max()
            least_pop_sales = category_sales.min()

            # Create a new window for the results
            category_window = tk.Toplevel(self.root)
            category_window.title("Most and Least Popular Pizza Categories")
            category_window.geometry("400x300")
            category_window.configure(bg=self.bg_color)
            
            # Display the results
            tk.Label(category_window, text=f"Most Popular Pizza Category: {most_pop_category}", bg=self.bg_color, fg=self.plot_bg_color, font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(category_window, text=f"Total Sales: {most_pop_sales}", bg=self.bg_color, fg=self.plot_bg_color, font=("Helvetica", 12)).pack(pady=5)
            tk.Label(category_window, text=f"Least Popular Pizza Category: {least_pop_category}", bg=self.bg_color, fg=self.plot_bg_color, font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(category_window, text=f"Total Sales: {least_pop_sales}", bg=self.bg_color, fg=self.plot_bg_color, font=("Helvetica", 12)).pack(pady=5)
        else:
            messagebox.showwarning("Warning", "Columns 'pizza_category' and 'quantity' must be present in data.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PizzaSales(root)
    root.mainloop()
