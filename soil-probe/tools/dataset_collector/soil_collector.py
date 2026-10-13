#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os
import time
import threading
from datetime import datetime

class SoilCollectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soil Probe Dataset Collector")
        self.root.geometry("600x500")
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Serial connection variables
        self.serial_port = None
        self.is_connected = False
        
        # Create UI
        self.create_widgets()
        
        # Soil classes
        self.soil_classes = ['red_soil', 'black_soil', 'alluvial_soil', 'laterite_soil', 'sandy_soil', 'clay_soil']
        self.selected_class = tk.StringVar(value=self.soil_classes[0])
        
        # Create dataset directory structure
        self.dataset_dir = "dataset"
        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)
        for soil_class in self.soil_classes:
            class_dir = os.path.join(self.dataset_dir, soil_class)
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Top section - Serial connection
        conn_frame = ttk.LabelFrame(main_frame, text="Serial Connection", padding="5")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(conn_frame, text="COM Port:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(conn_frame, textvariable=self.port_var, width=20)
        self.port_combo.grid(row=0, column=1, padx=(0, 10))
        
        self.refresh_button = ttk.Button(conn_frame, text="Refresh", command=self.refresh_ports)
        self.refresh_button.grid(row=0, column=2, padx=(0, 10))
        
        self.connect_button = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_button.grid(row=0, column=3, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(conn_frame, text="Not connected")
        self.status_label.grid(row=0, column=4, padx=(0, 10))
        
        # Middle section - Soil class selection and capture
        class_frame = ttk.LabelFrame(main_frame, text="Soil Class", padding="5")
        class_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(class_frame, text="Select soil type:").grid(row=0, column=0, sticky=tk.W)
        self.class_combo = ttk.Combobox(class_frame, textvariable=self.selected_class, 
                                       values=self.soil_classes, state="readonly", width=20)
        self.class_combo.grid(row=0, column=1, padx=(10, 0))
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="5")
        preview_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_label = ttk.Label(preview_frame, text="No image preview")
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Capture button
        self.capture_button = ttk.Button(main_frame, text="Capture Image", 
                                       command=self.capture_image, state=tk.DISABLED)
        self.capture_button.grid(row=3, column=0, pady=(0, 10))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_text = tk.Text(progress_frame, height=6, width=70)
        self.progress_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for progress
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.progress_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.progress_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Initial refresh of ports
        self.refresh_ports()
    
    def refresh_ports(self):
        """Refresh available COM ports"""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.port_combo['values'] = port_list
        
        if not self.port_var.get() and port_list:
            self.port_var.set(port_list[0])
    
    def toggle_connection(self):
        """Toggle connection to the device"""
        if self.is_connected:
            self.disconnect_device()
        else:
            self.connect_device()
    
    def connect_device(self):
        """Connect to the serial device"""
        port = self.port_var.get()
        if not port:
            messagebox.showerror("Error", "No COM port selected")
            return
            
        try:
            # Try connecting with DTR/RTS low
            self.serial_port = serial.Serial(port, 921600, timeout=2)
            
            # Reset into run mode (this is a simplified approach)
            self.serial_port.setDTR(False)
            self.serial_port.setRTS(True)
            time.sleep(0.1)
            self.serial_port.setRTS(False)
            time.sleep(0.1)
            
            # Test if we can communicate
            self.serial_port.flushInput()
            self.is_connected = True
            self.status_label.config(text="Connected")
            self.connect_button.config(text="Disconnect")
            self.capture_button.config(state=tk.NORMAL)
            
            self.log_message("Connected to device on " + port)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
            if self.serial_port:
                self.serial_port.close()
    
    def disconnect_device(self):
        """Disconnect from the serial device"""
        if self.serial_port and self.is_connected:
            self.serial_port.close()
            self.is_connected = False
            self.status_label.config(text="Disconnected")
            self.connect_button.config(text="Connect")
            self.capture_button.config(state=tk.DISABLED)
            
            self.log_message("Disconnected from device")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.progress_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.progress_text.see(tk.END)
    
    def capture_image(self):
        """Capture image from device and save it"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        try:
            # Send 'C' command to capture
            self.serial_port.write(b'C')
            self.serial_port.flush()
            
            # Read the header
            header = self.serial_port.read(4)
            if not header or len(header) < 4:
                raise Exception("Invalid response header")
                
            # Check for IMG header
            if header[0] != ord('I') or header[1] != ord('M') or header[2] != ord('G') or header[3] != ord('!'):
                err_data = self.serial_port.read(1024)
                error_msg = err_data.decode('utf-8', errors='ignore')
                raise Exception(f"Device error: {error_msg}")
            
            # Read 4-byte length (little-endian)
            length_bytes = self.serial_port.read(4)
            if len(length_bytes) < 4:
                raise Exception("Incomplete length data")
                
            length = int.from_bytes(length_bytes, 'little')
            
            # Read JPEG data
            jpeg_data = self.serial_port.read(length)
            if len(jpeg_data) != length:
                raise Exception(f"Image size mismatch. Expected {length}, got {len(jpeg_data)}")
            
            # Save image
            soil_class = self.selected_class.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{soil_class}_{timestamp}.jpg"
            file_path = os.path.join(self.dataset_dir, soil_class, filename)
            
            with open(file_path, 'wb') as f:
                f.write(jpeg_data)
                
            self.log_message(f"Saved image: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Capture failed: {str(e)}")
            self.log_message(f"Capture error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SoilCollectorApp(root)
    root.mainloop()