#!/usr/bin/env python3
import time
import random
import sys
import os
import subprocess
from datetime import datetime

# 获取终端尺寸
def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24  # 默认值

# 清屏函数
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# 颜色代码
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# 创建适应宽度的字符串
def create_fit_text(text, width, padding_char=" "):
    text_len = len(text.strip())
    if text_len >= width:
        return text[:width-3] + "..."
    
    padding = (width - text_len) // 2
    return padding_char * padding + text + padding_char * (width - text_len - padding)

# 创建分隔线
def create_separator(width, char="═"):
    return char * width

# 音频播放函数
def play_audio(audio_file="audio.mp3"):
    audio_played = False
    
    # 首先尝试使用pygame播放
    try:
        import pygame
        pygame.mixer.init()
        if os.path.exists(audio_file):
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            audio_played = True
            print(f"{Colors.CYAN}AUDIO: Playing {audio_file} with pygame{Colors.END}")
    except ImportError:
        print(f"{Colors.YELLOW}AUDIO: Pygame not available, trying system commands{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}AUDIO: Pygame error: {e}{Colors.END}")
    
    # 如果pygame不可用或失败，尝试使用系统命令
    if not audio_played:
        try:
            if os.path.exists(audio_file):
                if sys.platform == "darwin":  # macOS
                    subprocess.run(["afplay", audio_file], check=False)
                elif sys.platform == "win32":  # Windows
                    subprocess.run(["start", audio_file], shell=True, check=False)
                else:  # Linux/Android (Termux)
                    # 尝试多种可能的音频播放器
                    for player in ["mpv", "mplayer", "ffplay", "play-audio"]:
                        try:
                            subprocess.run([player, audio_file], check=False)
                            print(f"{Colors.CYAN}AUDIO: Playing {audio_file} with {player}{Colors.END}")
                            audio_played = True
                            break
                        except FileNotFoundError:
                            continue
                
                if not audio_played:
                    print(f"{Colors.YELLOW}AUDIO: No suitable audio player found{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}AUDIO: System command error: {e}{Colors.END}")
    
    return audio_played

# 停止音频播放
def stop_audio():
    try:
        import pygame
        pygame.mixer.music.stop()
    except:
        pass  # 忽略停止错误

# 生成更真实的栈追踪
def generate_realistic_stack_trace():
    # 定义合理的调用链结构
    call_chains = [
        # 调用链1: 数据处理流程
        [
            ("com.example.Main", "main", 15),
            ("com.example.DataProcessor", "processUserData", 42),
            ("com.example.DataProcessor", "validateInput", 27),
            ("com.example.ValidationUtil", "checkNotNull", 18)
        ],
        # 调用链2: Web请求处理
        [
            ("com.example.Main", "main", 10),
            ("com.example.WebServer", "handleRequest", 88),
            ("com.example.RequestHandler", "parseRequestBody", 33),
            ("com.example.JsonParser", "getString", 56)
        ],
        # 调用链3: 文件操作
        [
            ("com.example.Main", "main", 22),
            ("com.example.FileManager", "loadConfig", 47),
            ("com.example.ConfigReader", "readProperty", 31),
            ("com.example.PropertyUtils", "getValue", 19)
        ],
        # 调用链4: 业务逻辑
        [
            ("com.example.Main", "main", 18),
            ("com.example.OrderService", "processOrder", 65),
            ("com.example.OrderService", "calculateTotal", 41),
            ("com.example.PriceCalculator", "getItemPrice", 29)
        ]
    ]
    
    # 选择一条调用链
    call_chain = random.choice(call_chains)
    
    stack_trace = []
    
    # 第一行总是 NullPointerException
    stack_trace.append("java.lang.NullPointerException")
    
    # 从最内层方法开始（抛出异常的地方）
    # 这里我们反转调用链，因为栈跟踪是从最内层到最外层
    for i, (class_name, method_name, line_num) in enumerate(reversed(call_chain)):
        stack_trace.append(f"    at {class_name}.{method_name}({class_name.split('.')[-1]}.java:{line_num})")
        
        # 在中间层偶尔添加一些反射调用
        if i == 1 and random.random() < 0.3:
            stack_trace.append("    at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)")
            stack_trace.append("    at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)")
            stack_trace.append("    at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)")
    
    # 偶尔添加线程信息
    if random.random() < 0.2:
        stack_trace.append("    at java.base/java.lang.Thread.run(Thread.java:833)")
    
    # 偶尔添加嵌套异常
    if random.random() < 0.1:
        stack_trace.append("Caused by: java.lang.IllegalArgumentException: Source must not be null")
        stack_trace.append("    at org.springframework.util.Assert.notNull(Assert.java:201)")
        stack_trace.append("    ... 4 more")
    
    return stack_trace

