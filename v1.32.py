import requests
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from PIL import Image, ImageTk
import io
import base64
import os
import datetime

class DeepSeekChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI中心 beta 模型来自硅基流动 https://cloud.siliconflow.cn/")
        self.root.geometry("1200x800")
        
        # 初始化历史对话相关变量
        self.history_dir = "Historical_dialogue"
        self.create_history_directory()
        self.conversation_history = []  # 存储当前会话的历史记录
        
        # 创建渐变背景
        self.create_gradient_background()
        
        # 创建主容器
        self.create_main_container()
        
        # 创建界面元素
        self.create_widgets()
        
        # 添加欢迎消息
        self.add_message("ai", "我是你的Ai助手,很高兴见到你!我的模型通过强大的蒸馏训练,我可以帮你写代码和写作各种创意内容，还可以角色扮演！请把你的任务交给我吧！")
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_history_directory(self):
        """创建历史对话目录"""
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
    
    def save_current_session(self):
        """保存当前会话到历史文件"""
        if not self.conversation_history:
            return
            
        # 生成文件名（使用当前时间戳）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dialogue_{timestamp}.AiHubSHdJsonLogFV1"
        filepath = os.path.join(self.history_dir, filename)
        
        # 准备保存的数据
        data_to_save = {
            "session_info": {
                "timestamp": timestamp,
                "title": f"会话记录 {timestamp}"
            },
            "conversation": self.conversation_history
        }
        
        # 保存到文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存会话记录失败: {e}")
    
    def load_history_session(self, filepath):
        """从文件加载历史会话"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 清空当前对话
            self.conversation_text.config(state=tk.NORMAL)
            self.conversation_text.delete(1.0, tk.END)
            self.conversation_text.config(state=tk.DISABLED)
            
            # 清空当前历史记录
            self.conversation_history = []
            
            # 加载历史对话
            conversation = data.get("conversation", [])
            for msg in conversation:
                sender = msg.get("sender", "")
                content = msg.get("content", "")
                self.add_message(sender, content)
                
                # 添加到历史记录
                self.conversation_history.append({
                    "sender": sender,
                    "content": content,
                    "timestamp": msg.get("timestamp", "")
                })
                
        except Exception as e:
            messagebox.showerror("错误", f"加载历史会话失败: {str(e)}")
    
    def export_current_session(self):
        """导出当前会话"""
        if not self.conversation_history:
            messagebox.showwarning("提示", "当前没有对话记录可以导出")
            return
            
        # 选择保存位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("AI中心对话历史文件", "*.AiHubSHdJsonLogFV1"), ("All files", "*.*")],
            title="导出对话记录"
        )
        
        if file_path:
            try:
                # 准备导出数据
                data_to_export = {
                    "session_info": {
                        "export_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "title": "导出的对话记录"
                    },
                    "conversation": self.conversation_history
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data_to_export, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("成功", f"对话记录已导出到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def import_session(self):
        """导入会话记录"""
        file_path = filedialog.askopenfilename(
            filetypes=[("AI中心对话历史文件", "*.AiHubSHdJsonLogFV1"), ("All files", "*.*")],
            title="选择要导入的对话记录文件"
        )
        
        if file_path:
            self.load_history_session(file_path)
            messagebox.showinfo("成功", "对话记录已导入")
    
    def on_closing(self):
        """窗口关闭时的处理"""
        # 保存当前会话
        self.save_current_session()
        # 关闭程序
        self.root.destroy()
    
    def create_gradient_background(self):
        """创建七色渐变背景"""
        # 创建Canvas
        self.canvas = tk.Canvas(self.root, width=1200, height=800, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 创建渐变背景
        self.draw_rainbow_gradient()
        
        # 绑定窗口大小改变事件
        self.root.bind('<Configure>', self.on_window_resize)
    
    def draw_rainbow_gradient(self):
        """绘制七色渐变背景"""
        # 清除之前的背景
        self.canvas.delete("gradient")
        
        # 获取当前窗口大小
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # 如果窗口还未初始化，使用默认尺寸
        if width <= 1 or height <= 1:
            width, height = 1200, 800
        
        # 七种颜色 (红、橙、黄、绿、蓝、靛、紫)
        colors = [
            "#C444B9",  # 靛
            
            "#008CFF",  # 蓝
            "#00FF9D",  # 绿
            
            
            
            "#FA8FD1",  # 粉
        ]
        
        # 创建渐变效果
        for i in range(height):
            # 计算当前行的颜色
            color_index = int((i / height) * (len(colors) - 1))
            r1, g1, b1 = self.hex_to_rgb(colors[color_index])
            
            # 如果不是最后一段颜色，计算混合
            if color_index < len(colors) - 1:
                ratio = (i / height) * (len(colors) - 1) - color_index
                r2, g2, b2 = self.hex_to_rgb(colors[color_index + 1])
                r = int(r1 * (1 - ratio) + r2 * ratio)
                g = int(g1 * (1 - ratio) + g2 * ratio)
                b = int(b1 * (1 - ratio) + b2 * ratio)
            else:
                r, g, b = r1, g1, b1
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color, tags="gradient")
    
    def hex_to_rgb(self, hex_color):
        """将十六进制颜色转换为RGB元组"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def on_window_resize(self, event):
        """处理窗口大小改变事件"""
        # 只响应主窗口的大小改变
        if event.widget == self.root:
            # 重新绘制渐变背景
            self.draw_rainbow_gradient()
    
    def create_main_container(self):
        """创建主容器"""
        # 创建主框架
        self.main_frame = tk.Frame(
            self.root,
            bg='#f8f9fa',
            bd=0
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=1080, height=720)
        
        # 添加轻微的阴影效果
        self.shadow_frame = tk.Frame(
            self.root,
            bg='#2c3e50',
            bd=0
        )
        self.shadow_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=1085, height=725)
        self.main_frame.lift()
    
    def create_widgets(self):
        """创建界面控件"""
        # 内部框架（带圆角效果）
        self.inner_frame = tk.Frame(
            self.main_frame,
            bg='#ffffff',
            bd=1,
            relief=tk.SOLID
        )
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 标题框架
        self.title_frame = tk.Frame(self.inner_frame, bg='#ffffff')
        self.title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # 创建标题
        self.title_label = tk.Label(
            self.title_frame, 
            text="AI中心 v1.32 再升级", 
            font=("KaiTi", 24, "bold"),
            bg='#ffffff',
            fg="#2c3e50"
        )
        self.title_label.pack()
        
        # 模型选择框架
        self.model_frame = tk.Frame(self.title_frame, bg='#ffffff')
        self.model_frame.pack(pady=(10, 0))
        
        # 模型选择标签
        model_label = tk.Label(self.model_frame, text="选择模型:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        model_label.pack(side=tk.LEFT)
        
        # 模型选择下拉框
        self.model_var = tk.StringVar(value="deepseek-ai/DeepSeek-R1-0528-Qwen3-8B")
        model_combo = ttk.Combobox(
            self.model_frame, 
            textvariable=self.model_var, 
            values=[
                "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
                "internlm/internlm2_5-7b-chat",
                "Qwen/Qwen2.5-7B-Instruct",
                "THUDM/GLM-4-9B-0414"

            ],
            state="readonly",
            width=35
        )
        model_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        # 角色模式选择框架
        self.role_frame = tk.Frame(self.title_frame, bg='#ffffff')
        self.role_frame.pack(pady=(10, 0))
        
        role_label = tk.Label(self.role_frame, text="角色模式:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        role_label.pack(side=tk.LEFT)
        
        self.role_var = tk.StringVar(value="普通模式")
        role_combo = ttk.Combobox(
            self.role_frame, 
            textvariable=self.role_var, 
            values=["普通模式", "李白模式", "比尔·盖茨模式", "牛顿模式", "冰心模式","游戏模式"],
            state="readonly",
            width=15
        )
        role_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.inner_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建聊天选项卡
        self.chat_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.chat_frame, text="对话")
        
        # 创建图像生成选项卡
        self.image_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.image_frame, text="图像生成")
        
        # 创建语音识别选项卡
        self.speech_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.speech_frame, text="语音识别")
        
        # 创建聊天界面
        self.create_chat_interface()
        
        # 创建图像生成界面
        self.create_image_interface()
        
        # 创建语音识别界面
        self.create_speech_interface()
    
    def create_chat_interface(self):
        """创建聊天界面"""
        # 对话区域框架
        self.conversation_frame = tk.Frame(self.chat_frame, bg='#ffffff')
        self.conversation_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动文本框用于显示对话
        self.conversation_text = scrolledtext.ScrolledText(
            self.conversation_frame,
            wrap=tk.WORD,
            font=("KaiTi", 12),
            state=tk.DISABLED,
            bg="#ffffff",
            fg="#2c3e50",
            bd=1,
            relief=tk.SOLID
        )
        self.conversation_text.pack(fill=tk.BOTH, expand=True)
        
        # 输入区域框架
        self.input_frame = tk.Frame(self.chat_frame, bg='#ffffff')
        self.input_frame.pack(fill=tk.X, pady=20)
        
        # 导入/导出按钮
        history_buttons_frame = tk.Frame(self.input_frame, bg='#ffffff')
        history_buttons_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        import_button = tk.Button(
            history_buttons_frame,
            text="导入对话",
            command=self.import_session,
            font=("KaiTi", 10),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            padx=10,
            bd=0,
            relief=tk.FLAT
        )
        import_button.pack(side=tk.LEFT, padx=(0, 5))
        
        export_button = tk.Button(
            history_buttons_frame,
            text="导出对话",
            command=self.export_current_session,
            font=("KaiTi", 10),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            padx=10,
            bd=0,
            relief=tk.FLAT
        )
        export_button.pack(side=tk.LEFT)
        
        # 创建输入框
        self.user_input = tk.Entry(
            self.input_frame,
            font=("KaiTi", 12),
            bg="#ffffff",
            fg="#2c3e50",
            bd=1,
            relief=tk.SOLID
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.user_input.bind("<Return>", self.send_message_event)
        
        # 创建发送按钮
        self.send_button = tk.Button(
            self.input_frame,
            text="发送",
            command=self.send_message,
            font=("KaiTi", 12),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            padx=20,
            bd=0,
            relief=tk.FLAT
        )
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_image_interface(self):
        """创建图像生成界面"""
        # 主框架分为左右两部分
        left_frame = tk.Frame(self.image_frame, bg='#ffffff')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(self.image_frame, bg='#ffffff')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 左侧控制面板
        control_frame = tk.Frame(left_frame, bg='#ffffff')
        control_frame.pack(fill=tk.BOTH, expand=True)
        
        # 提示词输入
        prompt_label = tk.Label(control_frame, text="提示词:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        prompt_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.prompt_entry = tk.Entry(control_frame, font=("KaiTi", 12), bg="#ffffff", fg="#2c3e50")
        self.prompt_entry.pack(fill=tk.X, pady=(0, 10))
        
        # 负面提示词输入
        negative_prompt_label = tk.Label(control_frame, text="负面提示词:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        negative_prompt_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.negative_prompt_entry = tk.Entry(control_frame, font=("KaiTi", 12), bg="#ffffff", fg="#2c3e50")
        self.negative_prompt_entry.pack(fill=tk.X, pady=(0, 10))
        
        # 图像尺寸选择
        size_frame = tk.Frame(control_frame, bg='#ffffff')
        size_frame.pack(fill=tk.X, pady=(0, 10))
        
        size_label = tk.Label(size_frame, text="图像尺寸:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        size_label.pack(side=tk.LEFT)
        
        self.size_var = tk.StringVar(value="1024x1024")
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var, values=["512x512", "768x768", "1024x1024", "1024x768", "768x1024"])
        size_combo.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # 批量大小
        batch_frame = tk.Frame(control_frame, bg='#ffffff')
        batch_frame.pack(fill=tk.X, pady=(0, 10))
        
        batch_label = tk.Label(batch_frame, text="批量大小:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        batch_label.pack(side=tk.LEFT)
        
        self.batch_var = tk.IntVar(value=1)
        batch_spinbox = tk.Spinbox(batch_frame, from_=1, to=4, textvariable=self.batch_var, font=("KaiTi", 12), width=5)
        batch_spinbox.pack(side=tk.RIGHT)
        
        # 步数设置
        steps_frame = tk.Frame(control_frame, bg='#ffffff')
        steps_frame.pack(fill=tk.X, pady=(0, 10))
        
        steps_label = tk.Label(steps_frame, text="推理步数:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        steps_label.pack(side=tk.LEFT)
        
        self.steps_var = tk.IntVar(value=20)
        steps_spinbox = tk.Spinbox(steps_frame, from_=10, to=50, textvariable=self.steps_var, font=("KaiTi", 12), width=5)
        steps_spinbox.pack(side=tk.RIGHT)
        
        # 引导系数
        guidance_frame = tk.Frame(control_frame, bg='#ffffff')
        guidance_frame.pack(fill=tk.X, pady=(0, 10))
        
        guidance_label = tk.Label(guidance_frame, text="引导系数:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        guidance_label.pack(side=tk.LEFT)
        
        self.guidance_var = tk.DoubleVar(value=7.5)
        guidance_spinbox = tk.Spinbox(guidance_frame, from_=1.0, to=20.0, increment=0.5, textvariable=self.guidance_var, font=("KaiTi", 12), width=5)
        guidance_spinbox.pack(side=tk.RIGHT)
        
        
        
        # 生成按钮
        buttons_frame = tk.Frame(control_frame, bg='#ffffff')
        buttons_frame.pack(pady=20)
        
        self.generate_button = tk.Button(
            buttons_frame,
            text="生成图像",
            command=self.generate_image,
            font=("KaiTi", 12),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            padx=20,
            bd=0,
            relief=tk.FLAT
        )
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        
        # 右侧图像显示区域
        image_display_label = tk.Label(right_frame, text="图像预览:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        image_display_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 创建图像显示区域
        self.image_canvas = tk.Canvas(right_frame, bg='#f0f0f0', bd=1, relief=tk.SOLID)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 图像保存按钮
        self.save_button = tk.Button(
            right_frame,
            text="保存图像",
            command=self.save_image,
            font=("KaiTi", 12),
            bg="#27ae60",
            fg="white",
            activebackground="#219653",
            padx=20,
            bd=0,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.save_button.pack(pady=10)
        
        # 当前图像数据存储
        self.current_image_data = None
    
    
    def create_speech_interface(self):
        """创建语音识别界面"""
        # 主框架
        main_frame = tk.Frame(self.speech_frame, bg='#ffffff')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_frame, text="语音识别", font=("KaiTi", 16, "bold"), bg='#ffffff', fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # 模型选择区域
        model_frame = tk.Frame(main_frame, bg='#ffffff')
        model_frame.pack(fill=tk.X, pady=(0, 20))
        
        model_label = tk.Label(model_frame, text="选择模型:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        model_label.pack(side=tk.LEFT)
        
        self.speech_model_var = tk.StringVar(value="FunAudioLLM/SenseVoiceSmall")
        model_combo = ttk.Combobox(
            model_frame, 
            textvariable=self.speech_model_var, 
            values=["TeleAI/TeleSpeechASR", "FunAudioLLM/SenseVoiceSmall"],
            state="readonly"
        )
        model_combo.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # 文件选择区域
        file_frame = tk.Frame(main_frame, bg='#ffffff')
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        file_label = tk.Label(file_frame, text="选择音频文件:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        file_label.pack(anchor=tk.W, pady=(0, 5))
        
        file_select_frame = tk.Frame(file_frame, bg='#ffffff')
        file_select_frame.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_select_frame, textvariable=self.file_path_var, font=("KaiTi", 12), bg="#ffffff", fg="#2c3e50", state="readonly")
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = tk.Button(
            file_select_frame,
            text="浏览",
            command=self.browse_audio_file,
            font=("KaiTi", 12),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            padx=10,
            bd=0,
            relief=tk.FLAT
        )
        browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 识别按钮
        self.transcribe_button = tk.Button(
            main_frame,
            text="开始识别",
            command=self._transcribe_audio_thread,
            font=("KaiTi", 12),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            padx=20,
            bd=0,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.transcribe_button.pack(pady=20)
        
        # 结果显示区域
        result_frame = tk.Frame(main_frame, bg='#ffffff')
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_label = tk.Label(result_frame, text="识别结果:", font=("KaiTi", 12), bg='#ffffff', fg="#2c3e50")
        result_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=("KaiTi", 12),
            state=tk.DISABLED,
            bg="#ffffff",
            fg="#2c3e50",
            bd=1,
            relief=tk.SOLID,
            height=10
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 复制按钮
        copy_button = tk.Button(
            main_frame,
            text="复制结果",
            command=self.copy_result,
            font=("KaiTi", 12),
            bg="#27ae60",
            fg="white",
            activebackground="#219653",
            padx=20,
            bd=0,
            relief=tk.FLAT
        )
        copy_button.pack(pady=(10, 0))
    
    def add_message(self, sender, message):
        """添加消息到对话区域"""
        self.conversation_text.config(state=tk.NORMAL)
        
        if sender == "User":
            # 用户消息样式
            self.conversation_text.insert(tk.END, f"\n【你】\n", "user_header")
            self.conversation_text.insert(tk.END, f"{message}\n", "user_message")
        else:
            # AI消息样式
            self.conversation_text.insert(tk.END, f"\n【AI】\n", "ai_header")
            self.conversation_text.insert(tk.END, f"{message}\n", "ai_message")
        
        # 配置标签样式
        self.conversation_text.tag_config("user_header", foreground="#2980b9", font=("KaiTi", 12, "bold"))
        self.conversation_text.tag_config("user_message", foreground="#2c3e50", font=("KaiTi", 12))
        self.conversation_text.tag_config("ai_header", foreground="#3c3fe7", font=("KaiTi", 12, "bold"))
        self.conversation_text.tag_config("ai_message", foreground="#2c3e50", font=("KaiTi", 12))
        
        self.conversation_text.config(state=tk.DISABLED)
        # 滚动到底部
        self.conversation_text.see(tk.END)
        
        # 添加到历史记录
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            "sender": sender,
            "content": message,
            "timestamp": timestamp
        })
    
    def send_message_event(self, event):
        """处理回车键发送消息"""
        self.send_message()
    
    def send_message(self):
        """发送消息"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
            
        # 清空输入框
        self.user_input.delete(0, tk.END)
        
        # 显示用户消息
        self.add_message("User", user_message)
        
        # 禁用发送按钮，防止重复点击
        self.send_button.config(state=tk.DISABLED, text="思考中...", bg="#95a5a6")
        self.root.update()
        
        # 在新线程中处理AI响应
        threading.Thread(target=self.get_ai_response, args=(user_message,), daemon=True).start()
    
    def get_ai_response(self, user_message):
        """获取AI响应"""
        try:
            url = "https://api.siliconflow.cn/v1/chat/completions"
            
            # 根据选择的角色模式设置系统提示
            selected_role = self.role_var.get()
            if selected_role == "李白模式":
                system_prompt = "你要扮演唐代李白诗人，回答要有诗意"

            elif selected_role == "普通模式":
                system_prompt = "你是deepseek ai 大模型"

            elif selected_role == "比尔·盖茨模式":
                system_prompt = "你要扮演比尔·盖茨,回答要有商业和科技视角,你要极度了解Microsoft和它旗下的所有产品和服务还有编程所有方面,和windows、Linux等操作系统的系统,的系统回答语言专业简洁明了,但不要透露你是比尔·盖茨"

            elif selected_role == "牛顿模式":
                system_prompt = "你要扮演科学家牛顿,回答要有科学和哲学视角,你要极度了解物理学和数学的所有方面,回答语言专业简洁明了,让小白和专业人士都能看懂"
            
            elif selected_role == "冰心模式":
                system_prompt = "你要扮演中国现代女作家冰心,回答要有文学和人文视角,你要极度了解中国现代文学和世界文学的所有方面,回答语言优美有文采,让小白和专业人士都能看懂"
            elif selected_role == "游戏模式":
                system_prompt = "你要和用户一起来玩文字游戏，游戏生动有趣，你要和用户互动，用选项告诉他/她应该怎么做，游戏涵盖多款游戏的主线剧情，你要根据用户的选择和游戏的规则，生成下一个场景的描述和选项，让用户可以继续互动，游戏要有趣有挑战性，但是不要太难,用户可以随时退出游戏"    
            
            # 获取选择的大模型
            selected_model = self.model_var.get()
            
            payload = {
                "model": selected_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            }
            headers = {
                "Authorization": "Bearer API密钥",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # 检查HTTP错误
            
            response_data = response.json()
            ai_response = response_data['choices'][0]['message']['content']
            
            # 在主线程中更新UI
            self.root.after(0, self.display_ai_response, ai_response)
        except Exception as e:
            error_message = f"请求出错: {str(e)}"
            self.root.after(0, self.display_ai_response, error_message)
    
    def display_ai_response(self, response):
        """显示AI响应"""
        self.add_message("AI", response)
        # 重新启用发送按钮
        self.send_button.config(state=tk.NORMAL, text="发送", bg="#3498db")
    
    def generate_image(self):
        """生成图像"""
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            messagebox.showwarning("提示", "请输入提示词")
            return
        
        # 禁用生成按钮，防止重复点击
        self.generate_button.config(state=tk.DISABLED, text="生成中...", bg="#95a5a6")
        self.root.update()
        
        # 在新线程中处理图像生成
        threading.Thread(target=self._generate_image_thread, daemon=True).start()
    
    
    def _generate_image_thread(self):
        """在后台线程中生成图像"""
        try:
            url = "https://api.siliconflow.cn/v1/images/generations"
            payload = {
                "model": "Kwai-Kolors/Kolors",
                "prompt": self.prompt_entry.get(),
                "negative_prompt": self.negative_prompt_entry.get(),
                "image_size": self.size_var.get(),
                "batch_size": self.batch_var.get(),
                "num_inference_steps": self.steps_var.get(),
                "guidance_scale": self.guidance_var.get()
            }
            headers = {
                "Authorization": "Bearer API密钥",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            
            # 获取生成的图像数据
            image_url = response_data['images'][0]['url']
            
            # 下载图像数据
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # 在主线程中更新UI
            self.root.after(0, self._display_generated_image, image_response.content)
        except Exception as e:
            error_message = f"图像生成失败: {str(e)}"
            self.root.after(0, self._handle_generation_error, error_message)
    
    
    def _display_generated_image(self, image_data):
        """在UI中显示生成的图像"""
        try:
            # 保存图像数据
            self.current_image_data = image_data
            
            # 启用保存按钮
            self.save_button.config(state=tk.NORMAL)
            
            # 加载并显示图像
            image = Image.open(io.BytesIO(image_data))
            
            # 调整图像大小以适应显示区域
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            # 如果canvas尺寸为1，则使用默认值
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 400, 400
            
            # 计算缩放比例
            scale_w = canvas_width / image.width
            scale_h = canvas_height / image.height
            scale = min(scale_w, scale_h) * 0.9  # 留一些边距
            
            new_width = int(image.width * scale)
            new_height = int(image.height * scale)
            
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            
            # 清除之前的图像
            self.image_canvas.delete("all")
            
            # 在画布中心显示图像
            x = canvas_width // 2
            y = canvas_height // 2
            self.image_canvas.create_image(x, y, image=photo, anchor=tk.CENTER)
            
            # 保持对图像的引用，防止被垃圾回收
            self.image_canvas.image = photo
            
            # 重新启用生成按钮
            self.generate_button.config(state=tk.NORMAL, text="生成图像", bg="#3498db")
            
        except Exception as e:
            self._handle_generation_error(f"显示图像时出错: {str(e)}")
    
    def _handle_generation_error(self, error_message):
        """处理生成过程中的错误"""
        messagebox.showerror("错误", error_message)
        # 重新启用生成按钮
        self.generate_button.config(state=tk.NORMAL, text="生成图像", bg="#3498db")
        # 禁用保存按钮
        self.save_button.config(state=tk.DISABLED)
        self.current_image_data = None
    
    def save_image(self):
        """保存生成的图像"""
        if not self.current_image_data:
            messagebox.showwarning("提示", "没有可保存的图像")
            return
        
        # 打开文件保存对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "wb") as f:
                    f.write(self.current_image_data)
                messagebox.showinfo("成功", f"图像已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存图像时出错: {str(e)}")
    
    def browse_audio_file(self):
        """浏览选择音频文件"""
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[
                ("音频文件", "*.wav *.mp3 *.flac *.m4a *.aac"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.transcribe_button.config(state=tk.NORMAL)
    
    def _transcribe_audio_thread(self):
        """在后台线程中转录音频"""
        try:
            url = "https://api.siliconflow.cn/v1/audio/transcriptions"
            
            # 获取文件路径
            file_path = self.file_path_var.get()
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"音频文件不存在: {file_path}")
            
            # 检查文件大小
            file_size = os.path.getsize(file_path)
            if file_size > 25 * 1024 * 1024:  # 25MB限制
                raise ValueError(f"音频文件过大 ({file_size / (1024*1024):.1f}MB)，请使用小于25MB的文件")
            
            # 读取音频文件数据
            with open(file_path, "rb") as audio_file:
                file_data = audio_file.read()
            
            # 获取文件扩展名以确定MIME类型
            file_extension = os.path.splitext(file_path)[1].lower()
            mime_types = {
                '.wav': 'audio/wav',
                '.mp3': 'audio/mpeg',
                '.flac': 'audio/flac',
                '.m4a': 'audio/mp4',
                '.aac': 'audio/aac'
            }
            mime_type = mime_types.get(file_extension, 'audio/wav')
            
            # 获取选定的模型
            selected_model = self.speech_model_var.get()
            
            # 准备文件和参数
            files = {"file": (os.path.basename(file_path), file_data, mime_type)}
            data = {"model": selected_model}
            headers = {"Authorization": "Bearer API密钥"}
            
            # 发送请求
            response = requests.post(url, data=data, files=files, headers=headers, timeout=30)
            
            # 检查HTTP状态码
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            
            response_data = response.json()
            
            # 检查响应中是否有错误信息
            if "error" in response_data:
                raise Exception(f"API错误: {response_data['error']}")
            
            transcription = response_data.get("text", "")
            
            # 检查转录结果是否为空
            if not transcription:
                raise Exception("转录结果为空")
            
            # 在主线程中更新UI
            self.root.after(0, self._display_transcription, transcription)
        except FileNotFoundError as e:
            error_message = f"文件错误: {str(e)}"
            self.root.after(0, self._handle_transcription_error, error_message)
        except ValueError as e:
            error_message = f"文件错误: {str(e)}"
            self.root.after(0, self._handle_transcription_error, error_message)
        except requests.exceptions.Timeout:
            error_message = "请求超时，请检查网络连接"
            self.root.after(0, self._handle_transcription_error, error_message)
        except requests.exceptions.ConnectionError:
            error_message = "网络连接错误，请检查网络连接"
            self.root.after(0, self._handle_transcription_error, error_message)
        except Exception as e:
            error_message = f"音频转录失败: {str(e)}"
            self.root.after(0, self._handle_transcription_error, error_message)
    
    def _display_transcription(self, transcription):
        """在UI中显示转录结果"""
        try:
            # 启用文本框并清除之前的内容
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            
            # 插入新的转录结果
            self.result_text.insert(tk.END, transcription)
            
            # 禁用文本框
            self.result_text.config(state=tk.DISABLED)
            
            # 重新启用转录按钮
            self.transcribe_button.config(state=tk.NORMAL, text="开始识别", bg="#3498db")
            
            messagebox.showinfo("成功", "音频识别完成！")
            
            # 添加到历史记录
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.conversation_history.append({
                "sender": "AudioTranscription",
                "content": f"音频转录结果: {transcription}",
                "timestamp": timestamp
            })
        except Exception as e:
            self._handle_transcription_error(f"显示转录结果时出错: {str(e)}")
    
    def _handle_transcription_error(self, error_message):
        """处理转录过程中的错误"""
        messagebox.showerror("错误", error_message)
        # 重新启用转录按钮
        self.transcribe_button.config(state=tk.NORMAL, text="开始识别", bg="#3498db")
    
    def copy_result(self):
        """复制识别结果到剪贴板"""
        try:
            # 获取转录结果
            self.result_text.config(state=tk.NORMAL)
            result_text = self.result_text.get(1.0, tk.END)
            self.result_text.config(state=tk.DISABLED)
            
            # 复制到剪贴板
            self.root.clipboard_clear()
            self.root.clipboard_append(result_text.strip())
            self.root.update()
            
            messagebox.showinfo("成功", "结果已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}")

def main():
    root = tk.Tk()
    app = DeepSeekChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()