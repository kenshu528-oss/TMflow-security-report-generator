#!/usr/bin/env python3
"""
TMflow Security Report Generator - 模組化版本 v1.0.2.048
UI 佈局比例修正版 (使用 PanedWindow)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import subprocess
import sys
from datetime import datetime
import json
import platform

class APIManager:
    """API 管理模組 - 負責所有 API 相關操作"""
    
    def __init__(self, api_token="", subdomain="tm-robot"):
        self.api_token = api_token
        self.subdomain = subdomain
        self.base_url = f"https://{subdomain}.finitestate.io/api"
        self.headers = {
            "X-Authorization": api_token,
            "Content-Type": "application/json"
        }
    
    def update_credentials(self, api_token, subdomain):
        """更新 API 憑證"""
        self.api_token = api_token
        self.subdomain = subdomain
        self.base_url = f"https://{subdomain}.finitestate.io/api"
        self.headers["X-Authorization"] = api_token
    
    def test_connection(self):
        """測試 API 連接"""
        if not self.api_token:
            return False, "API Token 不能為空"
        
        if not self.subdomain:
            return False, "Subdomain 不能為空"
        
        try:
            import requests
            
            response = requests.get(f"{self.base_url}/public/v0/projects", 
                                  headers=self.headers, timeout=10)
            
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
                
        except Exception as e:
            return False, f"連接測試失敗: {e}"
    
    def fetch_projects(self):
        """獲取專案列表"""
        try:
            import requests
            
            # 獲取專案列表
            projects_response = requests.get(f"{self.base_url}/public/v0/projects", 
                                           headers=self.headers, timeout=30)
            
            if projects_response.status_code != 200:
                return None, f"API 請求失敗: {projects_response.status_code}"
            
            projects_data = projects_response.json()
            
            # 處理回應格式
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
                
                # 獲取專案的版本列表
                versions_response = requests.get(
                    f"{self.base_url}/public/v0/projects/{project_id}/versions",
                    headers=self.headers,
                    params={"limit": 50, "sort": "-created"},
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
                        version_name = version.get('version', version.get('name', 'Unknown'))
                        version_id = str(version.get('id', ''))
                        created_at = version.get('created', version.get('created_at', ''))
                        
                        if version_id:
                            versions.append({
                                "version": version_name,
                                "project_id": str(project_id),
                                "version_id": version_id,
                                "created": created_at
                            })
                    
                    # 按版本號降序排列
                    def version_sort_key(v):
                        version_name = v["version"]
                        try:
                            parts = version_name.replace('_', '.').split('.')
                            numeric_parts = []
                            for part in parts:
                                try:
                                    numeric_parts.append(int(part))
                                except ValueError:
                                    return (0, version_name)
                            return (1, tuple(numeric_parts))
                        except:
                            return (0, version_name)
                    
                    versions.sort(key=version_sort_key, reverse=True)
                    
                    if versions:
                        projects[project_name] = versions
            
            return projects, "成功"
            
        except Exception as e:
            return None, f"獲取專案資料時發生錯誤: {e}"

class ReportGenerator:
    """報告生成模組 - 負責所有報告生成操作"""
    
    def __init__(self, api_token="", subdomain="tm-robot", organization="Techman Robot"):
        self.api_token = api_token
        self.subdomain = subdomain
        self.organization = organization
    
    def update_config(self, api_token, subdomain, organization):
        """更新配置"""
        self.api_token = api_token
        self.subdomain = subdomain
        self.organization = organization
    
    def generate_single_report(self, version, version_id, report_type, output_dir):
        """生成單個報告 - 激進重構：完全直接整合架構"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_suffix = "Standard" if report_type == "standard" else "Detailed"
            filename = f"TMflow_{version}_{report_suffix}_{timestamp}.pdf"
            output_path = os.path.join(output_dir, filename)
            
            # 激進方案：完全直接整合 fs-reporter 核心功能
            return self._direct_integration_only(version_id, report_type, output_path)
            
        except Exception as e:
            return False, f"執行錯誤: {e}"
    
    def _direct_integration_only(self, version_id, report_type, output_path):
        """激進重構：只使用直接整合，徹底解決彈出視窗問題"""
        try:
            # 1. 動態添加 fs-reporter 到 Python 路徑
            import sys
            import os
            
            fs_reporter_path = os.path.join(os.getcwd(), "fs-reporter", "src")
            if fs_reporter_path not in sys.path:
                sys.path.insert(0, fs_reporter_path)
            
            # 2. 先驗證版本 ID 是否有效
            if not self._validate_version_id(version_id):
                return False, f"版本 ID {version_id} 無效或已過期"
            
            # 3. 直接導入和調用 fs-reporter 核心功能
            from finite_state_reporter.core.reporter import main
            
            # 4. 設定參數
            detailed_findings = (report_type == "detailed")
            
            # 5. 直接調用 main 函數，完全避免 subprocess
            main(
                token=self.api_token,
                subdomain=self.subdomain,
                project_version_id=version_id,
                output_filename=output_path,
                detailed_findings=detailed_findings,
                all_severities=False,
                max_detailed_findings=100,
                organization_name=self.organization
            )
            
            # 6. 檢查檔案是否成功生成
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                return True, f"{output_path} ({file_size} bytes)"
            else:
                return False, "報告檔案未生成"
                
        except ImportError as e:
            return False, f"無法導入 fs-reporter 模組: {e}"
        except Exception as e:
            return False, f"直接整合執行失敗: {e}"
    
    def _validate_version_id(self, version_id):
        """驗證版本 ID 是否有效"""
        try:
            import requests
            
            # 使用 API 驗證版本 ID
            response = requests.get(
                f"https://{self.subdomain}.finitestate.io/api/public/v0/versions/{version_id}",
                headers={"X-Authorization": self.api_token},
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            # 如果驗證失敗，記錄錯誤但不阻止執行
            print(f"版本 ID 驗證失敗: {e}")
            return True  # 預設為有效，讓後續流程處理錯誤

class ConfigManager:
    """配置管理模組 - 負責配置檔案的讀寫"""
    
    def __init__(self, config_file="config.txt"):
        self.config_file = config_file
    
    def load_config(self):
        """載入配置檔案"""
        config = {
            "API_TOKEN": "svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq",
            "SUBDOMAIN": "tm-robot",
            "ORGANIZATION": "Techman Robot",
            "OUTPUT_PATH": "reports",
            "STANDARD_REPORT": True,
            "DETAILED_REPORT": True,
            "SELECTED_VERSIONS": [],
            "PROJECTS_DATA": {}
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if "=" in line:
                                key, value = line.split("=", 1)
                                key = key.strip()
                                value = value.strip()
                                
                                if key in ["SELECTED_VERSIONS", "PROJECTS_DATA"]:
                                    try:
                                        config[key] = json.loads(value)
                                    except:
                                        config[key] = [] if key == "SELECTED_VERSIONS" else {}
                                elif key in ["STANDARD_REPORT", "DETAILED_REPORT"]:
                                    config[key] = value.lower() == 'true'
                                else:
                                    config[key] = value
        except Exception as e:
            print(f"載入配置檔案失敗: {e}")
        
        return config
    
    def save_config(self, config):
        """儲存配置檔案"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                f.write("# TMflow Security Report Generator 配置檔案\n")
                f.write("# 請勿將此檔案提交到 Git\n\n")
                
                for key, value in config.items():
                    if key in ["SELECTED_VERSIONS", "PROJECTS_DATA"]:
                        f.write(f"{key}={json.dumps(value, ensure_ascii=False)}\n")
                    else:
                        f.write(f"{key}={value}\n")
            return True
        except Exception as e:
            print(f"儲存配置檔案失敗: {e}")
            return False

class ModularTMflowReportGeneratorUI:
    """主 UI 類別 - 使用模組化架構"""
    
    def __init__(self, root):
        self.root = root
        
        # 初始化模組
        self.config_manager = ConfigManager()
        self.api_manager = APIManager()
        self.report_generator = ReportGenerator()
        
        # 載入配置
        self.config = self.config_manager.load_config()
        
        # 更新模組配置
        self.api_manager.update_credentials(
            self.config["API_TOKEN"], 
            self.config["SUBDOMAIN"]
        )
        self.report_generator.update_config(
            self.config["API_TOKEN"],
            self.config["SUBDOMAIN"], 
            self.config["ORGANIZATION"]
        )
        
        # 設定 UI
        self.setup_window()
        self.setup_style()
        self.setup_variables()
        self.create_widgets()
        self.load_initial_data()
        
        # 綁定關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def auto_connect_api(self):
        """自動連線 API"""
        if self.api_token.get() and self.subdomain.get():
            # 延遲 500ms 後自動連線，讓 UI 先完成初始化
            self.root.after(500, self._auto_test_connection)
    
    def _auto_test_connection(self):
        """自動測試連接（不彈出錯誤對話框）"""
        self.log_message("正在測試 API 連接...")
        
        # 更新狀態為測試中
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ffff00', outline='')
        
        # 更新 API 管理器的憑證
        self.api_manager.update_credentials(
            self.api_token.get(), 
            self.subdomain.get()
        )
        
        # 在背景執行緒中測試連接（自動連線，不設定手動標記）
        threading.Thread(target=self._test_connection_thread, daemon=True).start()
    
    def setup_window(self):
        """設定主視窗"""
        self.root.title("TMflow Security Report Generator v1.0.2.048")
        self.root.geometry("900x550")
        self.root.resizable(True, True)
        self.root.configure(bg='#2b2b2b')
    
    def setup_style(self):
        """設定深色主題樣式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 深色主題配色
        self.style.configure('Dark.TFrame', background='#2b2b2b')
        self.style.configure('Dark.TLabel', background='#2b2b2b', foreground='white')
        self.style.configure('Dark.TLabelframe', background='#2b2b2b', foreground='white', borderwidth=1, relief='solid')
        self.style.configure('Dark.TLabelframe.Label', background='#2b2b2b', foreground='white')
        self.style.configure('Dark.TEntry', fieldbackground='#404040', foreground='white', borderwidth=1)
        self.style.configure('Dark.TButton', background='#404040', foreground='white')
        self.style.configure('Generate.TButton', background='#0078d4', foreground='white', font=('Arial', 10, 'bold'))
        self.style.configure('Dark.Treeview', background='#404040', foreground='white', fieldbackground='#404040')
        self.style.configure('Dark.Treeview.Heading', background='#505050', foreground='white')
        self.style.configure('Dark.Horizontal.TProgressbar', background='#0078d4', troughcolor='#404040')
    
    def setup_variables(self):
        """設定變數"""
        self.api_token = tk.StringVar(value=self.config["API_TOKEN"])
        self.subdomain = tk.StringVar(value=self.config["SUBDOMAIN"])
        self.organization = tk.StringVar(value=self.config["ORGANIZATION"])
        self.output_path = tk.StringVar(value=self.config["OUTPUT_PATH"])
        self.standard_report = tk.BooleanVar(value=self.config["STANDARD_REPORT"])
        self.detailed_report = tk.BooleanVar(value=self.config["DETAILED_REPORT"])
        
        # 專案資料
        self.projects_data = {}
        self.selected_versions = set()
        
        # 狀態變數
        self.is_generating = False
        self.generation_cancelled = False
    
    def create_widgets(self):
        """建立所有 UI 元件"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 使用 PanedWindow 來精確控制左右比例
        self.paned = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, 
                                    bg='#2b2b2b', sashwidth=5, 
                                    sashrelief=tk.FLAT, bd=0,
                                    showhandle=False)  # 隱藏拖動手柄
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # 左側區域
        left_frame = ttk.Frame(self.paned, style='Dark.TFrame')
        self.paned.add(left_frame, stretch='always')
        
        # 右側區域
        right_frame = ttk.Frame(self.paned, style='Dark.TFrame')
        self.paned.add(right_frame, stretch='always')
        
        # 禁用 PanedWindow 的手動拖動
        self.paned.bind('<Button-1>', lambda e: 'break')
        self.paned.bind('<B1-Motion>', lambda e: 'break')
        
        # 綁定視窗大小變化事件，動態調整分隔位置
        self.resize_timer = None
        self.root.bind('<Configure>', self.on_window_resize)
        
        # 建立各區域
        self.create_projects_section(left_frame)
        self.create_report_options_section(left_frame)
        self.create_progress_section(left_frame)
        self.create_api_section(right_frame)
        self.create_log_section(right_frame)
    
    def create_projects_section(self, parent):
        """建立專案選擇區域"""
        projects_group = ttk.LabelFrame(parent, text="📋 Select Projects & Versions", 
                                      style='Dark.TLabelframe', padding="10")
        projects_group.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 工具列
        toolbar = ttk.Frame(projects_group, style='Dark.TFrame')
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar, text="🔄 Refresh", style='Dark.TButton', 
                  command=self.refresh_projects).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Select All", style='Dark.TButton', 
                  command=self.select_all_versions).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Clear All", style='Dark.TButton', 
                  command=self.clear_all_versions).pack(side=tk.LEFT)
        
        # 專案列表
        tree_frame = ttk.Frame(projects_group, style='Dark.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("select", "version", "project_id", "version_id")
        self.projects_tree = ttk.Treeview(tree_frame, columns=columns, 
                                        show="tree headings", height=10, 
                                        style='Dark.Treeview')
        
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
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", 
                                  command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 綁定點擊事件
        self.projects_tree.bind("<Button-1>", self.on_tree_click)
    
    def create_report_options_section(self, parent):
        """建立報告選項區域"""
        options_group = ttk.LabelFrame(parent, text="⚙️ Report Options", 
                                     style='Dark.TLabelframe', padding="10")
        options_group.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行：報告類型 + Generate Reports 按鈕
        top_frame = ttk.Frame(options_group, style='Dark.TFrame')
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 左側：報告類型選項
        report_frame = ttk.Frame(top_frame, style='Dark.TFrame')
        report_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.standard_check = tk.Checkbutton(report_frame, text="Standard Report", 
                                           variable=self.standard_report,
                                           bg='#2b2b2b', fg='white', selectcolor='#404040')
        self.standard_check.pack(side=tk.LEFT, padx=(0, 20))
        
        self.detailed_check = tk.Checkbutton(report_frame, text="Detailed Report", 
                                           variable=self.detailed_report,
                                           bg='#2b2b2b', fg='white', selectcolor='#404040')
        self.detailed_check.pack(side=tk.LEFT)
        
        # 右側：Generate Reports 按鈕
        self.generate_btn = ttk.Button(top_frame, text="Generate Reports", 
                                     style='Generate.TButton', 
                                     command=self.generate_reports)
        self.generate_btn.pack(side=tk.RIGHT)
        
        # 第二行：輸出路徑
        output_frame = ttk.Frame(options_group, style='Dark.TFrame')
        output_frame.pack(fill=tk.X)
        
        ttk.Label(output_frame, text="Output:", style='Dark.TLabel').pack(side=tk.LEFT)
        ttk.Entry(output_frame, textvariable=self.output_path, 
                 style='Dark.TEntry').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
        ttk.Button(output_frame, text="📁", style='Dark.TButton', 
                  command=self.browse_output_folder, width=3).pack(side=tk.RIGHT)
    
    def create_progress_section(self, parent):
        """建立進度條區域"""
        progress_group = ttk.LabelFrame(parent, text="📊 Progress", 
                                      style='Dark.TLabelframe', padding="10")
        progress_group.pack(fill=tk.X)
        
        progress_frame = ttk.Frame(progress_group, style='Dark.TFrame')
        progress_frame.pack(fill=tk.X)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, style='Dark.Horizontal.TProgressbar')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="0%", 
                                      style='Dark.TLabel', font=('Arial', 9))
        self.progress_label.pack(side=tk.RIGHT)
    
    def create_api_section(self, parent):
        """建立 API 連接區域"""
        api_frame = ttk.Frame(parent, style='Dark.TFrame')
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        api_group = ttk.LabelFrame(api_frame, text="🔗 API Connection", 
                                 style='Dark.TLabelframe', padding="10")
        api_group.pack(fill=tk.X)
        
        # 狀態指示器
        status_frame = ttk.Frame(api_group, style='Dark.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.status_canvas = tk.Canvas(status_frame, width=12, height=12, 
                                     bg='#2b2b2b', highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=(0, 5))
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ff0000', outline='')
        
        self.status_label = ttk.Label(status_frame, text="Disconnected", style='Dark.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.test_btn = ttk.Button(status_frame, text="Reconnect", 
                                 style='Dark.TButton', command=self.test_api_connection)
        self.test_btn.pack(side=tk.LEFT)
        
        # API 設定
        api_config_frame = ttk.Frame(api_group, style='Dark.TFrame')
        api_config_frame.pack(fill=tk.X)
        
        field_width = 25
        
        # API Token
        token_frame = ttk.Frame(api_config_frame, style='Dark.TFrame')
        token_frame.pack(fill=tk.X, pady=1)
        ttk.Label(token_frame, text="API Token:", style='Dark.TLabel', width=10).pack(side=tk.LEFT)
        ttk.Entry(token_frame, textvariable=self.api_token, show="*", 
                 width=field_width, style='Dark.TEntry').pack(side=tk.LEFT, padx=(5, 0))
        
        # Subdomain
        subdomain_frame = ttk.Frame(api_config_frame, style='Dark.TFrame')
        subdomain_frame.pack(fill=tk.X, pady=1)
        ttk.Label(subdomain_frame, text="Subdomain:", style='Dark.TLabel', width=10).pack(side=tk.LEFT)
        ttk.Entry(subdomain_frame, textvariable=self.subdomain, 
                 width=field_width, style='Dark.TEntry').pack(side=tk.LEFT, padx=(5, 0))
        
        # Organization
        org_frame = ttk.Frame(api_config_frame, style='Dark.TFrame')
        org_frame.pack(fill=tk.X, pady=1)
        ttk.Label(org_frame, text="Organization:", style='Dark.TLabel', width=10).pack(side=tk.LEFT)
        ttk.Entry(org_frame, textvariable=self.organization, 
                 width=field_width, style='Dark.TEntry').pack(side=tk.LEFT, padx=(5, 0))
    
    def create_log_section(self, parent):
        """建立日誌區域"""
        log_frame = ttk.Frame(parent, style='Dark.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_group = ttk.LabelFrame(log_frame, text="📝 Log", 
                                 style='Dark.TLabelframe', padding="10")
        log_group.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_group, wrap=tk.WORD, 
                                                bg='#404040', fg='white', 
                                                insertbackground='white')
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def on_window_resize(self, event):
        """視窗大小變化時，動態調整 PanedWindow 分隔位置以維持 60:40 比例"""
        # 只處理主視窗的 Configure 事件
        if event.widget == self.root:
            # 取消之前的計時器
            if self.resize_timer:
                self.root.after_cancel(self.resize_timer)
            # 延遲 100ms 執行，避免在調整過程中頻繁觸發
            self.resize_timer = self.root.after(100, self.adjust_paned_position)
    
    def adjust_paned_position(self):
        """調整 PanedWindow 分隔位置為 60:40"""
        try:
            # 獲取 PanedWindow 的實際寬度
            paned_width = self.paned.winfo_width()
            if paned_width > 1:  # 確保已經渲染
                # 計算 60% 的位置
                sash_position = int(paned_width * 0.6)
                self.paned.sash_place(0, sash_position, 0)
        except:
            pass  # 忽略任何錯誤
    
    def load_initial_data(self):
        """載入初始資料 - v1.0.2.042 可分享版本"""
        self.log_message("TMflow Security Report Generator v1.0.2.046")
        
        # 優先載入保存的專案資料（保持原有邏輯）
        if self.config["PROJECTS_DATA"]:
            self.load_projects_from_config()
        else:
            # v1.0.2.042 可分享版本：清空預設專案資料
            self.load_known_projects_data()
        
        # 自動連線 API
        self.auto_connect_api()
    
    def load_known_projects_data(self):
        """載入已知專案資料 - v1.0.2.042 清空版本供分享使用"""
        # v1.0.2.042: 清空預設專案資料，提供乾淨版本給同事使用
        known_projects_data = {}
        
        # 清空專案資料
        self.projects_data = {}
        self.populate_projects_tree()
        
        self.log_message("預設專案清單已清空，請點擊 'Refresh' 載入專案資料")
    
    def load_projects_from_config(self):
        """從配置載入專案資料 - 保持原始邏輯"""
        try:
            # 清空現有資料
            self.projects_data = {}
            self.selected_versions = set()
            
            # 載入專案資料
            for project_name, versions_list in self.config["PROJECTS_DATA"].items():
                self.projects_data[project_name] = []
                for version_info in versions_list:
                    self.projects_data[project_name].append({
                        "version": version_info['version'],
                        "project_id": version_info['project_id'],
                        "version_id": version_info['version_id'],
                        "created": version_info.get('created', '')
                    })
            
            # 載入選擇狀態
            for selection in self.config["SELECTED_VERSIONS"]:
                version_id = selection.get('version_id')
                if version_id:
                    self.selected_versions.add(version_id)
            
            # 填充樹狀檢視
            self.populate_projects_tree()
            
        except Exception as e:
            self.log_message(f"載入專案資料失敗: {e}")
            # 如果載入失敗，使用已知專案資料作為備用
            self.log_message("使用已知專案資料作為備用")
            self.load_known_projects_data()
    
    def populate_projects_tree(self):
        """填充專案樹狀檢視"""
        # 清空現有項目
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        if not self.projects_data:
            return
        
        for project_name, versions in self.projects_data.items():
            project_node = self.projects_tree.insert("", "end", 
                                                    text=f"📁 {project_name}", open=True)
            
            for version_data in versions:
                is_selected = version_data['version_id'] in self.selected_versions
                select_symbol = "☑" if is_selected else "☐"
                
                version_node = self.projects_tree.insert(
                    project_node, "end", 
                    text=f"📄 {project_name}",
                    values=(select_symbol, version_data['version'], 
                           version_data['project_id'][:12] + "...", 
                           version_data['version_id'][:10] + "..."),
                    tags=("version",)
                )
    
    def on_tree_click(self, event):
        """處理樹狀檢視點擊事件"""
        item = self.projects_tree.identify("item", event.x, event.y)
        column = self.projects_tree.identify("column", event.x, event.y)
        
        if item and column == "#1":  # Select 欄位
            if "version" in self.projects_tree.item(item, "tags"):
                version_info = self._find_version_by_tree_item(item)
                if version_info:
                    version_id = version_info['version_id']
                    
                    # 切換選擇狀態
                    if version_id in self.selected_versions:
                        self.selected_versions.remove(version_id)
                        new_symbol = "☐"
                    else:
                        self.selected_versions.add(version_id)
                        new_symbol = "☑"
                    
                    # 更新樹狀檢視顯示
                    current_values = list(self.projects_tree.item(item, "values"))
                    current_values[0] = new_symbol
                    self.projects_tree.item(item, values=current_values)
                    
                    # 自動保存
                    self.save_config()
    
    def _find_version_by_tree_item(self, tree_item):
        """根據樹狀檢視項目找到對應的版本資料"""
        try:
            values = self.projects_tree.item(tree_item, "values")
            if len(values) >= 4:
                version_name = values[1]
                version_id_short = values[3].replace('...', '')
                
                for project_name, versions in self.projects_data.items():
                    for version_data in versions:
                        if (version_data['version'] == version_name and 
                            version_data['version_id'].startswith(version_id_short)):
                            return version_data
        except:
            pass
        return None
    
    def select_all_versions(self):
        """選擇所有版本"""
        for project_name, versions in self.projects_data.items():
            for version_data in versions:
                self.selected_versions.add(version_data['version_id'])
        
        self.populate_projects_tree()
        self.save_config()
        self.log_message(f"已選擇所有版本 ({len(self.selected_versions)} 個)")
    
    def clear_all_versions(self):
        """清除所有選擇"""
        self.selected_versions.clear()
        self.populate_projects_tree()
        self.save_config()
        self.log_message("已清除所有選擇")
    
    def refresh_projects(self):
        """重新整理專案"""
        self.log_message("正在重新整理專案列表...")
        
        # 更新 API 管理器的憑證
        self.api_manager.update_credentials(
            self.api_token.get(), 
            self.subdomain.get()
        )
        
        # 在背景執行緒中獲取專案資料
        threading.Thread(target=self._fetch_projects_thread, daemon=True).start()
    
    def _fetch_projects_thread(self):
        """在背景執行緒中獲取專案資料"""
        try:
            projects, message = self.api_manager.fetch_projects()
            
            if projects:
                self.root.after(0, lambda: self._update_projects_data(projects))
            else:
                self.root.after(0, lambda: self.log_message(f"❌ {message}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"獲取專案資料時發生錯誤: {e}"))
    
    def _update_projects_data(self, projects):
        """更新專案資料"""
        self.projects_data = projects
        self.populate_projects_tree()
        
        total_versions = sum(len(versions) for versions in projects.values())
        self.log_message(f"專案列表已更新: {len(projects)} 個專案, {total_versions} 個版本")
        
        # 保存到配置
        self.save_config()
    
    def test_api_connection(self):
        """測試 API 連接"""
        self.log_message("正在測試 API 連接...")
        self.test_btn.configure(state='disabled')
        
        # 更新狀態為測試中
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ffff00', outline='')
        
        # 更新 API 管理器的憑證
        self.api_manager.update_credentials(
            self.api_token.get(), 
            self.subdomain.get()
        )
        
        # 在背景執行緒中測試連接
        threading.Thread(target=self._test_connection_thread, daemon=True).start()
    
    def _update_connection_status(self, connected):
        """更新連接狀態顯示"""
        # 更新狀態標籤
        if connected:
            self.status_label.configure(text="Connected")
        else:
            self.status_label.configure(text="Disconnected")
        
        # 更新按鈕
        if connected:
            self.test_btn.configure(text="Disconnect", command=self.disconnect_api, state='normal')
        else:
            self.test_btn.configure(text="Reconnect", command=self.test_api_connection, state='normal')
    
    def disconnect_api(self):
        """斷開 API 連接"""
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ff0000', outline='')
        
        self._update_connection_status(False)
        self.log_message("已斷開 API 連接")
    
    def test_api_connection(self):
        """測試 API 連接"""
        self._manual_connection = True  # 標記為手動連接
        self.log_message("正在測試 API 連接...")
        self.test_btn.configure(state='disabled')
        
        # 更新狀態為測試中
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ffff00', outline='')
        
        # 更新 API 管理器的憑證
        self.api_manager.update_credentials(
            self.api_token.get(), 
            self.subdomain.get()
        )
        
        # 在背景執行緒中測試連接
        threading.Thread(target=self._test_connection_thread, daemon=True).start()
    
    def _test_connection_thread(self):
        """在背景執行緒中測試連接"""
        success, message = self.api_manager.test_connection()
        
        if success:
            self.root.after(0, self._connection_success)
        else:
            self.root.after(0, lambda: self._connection_failed(message))
    
    def _connection_success(self):
        """連接成功"""
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#00ff00', outline='')
        
        # 更新狀態文字和按鈕
        self._update_connection_status(True)
        self.log_message("API 連接測試成功")
        self.save_config()
    
    def _connection_failed(self, error_message):
        """連接失敗"""
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill='#ff0000', outline='')
        
        # 更新狀態文字和按鈕
        self._update_connection_status(False)
        self.log_message(f"API 連接測試失敗: {error_message}")
        # 自動連線失敗時不彈出錯誤對話框，只有手動點擊時才彈出
        if hasattr(self, '_manual_connection') and self._manual_connection:
            messagebox.showerror("連接失敗", f"API 連接測試失敗:\n{error_message}")
            self._manual_connection = False
    
    def browse_output_folder(self):
        """瀏覽輸出資料夾"""
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)
            self.log_message(f"輸出路徑已更新: {folder}")
            self.save_config()
    
    def generate_reports(self):
        """生成報告"""
        if self.is_generating:
            messagebox.showwarning("警告", "報告正在生成中，請稍候...")
            return
        
        if not self.selected_versions:
            messagebox.showwarning("警告", "請至少選擇一個版本")
            return
        
        if not self.standard_report.get() and not self.detailed_report.get():
            messagebox.showwarning("警告", "請至少選擇一種報告類型")
            return
        
        # 確保輸出目錄存在
        output_dir = self.output_path.get()
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("錯誤", f"無法建立輸出目錄: {e}")
            return
        
        # 更新報告生成器配置
        self.report_generator.update_config(
            self.api_token.get(),
            self.subdomain.get(),
            self.organization.get()
        )
        
        # 準備報告類型
        report_types = []
        if self.standard_report.get():
            report_types.append("standard")
        if self.detailed_report.get():
            report_types.append("detailed")
        
        # 準備選中的版本資料
        selected_version_data = []
        for project_name, versions in self.projects_data.items():
            for version_data in versions:
                if version_data['version_id'] in self.selected_versions:
                    selected_version_data.append(version_data)
        
        total_reports = len(selected_version_data) * len(report_types)
        self.log_message(f"開始生成報告: {len(selected_version_data)} 版本 × {len(report_types)} 類型 = {total_reports} 個報告")
        
        # 重置進度條
        self._update_progress(0)
        
        # 開始生成
        self.is_generating = True
        self.generation_cancelled = False
        self.generate_btn.configure(state='disabled', text='Generating...')
        
        # 在背景執行緒中生成報告
        threading.Thread(target=self._generate_reports_thread, 
                        args=(selected_version_data, report_types, output_dir), 
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
                
                self.root.after(0, lambda v=version: self.log_message(f"📄 正在處理版本: {v}"))
                
                for report_type in report_types:
                    if self.generation_cancelled:
                        break
                    
                    report_suffix = "Standard" if report_type == "standard" else "Detailed"
                    self.root.after(0, lambda s=report_suffix: self.log_message(f"⚙️ 生成 {s} 報告..."))
                    
                    # 生成報告
                    success, result = self.report_generator.generate_single_report(
                        version, version_id, report_type, output_dir
                    )
                    
                    completed_reports += 1
                    progress = int((completed_reports / total_reports) * 100)
                    
                    if success:
                        successful_reports.append(result)
                        filename = os.path.basename(result)
                        self.root.after(0, lambda f=filename: self.log_message(f"報告生成成功: {f}"))
                    else:
                        failed_reports.append(f"{version}_{report_suffix}")
                        self.root.after(0, lambda v=version, s=report_suffix, e=result: 
                                      self.log_message(f"❌ 報告生成失敗: {v}_{s} - {e}"))
                    
                    # 更新進度
                    self.root.after(0, lambda p=progress: self._update_progress(p))
            
            # 生成完成
            self.root.after(0, lambda: self._generation_complete(successful_reports, failed_reports))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ 生成過程發生錯誤: {e}"))
            self.root.after(0, lambda: self._generation_complete([], []))
    
    def _update_progress(self, progress):
        """更新進度"""
        self.progress_var.set(progress)
        self.progress_label.configure(text=f"{progress}%")
    
    def _generation_complete(self, successful_reports, failed_reports):
        """生成完成"""
        self.is_generating = False
        self.generate_btn.configure(state='normal', text='Generate Reports')
        
        total_success = len(successful_reports)
        total_failed = len(failed_reports)
        
        if total_failed == 0:
            self.log_message("🎉 所有報告生成完成！")
            messagebox.showinfo("完成", f"成功生成 {total_success} 個報告！")
        else:
            self.log_message(f"⚠️ 生成完成：成功 {total_success} 個，失敗 {total_failed} 個")
            messagebox.showwarning("部分完成", f"成功生成 {total_success} 個報告\n失敗 {total_failed} 個報告")
        
        # 設定最終進度
        if total_success > 0 or total_failed > 0:
            self._update_progress(100)
        else:
            self._update_progress(0)
    
    def save_config(self):
        """儲存配置"""
        # 準備配置資料
        config = {
            "API_TOKEN": self.api_token.get(),
            "SUBDOMAIN": self.subdomain.get(),
            "ORGANIZATION": self.organization.get(),
            "OUTPUT_PATH": self.output_path.get(),
            "STANDARD_REPORT": self.standard_report.get(),
            "DETAILED_REPORT": self.detailed_report.get(),
            "SELECTED_VERSIONS": [],
            "PROJECTS_DATA": {}
        }
        
        # 準備選中的版本資料
        for project_name, versions in self.projects_data.items():
            for version_data in versions:
                if version_data['version_id'] in self.selected_versions:
                    config["SELECTED_VERSIONS"].append({
                        "project": project_name,
                        "version": version_data['version'],
                        "version_id": version_data['version_id']
                    })
        
        # 準備專案資料
        for project_name, versions in self.projects_data.items():
            config["PROJECTS_DATA"][project_name] = []
            for version_data in versions:
                config["PROJECTS_DATA"][project_name].append({
                    "version": version_data['version'],
                    "project_id": version_data['project_id'],
                    "version_id": version_data['version_id'],
                    "created": version_data.get('created', ''),
                    "selected": version_data['version_id'] in self.selected_versions
                })
        
        # 儲存配置
        if self.config_manager.save_config(config):
            self.config = config
    
    def log_message(self, message):
        """記錄訊息到日誌"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def on_closing(self):
        """應用程式關閉時的處理"""
        if self.is_generating:
            if messagebox.askokcancel("確認關閉", "報告正在生成中，確定要關閉應用程式嗎？"):
                self.generation_cancelled = True
                self.save_config()
                self.root.destroy()
        else:
            self.save_config()
            self.root.destroy()

def main():
    root = tk.Tk()
    app = ModularTMflowReportGeneratorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()