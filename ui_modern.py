#!/usr/bin/env python3
"""
TMflow Security Report Generator - Modern Dark Theme UI
現代化深色主題的圖形化介面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import subprocess
import sys
from datetime import datetime
import json

class ModernTMflowReportGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_style()
        self.setup_variables()
        self.create_widgets()
        self.load_default_config()
        
        # 綁定關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """應用程式關閉時的處理"""
        if self.is_generating:
            if messagebox.askokcancel("確認關閉", "報告正在生成中，確定要關閉應用程式嗎？"):
                self.generation_cancelled = True
                # 儲存配置（包括選擇狀態）
                self.save_config_to_file()
                self.root.destroy()
        else:
            # 儲存配置（包括選擇狀態）
            self.save_config_to_file()
            self.root.destroy()
        
    def setup_window(self):
        """設定主視窗"""
        self.root.title("TMflow Security Report Generator v1.0.2.003")
        self.root.geometry("900x550")  # 減少寬度從 1000 到 900
        self.root.resizable(True, True)
        
        # 設定深色背景
        self.root.configure(bg='#2b2b2b')
        
    def setup_style(self):
        """設定深色主題樣式"""
        self.style = ttk.Style()
        
        # 設定深色主題
        self.style.theme_use('clam')
        
        # 配置顏色
        self.style.configure('Dark.TFrame', background='#2b2b2b')
        self.style.configure('Dark.TLabel', background='#2b2b2b', foreground='white')
        self.style.configure('Dark.TLabelframe', background='#2b2b2b', foreground='white', borderwidth=1, relief='solid')
        self.style.configure('Dark.TLabelframe.Label', background='#2b2b2b', foreground='white')
        self.style.configure('Dark.TEntry', fieldbackground='#404040', foreground='white', borderwidth=1)
        self.style.configure('Dark.TButton', background='#404040', foreground='white')
        self.style.configure('Dark.TCheckbutton', background='#2b2b2b', foreground='white', focuscolor='none')
        
        # 自訂 Checkbutton 樣式，使用 ✓ 符號
        self.style.map('Dark.TCheckbutton',
                      background=[('active', '#2b2b2b')],
                      foreground=[('active', 'white')])
        
        # 特殊按鈕樣式
        self.style.configure('Generate.TButton', background='#0078d4', foreground='white', font=('Arial', 10, 'bold'))
        self.style.map('Generate.TButton', background=[('active', '#106ebe')])
        
        # Treeview 深色樣式
        self.style.configure('Dark.Treeview', background='#404040', foreground='white', fieldbackground='#404040')
        self.style.configure('Dark.Treeview.Heading', background='#505050', foreground='white')
        self.style.map('Dark.Treeview', background=[('selected', '#0078d4')])
        
        # 進度條樣式
        self.style.configure('Dark.Horizontal.TProgressbar', background='#0078d4', troughcolor='#404040')
    
    def setup_variables(self):
        """設定變數"""
        self.api_token = tk.StringVar(value="svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq")
        self.subdomain = tk.StringVar(value="tm-robot")
        self.organization = tk.StringVar(value="Techman Robot")
        self.connection_status = tk.StringVar(value="Connected")
        self.output_path = tk.StringVar(value="reports")
        self.standard_report = tk.BooleanVar(value=True)  # 預設打勾
        self.detailed_report = tk.BooleanVar(value=True)  # 預設打勾
        self.filename_preview = tk.StringVar(value="TMflow_2.26.0.0_Standard_[時間戳]...")
        
        # 專案資料 - 預設為空，需要點擊 Refresh 載入
        self.projects_data = {}
        
        # 報告生成狀態
        self.is_generating = False
        self.generation_cancelled = False
    
    def create_widgets(self):
        """建立所有 UI 元件"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左側區域
        left_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # 右側區域 - 整個右側區域
        right_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 右上 - API Connection
        api_frame = ttk.Frame(right_frame, style='Dark.TFrame')
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 右下 - Log (延伸到底部)
        log_frame = ttk.Frame(right_frame, style='Dark.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立各區域
        self.create_projects_section(left_frame)
        self.create_api_connection_section(api_frame)
        self.create_log_section(log_frame)
        self.create_report_options_section(left_frame)
        self.create_progress_section(left_frame)
    
    def create_api_connection_section(self, parent):
        """建立 API 連接區域"""
        # API Connection 群組框 (縮小版)
        api_group = ttk.LabelFrame(parent, text="API Connection", style='Dark.TLabelframe', padding="10")
        api_group.pack(fill=tk.X)
        
        # 狀態指示器和重新連線按鈕 (第一行)
        status_frame = ttk.Frame(api_group, style='Dark.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 綠色圓點
        self.status_canvas = tk.Canvas(status_frame, width=12, height=12, bg='#2b2b2b', highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=(0, 5))
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#00ff00', outline='')
        
        ttk.Label(status_frame, text="Connected", style='Dark.TLabel', foreground='#00ff00').pack(side=tk.LEFT, padx=(0, 20))
        
        # 重新連線按鈕 - 往左靠
        self.reconnect_btn = ttk.Button(status_frame, text="Reconnect", style='Dark.TButton', command=self.reconnect_api)
        self.reconnect_btn.pack(side=tk.LEFT)
        
        # API 設定區域
        api_frame = ttk.Frame(api_group, style='Dark.TFrame')
        api_frame.pack(fill=tk.X)
        
        # 縮小的欄位寬度
        field_width = 25
        
        # API Token
        token_frame = ttk.Frame(api_frame, style='Dark.TFrame')
        token_frame.pack(fill=tk.X, pady=1)
        ttk.Label(token_frame, text="API Token:", style='Dark.TLabel', width=10).pack(side=tk.LEFT)
        ttk.Entry(token_frame, textvariable=self.api_token, show="*", width=field_width, style='Dark.TEntry').pack(side=tk.LEFT, padx=(5, 0))
        
        # Subdomain
        subdomain_frame = ttk.Frame(api_frame, style='Dark.TFrame')
        subdomain_frame.pack(fill=tk.X, pady=1)
        ttk.Label(subdomain_frame, text="Subdomain:", style='Dark.TLabel', width=10).pack(side=tk.LEFT)
        ttk.Entry(subdomain_frame, textvariable=self.subdomain, width=field_width, style='Dark.TEntry').pack(side=tk.LEFT, padx=(5, 0))
        
        # Organization
        org_frame = ttk.Frame(api_frame, style='Dark.TFrame')
        org_frame.pack(fill=tk.X, pady=1)
        ttk.Label(org_frame, text="Organization:", style='Dark.TLabel', width=10).pack(side=tk.LEFT)
        ttk.Entry(org_frame, textvariable=self.organization, width=field_width, style='Dark.TEntry').pack(side=tk.LEFT, padx=(5, 0))
    
    def create_projects_section(self, parent):
        """建立專案選擇區域"""
        # Projects 群組框 - 增加高度以顯示更多項目
        projects_group = ttk.LabelFrame(parent, text="Select Projects & Versions", style='Dark.TLabelframe', padding="10")
        projects_group.pack(fill=tk.BOTH, expand=True, pady=(0, 10))  # 改為 expand=True 讓它佔用更多空間
        
        # 工具列
        toolbar = ttk.Frame(projects_group, style='Dark.TFrame')
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar, text="🔄 Refresh", style='Dark.TButton', command=self.refresh_projects).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Select All", style='Dark.TButton', command=self.select_all_versions).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Clear All", style='Dark.TButton', command=self.clear_all_versions).pack(side=tk.LEFT)
        
        # 專案列表 - 增加高度
        tree_frame = ttk.Frame(projects_group, style='Dark.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立 Treeview - 增加高度
        columns = ("select", "version", "project_id", "version_id")
        self.projects_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=10, style='Dark.Treeview')
        
        # 設定欄位
        self.projects_tree.heading("#0", text="Project / Version")
        self.projects_tree.heading("select", text="Select")
        self.projects_tree.heading("version", text="Version")
        self.projects_tree.heading("project_id", text="Project ID")
        self.projects_tree.heading("version_id", text="Version ID")
        
        # 設定欄寬
        self.projects_tree.column("#0", width=150)
        self.projects_tree.column("select", width=60)
        self.projects_tree.column("version", width=100)
        self.projects_tree.column("project_id", width=120)
        self.projects_tree.column("version_id", width=120)
        
        # 滾動條
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 綁定點擊事件
        self.projects_tree.bind("<Button-1>", self.on_tree_click)
        
        self.populate_projects_tree()
    
    def create_report_options_section(self, parent):
        """建立報告選項區域"""
        # Report Options 群組框
        options_group = ttk.LabelFrame(parent, text="Report Options", style='Dark.TLabelframe', padding="10")
        options_group.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行：報告類型 + Generate Reports 按鈕
        top_frame = ttk.Frame(options_group, style='Dark.TFrame')
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 左側：報告類型選項
        report_frame = ttk.Frame(top_frame, style='Dark.TFrame')
        report_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 自訂 Checkbutton，使用 ✓ 符號
        self.standard_check = tk.Checkbutton(report_frame, text="Standard Report", variable=self.standard_report,
                                           bg='#2b2b2b', fg='white', selectcolor='#404040', activebackground='#2b2b2b',
                                           activeforeground='white', command=self.update_filename_preview)
        self.standard_check.pack(side=tk.LEFT, padx=(0, 20))
        
        self.detailed_check = tk.Checkbutton(report_frame, text="Detailed Report", variable=self.detailed_report,
                                           bg='#2b2b2b', fg='white', selectcolor='#404040', activebackground='#2b2b2b',
                                           activeforeground='white', command=self.update_filename_preview)
        self.detailed_check.pack(side=tk.LEFT)
        
        # 右側：Generate Reports 按鈕
        self.generate_btn = ttk.Button(top_frame, text="Generate Reports", style='Generate.TButton', command=self.generate_reports)
        self.generate_btn.pack(side=tk.RIGHT)
        
        # 第二行：輸出路徑
        output_frame = ttk.Frame(options_group, style='Dark.TFrame')
        output_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(output_frame, text="Output:", style='Dark.TLabel').pack(side=tk.LEFT)
        # 延伸 Output 輸入欄位
        ttk.Entry(output_frame, textvariable=self.output_path, style='Dark.TEntry').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
        ttk.Button(output_frame, text="📁", style='Dark.TButton', command=self.browse_output_folder, width=3).pack(side=tk.RIGHT)
        
        # 第三行：檔名預覽
        preview_frame = ttk.Frame(options_group, style='Dark.TFrame')
        preview_frame.pack(fill=tk.X)
        
        ttk.Label(preview_frame, text="Preview:", style='Dark.TLabel').pack(side=tk.LEFT)
        preview_label = ttk.Label(preview_frame, textvariable=self.filename_preview, style='Dark.TLabel', foreground='#87ceeb')
        preview_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def create_progress_section(self, parent):
        """建立進度條區域"""
        # Progress 群組框
        progress_group = ttk.LabelFrame(parent, text="Progress", style='Dark.TLabelframe', padding="10")
        progress_group.pack(fill=tk.X)
        
        # 進度條和百分比在同一行
        progress_frame = ttk.Frame(progress_group, style='Dark.TFrame')
        progress_frame.pack(fill=tk.X)
        
        # 進度條
        self.progress_var = tk.DoubleVar(value=0)  # 預設為 0%
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, 
                                          style='Dark.Horizontal.TProgressbar')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 百分比標籤在右側
        self.progress_label = ttk.Label(progress_frame, text="0%", style='Dark.TLabel', font=('Arial', 9))
        self.progress_label.pack(side=tk.RIGHT)
    
    def create_log_section(self, parent):
        """建立日誌區域"""
        # Log 群組框 (延伸到底部)
        log_group = ttk.LabelFrame(parent, text="Log", style='Dark.TLabelframe', padding="10")
        log_group.pack(fill=tk.BOTH, expand=True)
        
        # 日誌文字區域 (延伸到底部)
        self.log_text = scrolledtext.ScrolledText(log_group, wrap=tk.WORD, 
                                                 bg='#404040', fg='white', insertbackground='white')
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def populate_projects_tree(self):
        """填充專案樹狀檢視"""
        # 清空現有項目
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        # 如果沒有專案資料，顯示空清單
        if not self.projects_data:
            return
        
        for project_name, versions in self.projects_data.items():
            project_node = self.projects_tree.insert("", "end", text=f"📁 {project_name}", open=True)
            
            for version_data in versions:
                # 檢查選擇狀態
                is_selected = version_data['selected'].get()
                select_symbol = "☑" if is_selected else "☐"
                
                version_node = self.projects_tree.insert(
                    project_node, "end", 
                    text=f"📄 {project_name}",  # 顯示產品名稱
                    values=(select_symbol, version_data['version'], version_data['project_id'][:12] + "...", version_data['version_id'][:10] + "..."),
                    tags=("version",)
                )
    
    def on_tree_click(self, event):
        """處理樹狀檢視點擊事件"""
        item = self.projects_tree.identify("item", event.x, event.y)
        column = self.projects_tree.identify("column", event.x, event.y)
        
        if item and column == "#1":  # Select 欄位
            if "version" in self.projects_tree.item(item, "tags"):
                # 找到對應的版本資料
                version_info = self._find_version_by_tree_item(item)
                if version_info:
                    project_name, version_data = version_info
                    # 切換選擇狀態
                    current_state = version_data['selected'].get()
                    version_data['selected'].set(not current_state)
                    
                    # 更新樹狀檢視顯示
                    new_symbol = "☑" if not current_state else "☐"
                    current_values = list(self.projects_tree.item(item, "values"))
                    current_values[0] = new_symbol
                    self.projects_tree.item(item, values=current_values)
                    
                    self.update_filename_preview()
                    
                    # 自動保存選擇狀態
                    self.save_config_to_file()
    
    def _find_version_by_tree_item(self, tree_item):
        """根據樹狀檢視項目找到對應的版本資料"""
        try:
            values = self.projects_tree.item(tree_item, "values")
            if len(values) >= 4:
                version_name = values[1]
                version_id_short = values[3]
                
                # 在專案資料中尋找匹配的版本
                for project_name, versions in self.projects_data.items():
                    for version_data in versions:
                        if (version_data['version'] == version_name and 
                            version_data['version_id'].startswith(version_id_short.replace('...', ''))):
                            return project_name, version_data
        except:
            pass
        return None
    
    def select_all_versions(self):
        """選擇所有版本"""
        for project_name, versions in self.projects_data.items():
            for version_data in versions:
                version_data['selected'].set(True)
        
        # 重新填充樹狀檢視以反映變更
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        self.populate_projects_tree()
        self.update_filename_preview()
    
    def clear_all_versions(self):
        """清除所有選擇"""
        for project_name, versions in self.projects_data.items():
            for version_data in versions:
                version_data['selected'].set(False)
        
        # 重新填充樹狀檢視以反映變更
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        self.populate_projects_tree()
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
                selected.append({"version": values[1], "project_id": values[2], "version_id": values[3]})
        
        for child in self.projects_tree.get_children(item):
            selected.extend(self._get_selected_recursive(child))
        
        return selected
    
    def refresh_projects(self):
        """重新整理專案"""
        self.log_message("正在重新整理專案列表...")
        
        # 驗證 API 連接
        success, message = self.validate_api_connection()
        if not success:
            self.log_message(f"❌ 無法更新專案列表: {message}")
            messagebox.showerror("錯誤", f"無法更新專案列表:\n{message}")
            return
        
        # 在背景執行緒中獲取專案資料
        threading.Thread(target=self._fetch_projects_thread, daemon=True).start()
    
    def _fetch_projects_thread(self):
        """在背景執行緒中獲取專案資料"""
        try:
            # 獲取專案列表
            projects = self._fetch_projects_from_api()
            
            if projects:
                # 更新 UI（需要在主線程中執行）
                self.root.after(0, lambda: self._update_projects_data(projects))
            else:
                self.root.after(0, lambda: self.log_message("❌ 無法獲取專案資料"))
                
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ 獲取專案資料時發生錯誤: {e}"))
    
    def _fetch_projects_from_api(self):
        """從 API 獲取專案資料"""
        try:
            import requests
            import json
            
            # Finite State API 端點（正確的格式）
            base_url = f"https://{self.subdomain.get()}.finitestate.io/api"
            headers = {
                "X-Authorization": self.api_token.get(),
                "Content-Type": "application/json"
            }
            
            # 獲取專案列表
            projects_response = requests.get(f"{base_url}/public/v0/projects", headers=headers, timeout=30)
            if projects_response.status_code != 200:
                self.root.after(0, lambda: self.log_message(f"❌ API 請求失敗: {projects_response.status_code}"))
                return None
            
            projects_data = projects_response.json()
            
            # 處理回應格式（可能是列表或字典）
            if isinstance(projects_data, list):
                projects_list = projects_data
            else:
                projects_list = projects_data.get("items", [])
            
            projects = {}
            
            # 處理每個專案
            for project in projects_list:
                project_name = project.get('name', 'Unknown')
                project_id = project.get('id')
                
                if not project_id:
                    continue
                
                self.root.after(0, lambda p=project_name: self.log_message(f"正在載入專案: {p}"))
                
                # 獲取專案的版本列表
                versions_response = requests.get(
                    f"{base_url}/public/v0/projects/{project_id}/versions",
                    headers=headers,
                    params={"limit": 50, "sort": "-created"},  # 按創建時間降序排列
                    timeout=30
                )
                
                if versions_response.status_code == 200:
                    versions_data = versions_response.json()
                    
                    # 處理版本回應格式
                    if isinstance(versions_data, list):
                        versions_list = versions_data
                    else:
                        versions_list = versions_data.get("items", [])
                    
                    versions = []
                    
                    for version in versions_list:
                        # 版本名稱在 'version' 欄位中
                        version_name = version.get('version', version.get('name', 'Unknown'))
                        version_id = str(version.get('id', ''))
                        created_at = version.get('created', version.get('created_at', ''))
                        
                        if version_id:
                            versions.append({
                                "version": version_name,
                                "project_id": str(project_id),
                                "version_id": version_id,
                                "created": created_at,
                                "selected": tk.BooleanVar()
                            })
                    
                    # 按版本號降序排列（新版本在前）
                    def version_sort_key(v):
                        version_name = v["version"]
                        # 嘗試解析版本號進行數字排序
                        try:
                            # 處理類似 "3.12.1600.0" 的版本號
                            parts = version_name.replace('_', '.').split('.')
                            # 轉換為數字進行比較，如果無法轉換則使用 0
                            numeric_parts = []
                            for part in parts:
                                try:
                                    numeric_parts.append(int(part))
                                except ValueError:
                                    # 如果包含非數字字符，使用字符串排序
                                    return (0, version_name)
                            return (1, tuple(numeric_parts))
                        except:
                            # 如果解析失敗，按字符串排序
                            return (0, version_name)
                    
                    # 按版本號降序排列
                    versions.sort(key=version_sort_key, reverse=True)
                    
                    if versions:
                        projects[project_name] = versions
                        self.root.after(0, lambda p=project_name, c=len(versions): 
                                      self.log_message(f"✅ 載入專案 {p}: {c} 個版本"))
                else:
                    self.root.after(0, lambda p=project_name, s=versions_response.status_code: 
                                  self.log_message(f"❌ 無法載入 {p} 的版本: HTTP {s}"))
            
            return projects
            
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.log_message("❌ API 請求超時"))
            return None
        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: self.log_message(f"❌ API 請求錯誤: {e}"))
            return None
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ 處理 API 回應時發生錯誤: {e}"))
            return None
    
    def _update_projects_data(self, projects):
        """更新專案資料並重新填充樹狀檢視"""
        if projects:
            # 更新專案資料
            self.projects_data = projects
            
            # 應用保存的選擇狀態
            self.apply_saved_selections()
            
            # 清空現有的樹狀檢視
            for item in self.projects_tree.get_children():
                self.projects_tree.delete(item)
            
            # 重新填充樹狀檢視
            self.populate_projects_tree()
            
            total_versions = sum(len(versions) for versions in projects.values())
            self.log_message(f"✅ 專案列表已更新: {len(projects)} 個專案, {total_versions} 個版本")
            
            # 立即保存更新的專案資料到配置檔案
            self.save_config_to_file()
            self.log_message("✅ 專案資料已保存到配置檔案")
        else:
            self.log_message("❌ 無法更新專案列表")
    
    def browse_output_folder(self):
        """瀏覽輸出資料夾"""
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)
            self.update_filename_preview()
            self.log_message(f"輸出路徑已更新: {folder}")
    
    def update_filename_preview(self):
        """更新檔名預覽"""
        selected_count = len(self.get_selected_versions())
        
        if selected_count == 0:
            self.filename_preview.set("請選擇要生成報告的版本")
        elif selected_count == 1:
            version = self.get_selected_versions()[0]['version']
            timestamp = "[時間戳]"  # 總是包含時間戳
            
            reports = []
            if self.standard_report.get():
                reports.append(f"TMflow_{version}_Standard_{timestamp}...")
            if self.detailed_report.get():
                reports.append(f"TMflow_{version}_Detailed_{timestamp}...")
            
            if reports:
                self.filename_preview.set(" | ".join(reports))
            else:
                self.filename_preview.set("請選擇報告類型")
        else:
            report_types = []
            if self.standard_report.get():
                report_types.append("Standard")
            if self.detailed_report.get():
                report_types.append("Detailed")
            
            if report_types:
                total_reports = selected_count * len(report_types)
                self.filename_preview.set(f"將生成 {total_reports} 個報告檔案")
            else:
                self.filename_preview.set("請選擇報告類型")
    
    def generate_reports(self):
        """生成報告"""
        if self.is_generating:
            messagebox.showwarning("警告", "報告正在生成中，請稍候...")
            return
            
        selected_versions = self.get_selected_versions()
        
        if not selected_versions:
            messagebox.showwarning("警告", "請至少選擇一個版本")
            return
        
        if not self.standard_report.get() and not self.detailed_report.get():
            messagebox.showwarning("警告", "請至少選擇一種報告類型")
            return
        
        # 檢查 fs-reporter 是否存在
        if not os.path.exists("fs-reporter/main.py"):
            messagebox.showerror("錯誤", "找不到 fs-reporter/main.py\n請確保 fs-reporter 工具已正確安裝")
            return
        
        # 確保輸出目錄存在
        output_dir = self.output_path.get()
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("錯誤", f"無法建立輸出目錄: {e}")
            return
        
        # 重置進度條到 0%
        self._update_progress(0)
        
        self.log_message(f"開始生成報告...")
        self.log_message(f"選中版本數: {len(selected_versions)}")
        
        # 計算總報告數
        report_types = []
        if self.standard_report.get():
            report_types.append("standard")
        if self.detailed_report.get():
            report_types.append("detailed")
        
        total_reports = len(selected_versions) * len(report_types)
        self.log_message(f"將生成 {total_reports} 個報告檔案")
        
        # 開始生成
        self.is_generating = True
        self.generation_cancelled = False
        self.generate_btn.configure(state='disabled', text='生成中...')
        
        # 在背景執行緒中生成報告
        threading.Thread(target=self._generate_reports_thread, 
                        args=(selected_versions, report_types, output_dir), 
                        daemon=True).start()
    
    def _generate_reports_thread(self, selected_versions, report_types, output_dir):
        """在背景執行緒中生成報告"""
        try:
            total_reports = len(selected_versions) * len(report_types)
            completed_reports = 0
            successful_reports = []
            failed_reports = []
            
            for version_data in selected_versions:
                if self.generation_cancelled:
                    break
                    
                version = version_data['version']
                version_id = version_data['version_id']
                
                # 移除省略號
                if version_id.endswith('...'):
                    # 從原始資料中找到完整的 version_id
                    for project_name, versions in self.projects_data.items():
                        for v in versions:
                            if v['version'] == version and v['version_id'].startswith(version_id[:-3]):
                                version_id = v['version_id']
                                break
                
                self.root.after(0, lambda v=version: self.log_message(f"正在處理版本: {v}"))
                
                for report_type in report_types:
                    if self.generation_cancelled:
                        break
                        
                    report_suffix = "Standard" if report_type == "standard" else "Detailed"
                    self.root.after(0, lambda s=report_suffix: self.log_message(f"生成 {s} 報告..."))
                    
                    # 生成報告
                    success, output_path = self._generate_single_report(
                        version, version_id, report_type, output_dir
                    )
                    
                    completed_reports += 1
                    progress = int((completed_reports / total_reports) * 100)
                    
                    if success:
                        successful_reports.append(output_path)
                        self.root.after(0, lambda p=output_path: self.log_message(f"✅ 報告生成成功: {os.path.basename(p)}"))
                    else:
                        failed_reports.append(f"{version}_{report_suffix}")
                        self.root.after(0, lambda v=version, s=report_suffix: self.log_message(f"❌ 報告生成失敗: {v}_{s}"))
                    
                    # 更新進度
                    self.root.after(0, lambda p=progress: self._update_progress(p))
            
            # 生成完成
            self.root.after(0, lambda: self._generation_complete(successful_reports, failed_reports))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ 生成過程發生錯誤: {e}"))
            self.root.after(0, lambda: self._generation_complete([], []))
    
    def _generate_single_report(self, version, version_id, report_type, output_dir):
        """生成單個報告"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_suffix = "Standard" if report_type == "standard" else "Detailed"
            filename = f"TMflow_{version}_{report_suffix}_{timestamp}.pdf"
            output_path = os.path.join(output_dir, filename)
            
            # 構建命令
            cmd = [
                sys.executable, "fs-reporter/main.py",
                "-t", self.api_token.get(),
                "-s", self.subdomain.get(),
                "-pvi", version_id,
                "-n", self.organization.get(),
                "-o", output_path
            ]
            
            # 如果是詳細報告，添加 -d 參數
            if report_type == "detailed":
                cmd.insert(-2, "-d")
            
            # 執行命令
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5分鐘超時
            
            if result.returncode == 0:
                return True, output_path
            else:
                self.root.after(0, lambda: self.log_message(f"命令執行失敗: {result.stderr}"))
                return False, None
                
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self.log_message("報告生成超時"))
            return False, None
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"生成報告時發生錯誤: {e}"))
            return False, None
    
    def _update_progress(self, progress):
        """更新進度"""
        self.progress_var.set(progress)
        self.progress_label.configure(text=f"{progress}%")
    
    def _generation_complete(self, successful_reports=None, failed_reports=None):
        """生成完成"""
        self.is_generating = False
        self.generate_btn.configure(state='normal', text='Generate Reports')
        
        if successful_reports is None:
            successful_reports = []
        if failed_reports is None:
            failed_reports = []
        
        total_success = len(successful_reports)
        total_failed = len(failed_reports)
        
        if total_failed == 0:
            self.log_message("🎉 所有報告生成完成！")
            messagebox.showinfo("完成", f"成功生成 {total_success} 個報告！")
        else:
            self.log_message(f"⚠️ 生成完成：成功 {total_success} 個，失敗 {total_failed} 個")
            messagebox.showwarning("部分完成", f"成功生成 {total_success} 個報告\n失敗 {total_failed} 個報告")
        
        # 重置進度條
        if total_success > 0 or total_failed > 0:
            self._update_progress(100)
        else:
            self._update_progress(0)
    
    def reconnect_api(self):
        """重新連接 API"""
        self.log_message("正在驗證 API 連接...")
        self.reconnect_btn.configure(state='disabled')
        
        # 更新狀態為連接中
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ffff00', outline='')  # 黃色表示連接中
        
        # 儲存當前配置
        self.save_config_to_file()
        
        # 在背景執行緒中驗證連接
        def validate_thread():
            import time
            time.sleep(1)  # 模擬驗證時間
            
            # 驗證 API 連接
            success, message = self.validate_api_connection()
            
            # 更新 UI（需要在主線程中執行）
            if success:
                self.root.after(0, self._reconnection_success)
            else:
                self.root.after(0, lambda: self._reconnection_failed(message))
        
        threading.Thread(target=validate_thread, daemon=True).start()
    
    def _reconnection_success(self):
        """重新連接成功"""
        # 更新狀態為已連接
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#00ff00', outline='')  # 綠色表示已連接
        
        self.reconnect_btn.configure(state='normal')
        self.log_message("✅ API 連接驗證成功")
        self.log_message("✅ 配置已儲存")
    
    def _reconnection_failed(self, error_message):
        """重新連接失敗"""
        # 更新狀態為失敗
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ff0000', outline='')  # 紅色表示失敗
        
        self.reconnect_btn.configure(state='normal')
        self.log_message(f"❌ API 連接驗證失敗: {error_message}")
        messagebox.showerror("連接失敗", f"API 連接驗證失敗:\n{error_message}")
    
    def load_default_config(self):
        """載入預設配置"""
        # 嘗試從 config.txt 載入配置
        self.load_config_from_file()
        
        self.log_message("[15:21:19] 應用程式已啟動")
        self.log_message("[15:21:19] 配置已載入")
        self.log_message("[15:28:17] 連接到 FiniteState")
        
        # 檢查是否有保存的專案資料
        if hasattr(self, 'saved_projects_data') and self.saved_projects_data:
            self.log_message("[15:28:19] 載入保存的專案資料")
            # 在初始載入後應用保存的選擇狀態
            self.root.after(100, self.apply_saved_selections)
        else:
            self.log_message("[15:28:19] 專案清單為空")
            self.log_message("💡 點擊 'Refresh' 按鈕載入專案和版本資料")
            # 確保樹狀檢視為空
            self.root.after(100, self.populate_projects_tree)
    
    def load_config_from_file(self):
        """從配置檔案載入設定"""
        try:
            if os.path.exists("config.txt"):
                saved_selections = []
                saved_projects_data = None
                
                with open("config.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if "=" in line:
                                key, value = line.split("=", 1)
                                key = key.strip()
                                value = value.strip()
                                
                                if key == "API_TOKEN":
                                    self.api_token.set(value)
                                elif key == "SUBDOMAIN":
                                    self.subdomain.set(value)
                                elif key == "ORGANIZATION":
                                    self.organization.set(value)
                                elif key == "OUTPUT_PATH":
                                    self.output_path.set(value)
                                elif key == "STANDARD_REPORT":
                                    self.standard_report.set(value.lower() == 'true')
                                elif key == "DETAILED_REPORT":
                                    self.detailed_report.set(value.lower() == 'true')
                                elif key == "SELECTED_VERSIONS":
                                    try:
                                        import json
                                        saved_selections = json.loads(value)
                                    except:
                                        saved_selections = []
                                elif key == "PROJECTS_DATA":
                                    try:
                                        import json
                                        saved_projects_data = json.loads(value)
                                    except:
                                        saved_projects_data = None
                
                # 保存資料，稍後使用
                self.saved_selections = saved_selections
                self.saved_projects_data = saved_projects_data
                
                # 如果有保存的專案資料，載入它
                if saved_projects_data:
                    self.load_projects_data_from_saved(saved_projects_data)
                    self.log_message("✅ 配置檔案載入成功（包含專案資料）")
                else:
                    self.log_message("✅ 配置檔案載入成功（使用預設專案資料）")
            else:
                self.saved_selections = []
                self.saved_projects_data = None
                self.log_message("⚠️ 未找到 config.txt，使用預設配置")
        except Exception as e:
            self.saved_selections = []
            self.saved_projects_data = None
            self.log_message(f"❌ 載入配置檔案失敗: {e}")
    
    def load_projects_data_from_saved(self, saved_projects_data):
        """從保存的資料載入專案資料"""
        try:
            projects_data = {}
            for project_name, versions_list in saved_projects_data.items():
                projects_data[project_name] = []
                for version_info in versions_list:
                    # 重建 tkinter 變數
                    selected_var = tk.BooleanVar()
                    selected_var.set(version_info.get('selected', False))
                    
                    projects_data[project_name].append({
                        "version": version_info['version'],
                        "project_id": version_info['project_id'],
                        "version_id": version_info['version_id'],
                        "created": version_info.get('created', ''),
                        "selected": selected_var
                    })
            
            # 更新專案資料
            self.projects_data = projects_data
            
            # 重新填充樹狀檢視
            self.root.after(100, self.populate_projects_tree)
            self.root.after(200, self.update_filename_preview)
            
            total_versions = sum(len(versions) for versions in projects_data.values())
            self.log_message(f"✅ 已載入保存的專案資料: {len(projects_data)} 個專案, {total_versions} 個版本")
            
        except Exception as e:
            self.log_message(f"❌ 載入保存的專案資料失敗: {e}")
    
    def apply_saved_selections(self):
        """應用保存的選擇狀態"""
        if not hasattr(self, 'saved_selections') or not self.saved_selections:
            return
        
        try:
            for saved_selection in self.saved_selections:
                project_name = saved_selection.get('project')
                version_name = saved_selection.get('version')
                version_id = saved_selection.get('version_id')
                
                if project_name in self.projects_data:
                    for version_data in self.projects_data[project_name]:
                        if (version_data['version'] == version_name and 
                            version_data['version_id'] == version_id):
                            version_data['selected'].set(True)
                            break
            
            # 重新填充樹狀檢視以反映選擇狀態
            self.populate_projects_tree()
            self.update_filename_preview()
            
            selected_count = len([s for s in self.saved_selections])
            if selected_count > 0:
                self.log_message(f"✅ 已恢復 {selected_count} 個版本的選擇狀態")
                
        except Exception as e:
            self.log_message(f"❌ 應用保存的選擇狀態失敗: {e}")
    
    def save_config_to_file(self):
        """儲存設定到配置檔案"""
        try:
            # 獲取專案資料用於保存
            projects_data_for_save = self.get_projects_data_for_save()
            selected_versions_for_save = self.get_selected_versions_for_save()
            
            config_data = {
                "API_TOKEN": self.api_token.get(),
                "SUBDOMAIN": self.subdomain.get(),
                "ORGANIZATION": self.organization.get(),
                "OUTPUT_PATH": self.output_path.get(),
                "STANDARD_REPORT": self.standard_report.get(),
                "DETAILED_REPORT": self.detailed_report.get(),
                "SELECTED_VERSIONS": selected_versions_for_save,
                "PROJECTS_DATA": projects_data_for_save
            }
            
            with open("config.txt", "w", encoding="utf-8") as f:
                f.write("# TMflow Security Report Generator 配置檔案\n")
                f.write("# 請勿將此檔案提交到 Git\n\n")
                for key, value in config_data.items():
                    if key in ["SELECTED_VERSIONS", "PROJECTS_DATA"]:
                        # 將複雜資料保存為 JSON 格式
                        import json
                        f.write(f"{key}={json.dumps(value, ensure_ascii=False)}\n")
                    else:
                        f.write(f"{key}={value}\n")
            
            # 記錄保存的資料統計
            total_projects = len(projects_data_for_save)
            total_versions = sum(len(versions) for versions in projects_data_for_save.values())
            selected_count = len(selected_versions_for_save)
            
            self.log_message(f"✅ 配置已儲存: {total_projects} 專案, {total_versions} 版本, {selected_count} 選中")
        except Exception as e:
            self.log_message(f"❌ 儲存配置檔案失敗: {e}")
    
    def get_projects_data_for_save(self):
        """獲取專案資料用於保存（不包含 tkinter 變數）"""
        projects_data = {}
        for project_name, versions in self.projects_data.items():
            projects_data[project_name] = []
            for version_data in versions:
                projects_data[project_name].append({
                    "version": version_data['version'],
                    "project_id": version_data['project_id'],
                    "version_id": version_data['version_id'],
                    "created": version_data.get('created', ''),
                    "selected": version_data['selected'].get()
                })
        return projects_data
    
    def get_selected_versions_for_save(self):
        """獲取選中的版本用於保存"""
        selected = []
        for project_name, versions in self.projects_data.items():
            for version_data in versions:
                if version_data['selected'].get():
                    selected.append({
                        "project": project_name,
                        "version": version_data['version'],
                        "version_id": version_data['version_id']
                    })
        return selected
    
    def validate_api_connection(self):
        """驗證 API 連接"""
        token = self.api_token.get().strip()
        subdomain = self.subdomain.get().strip()
        
        if not token:
            return False, "API Token 不能為空"
        
        if not subdomain:
            return False, "Subdomain 不能為空"
        
        try:
            import requests
            
            # 測試 API 連接（使用正確的 Finite State API 格式）
            base_url = f"https://{subdomain}.finitestate.io/api"
            headers = {
                "X-Authorization": token,
                "Content-Type": "application/json"
            }
            
            # 簡單的 API 測試請求
            response = requests.get(f"{base_url}/public/v0/projects", headers=headers, timeout=10)
            
            if response.status_code == 200:
                return True, "連接成功"
            elif response.status_code == 401:
                return False, "API Token 無效或已過期"
            elif response.status_code == 403:
                return False, "權限不足，請檢查 API Token 權限"
            elif response.status_code == 404:
                return False, "API 端點不存在，請檢查 Subdomain"
            else:
                return False, f"API 回應錯誤: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "連接超時，請檢查網路連接"
        except requests.exceptions.ConnectionError:
            return False, "無法連接到伺服器，請檢查網路連接和 Subdomain"
        except ImportError:
            return False, "缺少 requests 模組，請執行: pip install requests"
        except Exception as e:
            return False, f"連接測試失敗: {e}"
    
    def log_message(self, message):
        """記錄訊息到日誌"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = ModernTMflowReportGeneratorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()