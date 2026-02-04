#!/usr/bin/env python3
"""
TMflow Security Report Generator - UI Prototype
使用 tkinter 實作的圖形化介面原型
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from datetime import datetime

class TMflowReportGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.load_default_config()
        
    def setup_window(self):
        """設定主視窗"""
        self.root.title("TMflow Security Report Generator v1.0.2")
        self.root.geometry("1000x750")  # 增加高度
        self.root.resizable(True, True)
        
        # 設定圖示（如果有的話）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_variables(self):
        """設定變數"""
        self.api_token = tk.StringVar(value="svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq")
        self.subdomain = tk.StringVar(value="tm-robot")
        self.organization = tk.StringVar(value="Techman Robot")
        self.connection_status = tk.StringVar(value="未連接")
        self.output_path = tk.StringVar(value=os.path.join(os.getcwd(), "reports"))
        self.standard_report = tk.BooleanVar(value=True)
        self.detailed_report = tk.BooleanVar(value=False)
        self.include_timestamp = tk.BooleanVar(value=True)
        self.filename_preview = tk.StringVar(value="TMflow_[版本]_[類型]_[時間戳].pdf")
        
        # 模擬的專案資料 - TMflow 和 TM AI+ Trainer 是平行的產品
        self.projects_data = {
            "TMflow": [
                {"version": "2025-12-19", "project_id": "1172955022268328018", "version_id": "5069892298893061197", "selected": tk.BooleanVar()},
                {"version": "2.26.1000.0", "project_id": "1172955022268328018", "version_id": "8235615984846311447", "selected": tk.BooleanVar()},
                {"version": "2.26.1100.0", "project_id": "1172955022268328018", "version_id": "2501085896754652149", "selected": tk.BooleanVar()},
                {"version": "2.26.1200.0", "project_id": "1172955022268328018", "version_id": "1936462473699050499", "selected": tk.BooleanVar()},
            ],
            "TM AI+ Trainer": [
                {"version": "1.0.0", "project_id": "1172955022268328019", "version_id": "1936462473699050500", "selected": tk.BooleanVar()},
                {"version": "1.1.0", "project_id": "1172955022268328019", "version_id": "1936462473699050501", "selected": tk.BooleanVar()},
            ]
        }
    
    def create_widgets(self):
        """建立所有 UI 元件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 左側區域
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        
        # 右側日誌區域
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        self.create_api_connection_section(left_frame)
        self.create_projects_section(left_frame)
        self.create_report_options_section(left_frame)
        self.create_progress_section(left_frame)
        self.create_buttons_section(left_frame)
        self.create_log_section(right_frame)
    
    def create_api_connection_section(self, parent):
        """建立 API 連接區域"""
        # API Connection 群組
        api_group = ttk.LabelFrame(parent, text="API Connection", padding="10")
        api_group.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        api_group.columnconfigure(1, weight=1)
        
        # 第一行：API Token 和 Status & Connect 按鈕
        ttk.Label(api_group, text="API Token:").grid(row=0, column=0, sticky=tk.W, pady=2)
        token_entry = ttk.Entry(api_group, textvariable=self.api_token, show="*", width=25)  # 縮短 Token 欄位
        token_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 20), pady=2)
        
        # Status 和 Connect 按鈕在同一行
        status_frame = ttk.Frame(api_group)
        status_frame.grid(row=0, column=2, sticky=tk.E, pady=2)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, textvariable=self.connection_status, foreground="red")
        self.status_label.pack(side=tk.LEFT, padx=(5, 10))
        
        self.connect_btn = ttk.Button(status_frame, text="Connect & Load Projects", command=self.connect_api)
        self.connect_btn.pack(side=tk.LEFT)
        
        # 第二行：Subdomain
        ttk.Label(api_group, text="Subdomain:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(api_group, textvariable=self.subdomain, width=20).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 第三行：Organization
        ttk.Label(api_group, text="Organization:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(api_group, textvariable=self.organization, width=30).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
    
    def create_projects_section(self, parent):
        """建立專案選擇區域"""
        # Projects 群組
        projects_group = ttk.LabelFrame(parent, text="Select Projects & Versions", padding="10")
        projects_group.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        projects_group.columnconfigure(0, weight=1)
        projects_group.rowconfigure(1, weight=1)
        
        # 工具列
        toolbar = ttk.Frame(projects_group)
        toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_projects).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Select All", command=self.select_all_versions).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Clear All", command=self.clear_all_versions).pack(side=tk.LEFT)
        
        # 專案樹狀檢視
        tree_frame = ttk.Frame(projects_group)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # 建立 Treeview
        columns = ("select", "project_version", "project_id", "version_id", "full_data")
        self.projects_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=8)
        
        # 設定欄位
        self.projects_tree.heading("#0", text="Project / Version")
        self.projects_tree.heading("select", text="Select")
        self.projects_tree.heading("project_version", text="Version")
        self.projects_tree.heading("project_id", text="Project ID")
        self.projects_tree.heading("version_id", text="Version ID")
        
        # 設定欄寬
        self.projects_tree.column("#0", width=200)
        self.projects_tree.column("select", width=60)
        self.projects_tree.column("project_version", width=120)
        self.projects_tree.column("project_id", width=150)
        self.projects_tree.column("version_id", width=150)
        self.projects_tree.column("full_data", width=0)  # 隱藏欄位
        
        # 滾動條
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.projects_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 綁定點擊事件
        self.projects_tree.bind("<Button-1>", self.on_tree_click)
        
        self.populate_projects_tree()
    
    def create_report_options_section(self, parent):
        """建立報告選項區域"""
        # Report Options 群組
        options_group = ttk.LabelFrame(parent, text="Report Options", padding="10")
        options_group.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        options_group.columnconfigure(1, weight=1)
        
        # 報告類型
        report_frame = ttk.Frame(options_group)
        report_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Checkbutton(report_frame, text="Standard Report", variable=self.standard_report, 
                       command=self.update_filename_preview).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Checkbutton(report_frame, text="Detailed Report", variable=self.detailed_report,
                       command=self.update_filename_preview).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Checkbutton(report_frame, text="Include Timestamp", variable=self.include_timestamp,
                       command=self.update_filename_preview).pack(side=tk.LEFT)
        
        # 輸出路徑
        ttk.Label(options_group, text="Output:").grid(row=1, column=0, sticky=tk.W, pady=2)
        output_frame = ttk.Frame(options_group)
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_path).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="📁", command=self.browse_output_folder, width=3).grid(row=0, column=1)
        
        # 檔名預覽
        ttk.Label(options_group, text="Preview:").grid(row=2, column=0, sticky=tk.W, pady=2)
        preview_label = ttk.Label(options_group, textvariable=self.filename_preview, foreground="blue")
        preview_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
    
    def create_progress_section(self, parent):
        """建立進度條區域"""
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_label = ttk.Label(parent, text="Ready")
        self.progress_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 10))
    
    def create_buttons_section(self, parent):
        """建立按鈕區域"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        self.generate_btn = ttk.Button(buttons_frame, text="Generate Reports", command=self.generate_reports, state="disabled")
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT)
    
    def create_log_section(self, parent):
        """建立日誌區域"""
        ttk.Label(parent, text="Log").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        log_frame = ttk.Frame(parent)
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=40, height=20, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 日誌按鈕
        log_buttons = ttk.Frame(parent)
        log_buttons.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(log_buttons, text="Clear", command=self.clear_log).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_buttons, text="Save", command=self.save_log).pack(side=tk.LEFT)
    
    def populate_projects_tree(self):
        """填充專案樹狀檢視"""
        for project_name, versions in self.projects_data.items():
            project_node = self.projects_tree.insert("", "end", text=f"📁 {project_name}", open=True)
            
            for version_data in versions:
                version_text = f"📄 {version_data['version']}"
                version_node = self.projects_tree.insert(
                    project_node, "end", 
                    text=version_text,
                    values=("☐", version_data['version'], version_data['project_id'][:12] + "...", version_data['version_id'][:12] + "...", str(version_data)),
                    tags=("version",)
                )
    
    def on_tree_click(self, event):
        """處理樹狀檢視點擊事件"""
        item = self.projects_tree.identify("item", event.x, event.y)
        column = self.projects_tree.identify("column", event.x, event.y)
        
        if item and column == "#1":  # Select 欄位
            if "version" in self.projects_tree.item(item, "tags"):
                # 切換選擇狀態
                current_values = list(self.projects_tree.item(item, "values"))
                if current_values[0] == "☐":
                    current_values[0] = "☑"
                else:
                    current_values[0] = "☐"
                self.projects_tree.item(item, values=current_values)
                self.update_filename_preview()
    
    def select_all_versions(self):
        """選擇所有版本"""
        for item in self.projects_tree.get_children():
            self._select_item_recursive(item, True)
        self.update_filename_preview()
    
    def clear_all_versions(self):
        """清除所有選擇"""
        for item in self.projects_tree.get_children():
            self._select_item_recursive(item, False)
        self.update_filename_preview()
    
    def _select_item_recursive(self, item, select):
        """遞迴選擇/取消選擇項目"""
        if "version" in self.projects_tree.item(item, "tags"):
            current_values = list(self.projects_tree.item(item, "values"))
            current_values[0] = "☑" if select else "☐"
            self.projects_tree.item(item, values=current_values)
        
        for child in self.projects_tree.get_children(item):
            self._select_item_recursive(child, select)
    
    def get_selected_versions(self):
        """取得選中的版本"""
        selected = []
        for item in self.projects_tree.get_children():
            selected.extend(self._get_selected_recursive(item))
        return selected
    
    def _get_selected_recursive(self, item):
        """遞迴取得選中的版本"""
        selected = []
        if "version" in self.projects_tree.item(item, "tags"):
            values = self.projects_tree.item(item, "values")
            if values[0] == "☑":
                # 從 values[4] 取得完整資料
                import ast
                full_data = ast.literal_eval(values[4])
                selected.append(full_data)
        
        for child in self.projects_tree.get_children(item):
            selected.extend(self._get_selected_recursive(child))
        
        return selected
    
    def load_default_config(self):
        """載入預設配置"""
        self.log_message("應用程式已啟動")
        self.log_message("請點擊 'Connect & Load Projects' 連接到 FiniteState API")
    
    def connect_api(self):
        """連接 API"""
        self.log_message("正在連接到 FiniteState API...")
        self.connect_btn.config(state="disabled")
        
        # 模擬連接過程
        def connect_thread():
            import time
            time.sleep(2)  # 模擬連接時間
            
            # 更新 UI（需要在主線程中執行）
            self.root.after(0, self._connection_success)
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def _connection_success(self):
        """連接成功回調"""
        self.connection_status.set("已連接")
        self.status_label.config(foreground="green")
        self.connect_btn.config(state="normal", text="Reconnect")
        self.generate_btn.config(state="normal")
        
        self.log_message("✅ API 連接成功")
        self.log_message("✅ 載入專案列表完成")
        total_versions = sum(len(versions) for versions in self.projects_data.values())
        self.log_message(f"找到 {len(self.projects_data)} 個專案，共 {total_versions} 個版本")
    
    def refresh_projects(self):
        """重新整理專案"""
        self.log_message("正在重新整理專案列表...")
        # 這裡可以重新載入專案資料
        self.log_message("✅ 專案列表已更新")
    
    def browse_output_folder(self):
        """瀏覽輸出資料夾"""
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)
            self.update_filename_preview()
    
    def update_filename_preview(self):
        """更新檔名預覽"""
        selected_count = len(self.get_selected_versions())
        
        if selected_count == 0:
            self.filename_preview.set("請選擇要生成報告的版本")
        elif selected_count == 1:
            # 單一版本
            version = self.get_selected_versions()[0]['version']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if self.include_timestamp.get() else ""
            
            reports = []
            if self.standard_report.get():
                reports.append(f"TMflow_{version}_Standard_{timestamp}.pdf" if timestamp else f"TMflow_{version}_Standard.pdf")
            if self.detailed_report.get():
                reports.append(f"TMflow_{version}_Detailed_{timestamp}.pdf" if timestamp else f"TMflow_{version}_Detailed.pdf")
            
            if reports:
                self.filename_preview.set(" | ".join(reports))
            else:
                self.filename_preview.set("請選擇報告類型")
        else:
            # 多個版本
            report_types = []
            if self.standard_report.get():
                report_types.append("Standard")
            if self.detailed_report.get():
                report_types.append("Detailed")
            
            if report_types:
                total_reports = selected_count * len(report_types)
                self.filename_preview.set(f"將生成 {total_reports} 個報告檔案 ({selected_count} 版本 × {len(report_types)} 類型)")
            else:
                self.filename_preview.set("請選擇報告類型")
    
    def generate_reports(self):
        """生成報告"""
        selected_versions = self.get_selected_versions()
        
        if not selected_versions:
            messagebox.showwarning("警告", "請至少選擇一個版本")
            return
        
        if not self.standard_report.get() and not self.detailed_report.get():
            messagebox.showwarning("警告", "請至少選擇一種報告類型")
            return
        
        self.log_message(f"開始生成報告...")
        self.log_message(f"選中版本數: {len(selected_versions)}")
        
        # 計算總報告數
        report_types = []
        if self.standard_report.get():
            report_types.append("Standard")
        if self.detailed_report.get():
            report_types.append("Detailed")
        
        total_reports = len(selected_versions) * len(report_types)
        self.log_message(f"將生成 {total_reports} 個報告")
        
        # 開始生成（在背景執行）
        self.generate_btn.config(state="disabled")
        threading.Thread(target=self._generate_reports_thread, 
                        args=(selected_versions, report_types), daemon=True).start()
    
    def _generate_reports_thread(self, selected_versions, report_types):
        """背景生成報告"""
        import time
        
        total_reports = len(selected_versions) * len(report_types)
        current_report = 0
        
        for version_data in selected_versions:
            version = version_data['version']
            version_id = version_data['version_id']
            
            for report_type in report_types:
                current_report += 1
                progress = (current_report / total_reports) * 100
                
                # 更新進度
                self.root.after(0, lambda p=progress, v=version, t=report_type: self._update_progress(p, f"生成 {v} {t} 報告..."))
                
                # 模擬報告生成
                time.sleep(2)
                
                # 記錄完成
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if self.include_timestamp.get() else ""
                filename = f"TMflow_{version}_{report_type}_{timestamp}.pdf" if timestamp else f"TMflow_{version}_{report_type}.pdf"
                self.root.after(0, lambda f=filename: self.log_message(f"✅ 已生成: {f}"))
        
        # 完成
        self.root.after(0, self._generation_complete)
    
    def _update_progress(self, progress, message):
        """更新進度條"""
        self.progress_var.set(progress)
        self.progress_label.config(text=message)
    
    def _generation_complete(self):
        """生成完成"""
        self.progress_var.set(100)
        self.progress_label.config(text="所有報告生成完成！")
        self.generate_btn.config(state="normal")
        self.log_message("🎉 所有報告生成完成！")
        messagebox.showinfo("完成", "所有報告已成功生成！")
    
    def log_message(self, message):
        """記錄訊息到日誌"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log_text.insert(tk.END, f"{timestamp} {message}\n")
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """清除日誌"""
        self.log_text.delete(1.0, tk.END)
    
    def save_log(self):
        """儲存日誌"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log_message(f"日誌已儲存到: {filename}")

def main():
    root = tk.Tk()
    app = TMflowReportGeneratorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()