# 生成与栈跟踪匹配的原因
def generate_matching_cause(stack_trace):
    # 分析栈跟踪的最后几行来确定可能的原因
    last_lines = stack_trace[-4:] if len(stack_trace) > 4 else stack_trace
    
    # 检查常见模式
    for line in last_lines:
        if "getString" in line or "readProperty" in line or "getValue" in line:
            return "Attempt to invoke method on null object returned from getter"
        elif "checkNotNull" in line or "validateInput" in line:
            return "Null check failed - parameter was null"
        elif "processUserData" in line or "processOrder" in line:
            return "Business object was not properly initialized"
        elif "handleRequest" in line:
            return "Request body or parameter was null"
        elif "loadConfig" in line:
            return "Configuration file or property was missing"
    
    # 默认原因
    causes = [
        "Attempt to invoke virtual method on null object reference",
        "Trying to access field of null object", 
        "Method call on uninitialized object",
        "Array element access on null array"
    ]
    return random.choice(causes)

# 炫酷的 NullPointerException 显示
def show_null_pointer_exception():
    width, height = get_terminal_size()
    
    error_text = "java.lang.NullPointerException"
    
    # 尝试播放音频
    audio_files = ["audio.mp3", "audio.wav", "sound.mp3", "sound.wav"]
    audio_playing = False
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            audio_playing = play_audio(audio_file)
            break
    
    if not audio_playing:
        print(f"{Colors.YELLOW}AUDIO: No audio file found. Looking for: {', '.join(audio_files)}{Colors.END}")
    
    # 初始效果
    print(f"\n{Colors.RED}{Colors.BOLD}")
    for i in range(2):
        explosion_line1 = "* " * (width // 3)
        explosion_line2 = "* " * (width // 2)
        explosion_line3 = "* " * (width // 3)
        
        print(create_fit_text(explosion_line1, width))
        print(create_fit_text(explosion_line2, width))
        print(create_fit_text(explosion_line3, width))
        time.sleep(0.2)
        clear_screen()
        
        explosion_line1 = "* " * (width // 2)
        explosion_line2 = "* " * (width // 3)
        explosion_line3 = "* " * (width // 2)
        
        print(create_fit_text(explosion_line1, width))
        print(create_fit_text(explosion_line2, width))
        print(create_fit_text(explosion_line3, width))
        time.sleep(0.2)
        clear_screen()
    
    # 显示错误标题
    print(f"\n{Colors.RED}{Colors.BOLD}")
    print(create_separator(width))
    print(create_fit_text("CRITICAL SYSTEM ERROR", width))
    print(create_separator(width))
    
    # 闪烁显示错误信息
    for _ in range(4):
        print(f"{Colors.RED}{Colors.BOLD}{create_fit_text(error_text, width)}{Colors.END}")
        time.sleep(0.4)
        print(f"{Colors.WHITE}{Colors.BOLD}{create_fit_text(error_text, width)}{Colors.END}") 
        time.sleep(0.4)
    
    print(f"\n{Colors.YELLOW}{create_fit_text('NULL REFERENCE DETECTED', width)}{Colors.END}\n")
    
    # 生成栈追踪
    stack_trace = generate_realistic_stack_trace()
    
    # 生成与栈跟踪匹配的原因
    cause = generate_matching_cause(stack_trace)
    
    print(f"{Colors.CYAN}Possible Cause: {cause}{Colors.END}")
    print(f"{Colors.PURPLE}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}{Colors.END}\n")
    
    # 显示堆栈跟踪
    print(f"{Colors.BLUE}{Colors.BOLD}Stack Trace:{Colors.END}")
    print(f"{Colors.BLUE}{create_separator(width, '━')}{Colors.END}")
    
    for i, line in enumerate(stack_trace):
        time.sleep(0.15)
        # 对不同类型的行使用不同的颜色
        if "java.lang.NullPointerException" in line:
            color = Colors.RED
        elif "Caused by:" in line:
            color = Colors.PURPLE
        elif "at java.base" in line:
            color = Colors.CYAN
        elif "..." in line:
            color = Colors.YELLOW
        else:
            color = Colors.WHITE
        print(f"{color}{line}{Colors.END}")
    
    print(f"{Colors.BLUE}{create_separator(width, '━')}{Colors.END}")
    
    # 闪烁的警告信息
    print(f"\n{Colors.RED}{Colors.BOLD}")
    for _ in range(2):
        warning_line = "! " * (width // 3)
        print(create_fit_text(warning_line, width))
        warning_text = "WARNING: Application may crash or behave unexpectedly!"
        print(create_fit_text(warning_text, width))
        print(create_fit_text(warning_line, width))
        time.sleep(0.5)
        clear_screen()
        
        warning_line = "# " * (width // 3)
        print(create_fit_text(warning_line, width))
        warning_text = "NULL POINTER EXCEPTION DETECTED!"
        print(create_fit_text(warning_text, width))
        print(create_fit_text(warning_line, width))
        time.sleep(0.5)
        clear_screen()
        
        # 重新显示主要内容
        print(f"\n{Colors.RED}{Colors.BOLD}{create_fit_text(error_text, width)}{Colors.END}")
        print(f"\n{Colors.YELLOW}{create_fit_text('NULL REFERENCE DETECTED', width)}{Colors.END}\n")
        print(f"{Colors.CYAN}Possible Cause: {cause}{Colors.END}")
        print(f"{Colors.BLUE}{Colors.BOLD}Stack Trace:{Colors.END}")
        print(f"{Colors.BLUE}{create_separator(width, '━')}{Colors.END}")
        for line in stack_trace:
            if "java.lang.NullPointerException" in line:
                color = Colors.RED
            elif "Caused by:" in line:
                color = Colors.PURPLE
            elif "at java.base" in line:
                color = Colors.CYAN
            elif "..." in line:
                color = Colors.YELLOW
            else:
                color = Colors.WHITE
            print(f"{color}{line}{Colors.END}")
        print(f"{Colors.BLUE}{create_separator(width, '━')}{Colors.END}")

# 主函数
def main():
    try:
        width, height = get_terminal_size()
        print(f"{Colors.CYAN}Terminal: {width}x{height}{Colors.END}")
        time.sleep(1)
        
        show_null_pointer_exception()
        
        # 最终显示
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print(create_separator(width))
        print(create_fit_text("PROCESS TERMINATED", width))
        print(create_separator(width))
        print(f"{Colors.END}")
        
        # 退出倒计时
        print(f"\n{Colors.RED}System will exit in:{Colors.END}")
        for i in range(5, 0, -1):
            print(f"{Colors.RED}{Colors.BOLD}  {i}...{Colors.END}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Process interrupted by user{Colors.END}")
    finally:
        # 停止音频
        stop_audio()
        
        # 结束效果
        print(f"\n{Colors.CYAN}Alert system shutting down...{Colors.END}")
        for _ in range(3):
            sys.stdout.write(f"\r{Colors.YELLOW}Shutdown: {'█' * (_ + 1)}{'░' * (2 - _)} {Colors.END}")
            sys.stdout.flush()
            time.sleep(0.3)
        print(f"\n{Colors.WHITE}{Colors.BOLD}NullPointerException demonstration completed.{Colors.END}")

if __name__ == "__main__":
    main()