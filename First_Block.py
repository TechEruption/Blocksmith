import hashlib
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta, timezone

# ===========================
# Block Class
# ===========================

class Block:
    def __init__(self, index, previous_hash, data, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash

        # Set Indian Standard Time (UTC+5:30)
        ist = timezone(timedelta(hours=5, minutes=30))
        self.timestamp = timestamp or datetime.now(ist)

        self.data = data
        self.transactions = transactions
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.transactions}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# ===========================
# GUI
# ===========================

class BlockchainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🪙 BlockForge – Build Your Blockchain")
        self.root.geometry("850x650")
        self.root.config(bg="#FFE5B4")  # Peach color background

        self.previous_hash = "0"
        self.block_index = 0

        # === Title area ===

        title = tk.Label(root, text="🪙 BlockForge – Build Your Blockchain", 
                         font=("Arial", 20, "bold"), fg="#3B2F2F", bg="#FFE5B4")
        title.pack(pady=15)

        # === Frame for block data input ===

        data_frame = tk.LabelFrame(root, text=" Block Content ", 
                                   font=("Arial", 12, "bold"), fg="#3B2F2F", bg="#FFE5B4", bd=3)
        data_frame.pack(pady=10, padx=20, fill="x")

        self.data_entry = tk.Entry(data_frame, font=("Arial", 12), width=60, fg="#3B2F2F", bg="#FFF8DC", relief="sunken")
        self.data_entry.pack(pady=8, padx=10)

        # === Frame for transactions input ===

        tx_frame = tk.LabelFrame(root, text=" Ledger Records ", 
                                 font=("Arial", 12, "bold"), fg="#3B2F2F", bg="#FFE5B4", bd=3)
        tx_frame.pack(pady=10, padx=20, fill="x")

        self.transactions_entry = tk.Text(tx_frame, height=6, width=70, font=("Arial", 11), 
                                          fg="#3B2F2F", bg="#FFF8DC", relief="sunken")
        self.transactions_entry.pack(pady=8, padx=10)

        # === Button Frame ===

        btn_frame = tk.Frame(root, bg="#FFE5B4")
        btn_frame.pack(pady=15)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=6)

        self.create_button = ttk.Button(btn_frame, text="➕ Create Block", command=self.create_block)
        self.create_button.pack()

        # === Output area with BLACK border only for last block ===

        output_frame = tk.LabelFrame(root, text=" Latest Block ", 
                                  font=("Arial", 12, "bold"), fg="#3B2F2F", bg="#FFE5B4", bd=3)
        output_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.output = tk.Text(output_frame, height=18, width=95, 
                              bg="#FFF8DC", fg="#3B2F2F", font=("Consolas", 10), relief="sunken")
        self.output.pack(pady=10, padx=10)

    def create_block(self):
        data = self.data_entry.get() or "Empty Block"
        transactions_text = self.transactions_entry.get("1.0", tk.END).strip()
        transactions = transactions_text.split("\n") if transactions_text else ["No Records"]

        block = Block(self.block_index, self.previous_hash, data, transactions)
        self.previous_hash = block.hash
        self.block_index += 1

        # Format timestamp (IST)

        timestamp_str = block.timestamp.strftime("%Y-%m-%d %H:%M:%S (IST)")

        # Clear old highlight

        self.output.tag_delete("last_block")
        self.output.tag_configure("last_block", borderwidth=2, relief="solid", background="#FFDAB9")

        # Display the block details

        start_index = self.output.index(tk.END)
        self.output.insert(tk.END, f"\n🔹 Block {block.index}\n")
        self.output.insert(tk.END, f"Content: {block.data}\n")
        self.output.insert(tk.END, f"Timestamp: {timestamp_str}\n")
        self.output.insert(tk.END, f"Hash: {block.hash}\n")
        self.output.insert(tk.END, f"Previous Hash: {block.previous_hash}\n")
        self.output.insert(tk.END, "Ledger Records:\n")
        for tx in block.transactions:
            self.output.insert(tk.END, f"   - {tx}\n")
        self.output.insert(tk.END, "-"*80 + "\n")
        end_index = self.output.index(tk.END)

        # Highlight last block with BLACK border effect

        self.output.tag_add("last_block", start_index, end_index)

        # Clear input fields

        self.data_entry.delete(0, tk.END)
        self.transactions_entry.delete("1.0", tk.END)
        
# ==========
# Run app
# ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()
