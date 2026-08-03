param(
    [Parameter(Mandatory = $true)]
    [int]$MoneyHomeProcessId,
    [Parameter(Mandatory = $true)]
    [long]$TargetHandle,
    [ValidateSet("move", "drag", "physical-move", "physical-click", "physical-drag", "physical-right-click", "physical-type", "physical-dropdown", "type-chars", "click", "double-click", "post-click", "set-text", "key", "scroll-page-up", "scroll-page-down", "scroll-top", "scroll-bottom", "set-date", "close")]
    [string]$Action,
    [int]$X = 1,
    [int]$Y = 1,
    [int]$X2 = 1,
    [int]$Y2 = 1,
    [string]$Text = "",
    [int]$VirtualKey = 0,
    [datetime]$Date,
    [int]$WaitMilliseconds = 250
)

$ErrorActionPreference = "Stop"

if (-not ("MoneyHomeControlActionNative" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;

public static class MoneyHomeControlActionNative
{
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct SYSTEMTIME
    {
        public ushort Year;
        public ushort Month;
        public ushort DayOfWeek;
        public ushort Day;
        public ushort Hour;
        public ushort Minute;
        public ushort Second;
        public ushort Milliseconds;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct POINT
    {
        public int X;
        public int Y;
    }

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr windowHandle, out uint processId);

    [DllImport("kernel32.dll")]
    public static extern uint GetCurrentThreadId();

    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern IntPtr GetAncestor(IntPtr windowHandle, uint flags);

    [DllImport("user32.dll")]
    public static extern bool AttachThreadInput(uint attachThreadId, uint attachToThreadId, bool attach);

    [DllImport("user32.dll")]
    public static extern bool BringWindowToTop(IntPtr windowHandle);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr windowHandle);

    [DllImport("user32.dll")]
    public static extern IntPtr SetActiveWindow(IntPtr windowHandle);

    [DllImport("user32.dll")]
    public static extern IntPtr SetFocus(IntPtr windowHandle);

    [DllImport("user32.dll")]
    public static extern bool ShowWindowAsync(IntPtr windowHandle, int command);

    [DllImport("user32.dll")]
    public static extern void SwitchToThisWindow(IntPtr windowHandle, bool altTab);

    [DllImport("user32.dll")]
    public static extern bool SetWindowPos(
        IntPtr windowHandle,
        IntPtr insertAfter,
        int x,
        int y,
        int width,
        int height,
        uint flags
    );

    [DllImport("user32.dll")]
    public static extern IntPtr WindowFromPoint(POINT point);

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr windowHandle, out RECT rectangle);

    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int x, int y);

    [DllImport("user32.dll")]
    public static extern int GetSystemMetrics(int index);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint flags, uint dx, uint dy, uint data, UIntPtr extraInfo);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern IntPtr SendMessage(IntPtr windowHandle, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern bool PostMessage(IntPtr windowHandle, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern short VkKeyScan(char character);
}
'@
}

function Set-MoneyHomePhysicalTarget {
    param([IntPtr]$WindowHandle)

    $rootHandle = [MoneyHomeControlActionNative]::GetAncestor($WindowHandle, 2)
    if ($rootHandle -eq [IntPtr]::Zero) {
        throw "无法定位目标控件的根窗口：$WindowHandle"
    }

    $targetThreadId = [MoneyHomeControlActionNative]::GetWindowThreadProcessId(
        $rootHandle,
        [ref]$null
    )
    $foregroundHandle = [MoneyHomeControlActionNative]::GetForegroundWindow()
    $foregroundThreadId = if ($foregroundHandle -ne [IntPtr]::Zero) {
        [MoneyHomeControlActionNative]::GetWindowThreadProcessId($foregroundHandle, [ref]$null)
    }
    else {
        0
    }
    $currentThreadId = [MoneyHomeControlActionNative]::GetCurrentThreadId()
    $attachedForeground = $false
    $attachedTarget = $false
    try {
        if ($foregroundThreadId -ne 0 -and $foregroundThreadId -ne $currentThreadId) {
            $attachedForeground = [MoneyHomeControlActionNative]::AttachThreadInput(
                $currentThreadId,
                $foregroundThreadId,
                $true
            )
        }
        if ($targetThreadId -ne 0 -and $targetThreadId -ne $currentThreadId) {
            $attachedTarget = [MoneyHomeControlActionNative]::AttachThreadInput(
                $currentThreadId,
                $targetThreadId,
                $true
            )
        }

        [void][MoneyHomeControlActionNative]::BringWindowToTop($rootHandle)
        [void][MoneyHomeControlActionNative]::SetForegroundWindow($rootHandle)
        [void][MoneyHomeControlActionNative]::SetActiveWindow($rootHandle)
        [void][MoneyHomeControlActionNative]::SetFocus($WindowHandle)
    }
    finally {
        if ($attachedTarget) {
            [void][MoneyHomeControlActionNative]::AttachThreadInput(
                $currentThreadId,
                $targetThreadId,
                $false
            )
        }
        if ($attachedForeground) {
            [void][MoneyHomeControlActionNative]::AttachThreadInput(
                $currentThreadId,
                $foregroundThreadId,
                $false
            )
        }
    }

    # Windows 前台锁可能拒绝普通激活；恢复并临时置顶后仍用命中测试保护物理输入。
    [void][MoneyHomeControlActionNative]::ShowWindowAsync($rootHandle, 9)
    if (-not [MoneyHomeControlActionNative]::SetWindowPos(
        $rootHandle,
        [IntPtr](-1),
        0,
        0,
        0,
        0,
        0x0043
    )) {
        throw "无法临时置顶目标根窗口：$rootHandle"
    }
    [MoneyHomeControlActionNative]::SwitchToThisWindow($rootHandle, $true)
    [void][MoneyHomeControlActionNative]::BringWindowToTop($rootHandle)
    [void][MoneyHomeControlActionNative]::SetForegroundWindow($rootHandle)
    Start-Sleep -Milliseconds 100
    return $rootHandle
}

function Reset-MoneyHomePhysicalTarget {
    param([IntPtr]$RootHandle)

    [void][MoneyHomeControlActionNative]::SetWindowPos(
        $RootHandle,
        [IntPtr](-2),
        0,
        0,
        0,
        0,
        0x0013
    )
}

function Assert-MoneyHomeScreenPoint {
    param(
        [int]$ScreenX,
        [int]$ScreenY,
        [int]$ExpectedProcessId
    )

    $point = New-Object MoneyHomeControlActionNative+POINT
    $point.X = $ScreenX
    $point.Y = $ScreenY
    $hitHandle = [MoneyHomeControlActionNative]::WindowFromPoint($point)
    if ($hitHandle -eq [IntPtr]::Zero) {
        throw "目标屏幕坐标没有命中窗口：($ScreenX,$ScreenY)"
    }
    $hitProcessId = 0
    [void][MoneyHomeControlActionNative]::GetWindowThreadProcessId(
        $hitHandle,
        [ref]$hitProcessId
    )
    if ($hitProcessId -ne $ExpectedProcessId) {
        throw "目标屏幕坐标命中了其它进程，拒绝物理输入：($ScreenX,$ScreenY) PID=$hitProcessId"
    }
}

function Assert-MoneyHomeForegroundProcess {
    param([int]$ExpectedProcessId)

    $foregroundHandle = [MoneyHomeControlActionNative]::GetForegroundWindow()
    if ($foregroundHandle -eq [IntPtr]::Zero) {
        throw "当前没有前台窗口，拒绝发送物理键盘输入。"
    }
    $foregroundProcessId = 0
    [void][MoneyHomeControlActionNative]::GetWindowThreadProcessId(
        $foregroundHandle,
        [ref]$foregroundProcessId
    )
    if ($foregroundProcessId -ne $ExpectedProcessId) {
        throw "前台窗口属于其它进程，拒绝物理键盘输入：PID=$foregroundProcessId"
    }
}

$targetProcessId = 0
[void][MoneyHomeControlActionNative]::GetWindowThreadProcessId(
    [IntPtr]$TargetHandle,
    [ref]$targetProcessId
)
if ($targetProcessId -ne $MoneyHomeProcessId) {
    throw "TargetHandle $TargetHandle 不属于 MoneyHome8 PID $MoneyHomeProcessId。"
}

switch ($Action) {
    "move" {
        $position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        [void][MoneyHomeControlActionNative]::SendMessage(
            [IntPtr]$TargetHandle,
            0x0200,
            [IntPtr]::Zero,
            $position
        )
    }
    "drag" {
        $startPosition = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        [void][MoneyHomeControlActionNative]::SendMessage(
            [IntPtr]$TargetHandle,
            0x0200,
            [IntPtr]::Zero,
            $startPosition
        )
        [void][MoneyHomeControlActionNative]::SendMessage(
            [IntPtr]$TargetHandle,
            0x0201,
            [IntPtr]1,
            $startPosition
        )
        Start-Sleep -Milliseconds 100
        foreach ($step in 1..12) {
            $currentX = [int][Math]::Round($X + (($X2 - $X) * $step / 12))
            $currentY = [int][Math]::Round($Y + (($Y2 - $Y) * $step / 12))
            $position = [IntPtr](($currentY -shl 16) -bor ($currentX -band 0xffff))
            # MK_LBUTTON 必须随移动消息发送，否则 VCL 只会处理悬停而不会更新拖放草稿。
            [void][MoneyHomeControlActionNative]::SendMessage(
                [IntPtr]$TargetHandle,
                0x0200,
                [IntPtr]1,
                $position
            )
            Start-Sleep -Milliseconds 35
        }
        $endPosition = [IntPtr](($Y2 -shl 16) -bor ($X2 -band 0xffff))
        [void][MoneyHomeControlActionNative]::SendMessage(
            [IntPtr]$TargetHandle,
            0x0202,
            [IntPtr]::Zero,
            $endPosition
        )
        Start-Sleep -Milliseconds 100
    }
    "physical-move" {
        $rootHandle = Set-MoneyHomePhysicalTarget -WindowHandle ([IntPtr]$TargetHandle)
        try {
            $rectangle = New-Object MoneyHomeControlActionNative+RECT
            if (-not [MoneyHomeControlActionNative]::GetWindowRect(
                [IntPtr]$TargetHandle,
                [ref]$rectangle
            )) {
                throw "无法读取目标窗口矩形：$TargetHandle"
            }
            $width = $rectangle.Right - $rectangle.Left
            $height = $rectangle.Bottom - $rectangle.Top
            if ($X -lt 0 -or $Y -lt 0 -or $X -ge $width -or $Y -ge $height) {
                throw "物理移动坐标超出目标窗口：($X,$Y) / ${width}x${height}"
            }
            $screenX = $rectangle.Left + $X
            $screenY = $rectangle.Top + $Y
            if (-not [MoneyHomeControlActionNative]::SetCursorPos($screenX, $screenY)) {
                throw "移动物理光标失败：$TargetHandle ($X,$Y)"
            }
            Assert-MoneyHomeScreenPoint -ScreenX $screenX -ScreenY $screenY -ExpectedProcessId $MoneyHomeProcessId
        }
        finally {
            Reset-MoneyHomePhysicalTarget -RootHandle $rootHandle
        }
    }
    "physical-click" {
        $rootHandle = Set-MoneyHomePhysicalTarget -WindowHandle ([IntPtr]$TargetHandle)
        try {
            $rectangle = New-Object MoneyHomeControlActionNative+RECT
            if (-not [MoneyHomeControlActionNative]::GetWindowRect(
                [IntPtr]$TargetHandle,
                [ref]$rectangle
            )) {
                throw "无法读取目标窗口矩形：$TargetHandle"
            }
            $width = $rectangle.Right - $rectangle.Left
            $height = $rectangle.Bottom - $rectangle.Top
            if ($X -lt 0 -or $Y -lt 0 -or $X -ge $width -or $Y -ge $height) {
                throw "物理点击坐标超出目标窗口：($X,$Y) / ${width}x${height}"
            }
            $screenX = $rectangle.Left + $X
            $screenY = $rectangle.Top + $Y
            if (-not [MoneyHomeControlActionNative]::SetCursorPos($screenX, $screenY)) {
                $screenWidth = [MoneyHomeControlActionNative]::GetSystemMetrics(0)
                $screenHeight = [MoneyHomeControlActionNative]::GetSystemMetrics(1)
                if ($screenWidth -le 1 -or $screenHeight -le 1) {
                    throw "无法读取主屏幕尺寸，拒绝回退物理点击。"
                }
                $absoluteX = [uint32][Math]::Round($screenX * 65535 / ($screenWidth - 1))
                $absoluteY = [uint32][Math]::Round($screenY * 65535 / ($screenHeight - 1))
                [MoneyHomeControlActionNative]::mouse_event(
                    0x8001,
                    $absoluteX,
                    $absoluteY,
                    0,
                    [UIntPtr]::Zero
                )
            }
            # 工具调用返回前桌面宿主可能重新取得顶层顺序，点击前再次置顶并激活目标根窗口。
            [void][MoneyHomeControlActionNative]::SetWindowPos(
                $rootHandle,
                [IntPtr](-1),
                0,
                0,
                0,
                0,
                0x0043
            )
            [void][MoneyHomeControlActionNative]::BringWindowToTop($rootHandle)
            [void][MoneyHomeControlActionNative]::SetForegroundWindow($rootHandle)
            Start-Sleep -Milliseconds 100
            Assert-MoneyHomeScreenPoint -ScreenX $screenX -ScreenY $screenY -ExpectedProcessId $MoneyHomeProcessId
            # 自绘下拉控件依赖真实鼠标状态；坐标校验可防止点击逃逸到其它窗口。
            Start-Sleep -Milliseconds 50
            [MoneyHomeControlActionNative]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 50
            [MoneyHomeControlActionNative]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
        }
        finally {
            Reset-MoneyHomePhysicalTarget -RootHandle $rootHandle
        }
    }
    "physical-drag" {
        $rootHandle = Set-MoneyHomePhysicalTarget -WindowHandle ([IntPtr]$TargetHandle)
        $mouseDown = $false
        try {
            $rectangle = New-Object MoneyHomeControlActionNative+RECT
            if (-not [MoneyHomeControlActionNative]::GetWindowRect(
                [IntPtr]$TargetHandle,
                [ref]$rectangle
            )) {
                throw "无法读取目标窗口矩形：$TargetHandle"
            }
            $width = $rectangle.Right - $rectangle.Left
            $height = $rectangle.Bottom - $rectangle.Top
            foreach ($point in @(@($X, $Y), @($X2, $Y2))) {
                if ($point[0] -lt 0 -or $point[1] -lt 0 -or
                    $point[0] -ge $width -or $point[1] -ge $height) {
                    throw "物理拖动坐标超出目标窗口：($($point[0]),$($point[1])) / ${width}x${height}"
                }
            }

            $startScreenX = $rectangle.Left + $X
            $startScreenY = $rectangle.Top + $Y
            $endScreenX = $rectangle.Left + $X2
            $endScreenY = $rectangle.Top + $Y2
            if (-not [MoneyHomeControlActionNative]::SetCursorPos($startScreenX, $startScreenY)) {
                throw "移动物理光标到拖动起点失败：$TargetHandle ($X,$Y)"
            }
            Assert-MoneyHomeScreenPoint -ScreenX $startScreenX -ScreenY $startScreenY -ExpectedProcessId $MoneyHomeProcessId

            # VCL 自绘排序列表依赖真实按键状态和连续鼠标移动，单独发送控件消息不会更新内部顺序。
            [MoneyHomeControlActionNative]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
            $mouseDown = $true
            Start-Sleep -Milliseconds 120
            foreach ($step in 1..12) {
                $screenX = [int][Math]::Round($startScreenX + (($endScreenX - $startScreenX) * $step / 12))
                $screenY = [int][Math]::Round($startScreenY + (($endScreenY - $startScreenY) * $step / 12))
                if (-not [MoneyHomeControlActionNative]::SetCursorPos($screenX, $screenY)) {
                    throw "移动物理光标执行拖动失败：($screenX,$screenY)"
                }
                Start-Sleep -Milliseconds 40
            }
            Assert-MoneyHomeScreenPoint -ScreenX $endScreenX -ScreenY $endScreenY -ExpectedProcessId $MoneyHomeProcessId
            Start-Sleep -Milliseconds 120
            [MoneyHomeControlActionNative]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
            $mouseDown = $false
            Start-Sleep -Milliseconds 150
        }
        finally {
            if ($mouseDown) {
                [MoneyHomeControlActionNative]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
            }
            Reset-MoneyHomePhysicalTarget -RootHandle $rootHandle
        }
    }
    "physical-right-click" {
        $rootHandle = Set-MoneyHomePhysicalTarget -WindowHandle ([IntPtr]$TargetHandle)
        try {
            $rectangle = New-Object MoneyHomeControlActionNative+RECT
            if (-not [MoneyHomeControlActionNative]::GetWindowRect(
                [IntPtr]$TargetHandle,
                [ref]$rectangle
            )) {
                throw "无法读取目标窗口矩形：$TargetHandle"
            }
            $width = $rectangle.Right - $rectangle.Left
            $height = $rectangle.Bottom - $rectangle.Top
            if ($X -lt 0 -or $Y -lt 0 -or $X -ge $width -or $Y -ge $height) {
                throw "物理右键坐标超出目标窗口：($X,$Y) / ${width}x${height}"
            }
            $screenX = $rectangle.Left + $X
            $screenY = $rectangle.Top + $Y
            if (-not [MoneyHomeControlActionNative]::SetCursorPos($screenX, $screenY)) {
                throw "移动物理光标失败：$TargetHandle ($X,$Y)"
            }
            Assert-MoneyHomeScreenPoint -ScreenX $screenX -ScreenY $screenY -ExpectedProcessId $MoneyHomeProcessId
            # 自绘分类控件只在真实右键状态下建立当前项目和上下文菜单。
            Start-Sleep -Milliseconds 50
            [MoneyHomeControlActionNative]::mouse_event(0x0008, 0, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 50
            [MoneyHomeControlActionNative]::mouse_event(0x0010, 0, 0, 0, [UIntPtr]::Zero)
        }
        finally {
            Reset-MoneyHomePhysicalTarget -RootHandle $rootHandle
        }
    }
    "physical-type" {
        if ([string]::IsNullOrEmpty($Text)) {
            throw "physical-type 操作必须提供 Text。"
        }
        if ($Text -notmatch '^[0-9A-Za-z .,_:/-]+$') {
            throw "physical-type 只允许不含 SendKeys 控制字符的安全 ASCII 文本。"
        }

        $rootHandle = Set-MoneyHomePhysicalTarget -WindowHandle ([IntPtr]$TargetHandle)
        try {
            Add-Type -AssemblyName System.Windows.Forms
            $rectangle = New-Object MoneyHomeControlActionNative+RECT
            if (-not [MoneyHomeControlActionNative]::GetWindowRect(
                [IntPtr]$TargetHandle,
                [ref]$rectangle
            )) {
                throw "无法读取目标窗口矩形：$TargetHandle"
            }
            $width = $rectangle.Right - $rectangle.Left
            $height = $rectangle.Bottom - $rectangle.Top
            if ($X -lt 0 -or $Y -lt 0 -or $X -ge $width -or $Y -ge $height) {
                throw "物理输入坐标超出目标窗口：($X,$Y) / ${width}x${height}"
            }
            $screenX = $rectangle.Left + $X
            $screenY = $rectangle.Top + $Y
            if (-not [MoneyHomeControlActionNative]::SetCursorPos($screenX, $screenY)) {
                throw "移动物理光标失败：$TargetHandle ($X,$Y)"
            }
            Assert-MoneyHomeScreenPoint -ScreenX $screenX -ScreenY $screenY -ExpectedProcessId $MoneyHomeProcessId
            [MoneyHomeControlActionNative]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 50
            [MoneyHomeControlActionNative]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 100
            [void][MoneyHomeControlActionNative]::SetFocus([IntPtr]$TargetHandle)
            Assert-MoneyHomeForegroundProcess -ExpectedProcessId $MoneyHomeProcessId
            # Delphi 自定义金额控件需要真实键盘事件来同步内部数值状态，不能只改窗口文本。
            [System.Windows.Forms.SendKeys]::SendWait('^a')
            [System.Windows.Forms.SendKeys]::SendWait($Text)
        }
        finally {
            Reset-MoneyHomePhysicalTarget -RootHandle $rootHandle
        }
    }
    "physical-dropdown" {
        $rootHandle = Set-MoneyHomePhysicalTarget -WindowHandle ([IntPtr]$TargetHandle)
        try {
            Add-Type -AssemblyName System.Windows.Forms
            [void][MoneyHomeControlActionNative]::SetFocus([IntPtr]$TargetHandle)
            Assert-MoneyHomeForegroundProcess -ExpectedProcessId $MoneyHomeProcessId
            # Delphi 自绘选择器依赖真实组合键状态，普通 WM_KEYDOWN 不会展开候选面板。
            [System.Windows.Forms.SendKeys]::SendWait('%{DOWN}')
        }
        finally {
            Reset-MoneyHomePhysicalTarget -RootHandle $rootHandle
        }
    }
    "type-chars" {
        if ([string]::IsNullOrEmpty($Text)) {
            throw "type-chars 操作必须提供 Text。"
        }
        if ($Text -notmatch '^[0-9A-Za-z .,_:/-]+$') {
            throw "type-chars 只允许安全 ASCII 文本。"
        }

        $position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0201, [IntPtr]1, $position)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0202, [IntPtr]::Zero, $position)
        # 使用控件自己的键盘消息处理链更新 Delphi 自定义编辑器内部值，避免 WM_SETTEXT 绕过状态同步。
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0100, [IntPtr]0x11, [IntPtr]::Zero)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0100, [IntPtr]0x41, [IntPtr]::Zero)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0101, [IntPtr]0x41, [IntPtr]::Zero)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0101, [IntPtr]0x11, [IntPtr]::Zero)
        foreach ($character in $Text.ToCharArray()) {
            $keyScan = [MoneyHomeControlActionNative]::VkKeyScan($character)
            $virtualKey = $keyScan -band 0xff
            if ($virtualKey -ne 0xff) {
                [void][MoneyHomeControlActionNative]::SendMessage(
                    [IntPtr]$TargetHandle,
                    0x0100,
                    [IntPtr]$virtualKey,
                    [IntPtr]::Zero
                )
            }
            [void][MoneyHomeControlActionNative]::SendMessage(
                [IntPtr]$TargetHandle,
                0x0102,
                [IntPtr][int][char]$character,
                [IntPtr]::Zero
            )
            if ($virtualKey -ne 0xff) {
                [void][MoneyHomeControlActionNative]::SendMessage(
                    [IntPtr]$TargetHandle,
                    0x0101,
                    [IntPtr]$virtualKey,
                    [IntPtr]::Zero
                )
            }
        }
    }
    "click" {
        $position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0200, [IntPtr]::Zero, $position)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0201, [IntPtr]1, $position)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0202, [IntPtr]::Zero, $position)
    }
    "double-click" {
        $position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        # 自绘账户列表只在双击消息链中打开工作区，两个独立单击不会触发该处理器。
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0200, [IntPtr]::Zero, $position)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0201, [IntPtr]1, $position)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0202, [IntPtr]::Zero, $position)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0203, [IntPtr]1, $position)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0202, [IntPtr]::Zero, $position)
    }
    "post-click" {
        $position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        # 打开模态窗体的处理器会阻塞同步 SendMessage；异步投递仍由目标控件自己的消息链处理。
        [void][MoneyHomeControlActionNative]::PostMessage([IntPtr]$TargetHandle, 0x0200, [IntPtr]::Zero, $position)
        [void][MoneyHomeControlActionNative]::PostMessage([IntPtr]$TargetHandle, 0x0201, [IntPtr]1, $position)
        [void][MoneyHomeControlActionNative]::PostMessage([IntPtr]$TargetHandle, 0x0202, [IntPtr]::Zero, $position)
    }
    "set-text" {
        $pointer = [System.Runtime.InteropServices.Marshal]::StringToHGlobalUni($Text)
        try {
            [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x000C, [IntPtr]::Zero, $pointer)
        }
        finally {
            [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pointer)
        }
    }
    "key" {
        if ($VirtualKey -le 0) {
            throw "key 操作必须提供 VirtualKey。"
        }
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0100, [IntPtr]$VirtualKey, [IntPtr]::Zero)
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0101, [IntPtr]$VirtualKey, [IntPtr]::Zero)
    }
    "scroll-page-up" {
        # 直接驱动指定滚动容器，避免物理滚轮被其它桌面窗口截获。
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0115, [IntPtr]2, [IntPtr]::Zero)
    }
    "scroll-page-down" {
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0115, [IntPtr]3, [IntPtr]::Zero)
    }
    "scroll-top" {
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0115, [IntPtr]6, [IntPtr]::Zero)
    }
    "scroll-bottom" {
        [void][MoneyHomeControlActionNative]::SendMessage([IntPtr]$TargetHandle, 0x0115, [IntPtr]7, [IntPtr]::Zero)
    }
    "set-date" {
        if ($null -eq $Date) {
            throw "set-date 操作必须提供 Date。"
        }
        $systemTime = New-Object MoneyHomeControlActionNative+SYSTEMTIME
        $systemTime.Year = $Date.Year
        $systemTime.Month = $Date.Month
        $systemTime.DayOfWeek = [int]$Date.DayOfWeek
        $systemTime.Day = $Date.Day
        $systemTime.Hour = $Date.Hour
        $systemTime.Minute = $Date.Minute
        $systemTime.Second = $Date.Second
        $systemTime.Milliseconds = $Date.Millisecond
        $pointer = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(
            [System.Runtime.InteropServices.Marshal]::SizeOf($systemTime)
        )
        try {
            [System.Runtime.InteropServices.Marshal]::StructureToPtr($systemTime, $pointer, $false)
            # DTM_SETSYSTEMTIME 更新标准日期控件的绑定值，避免只改显示文本。
            $result = [MoneyHomeControlActionNative]::SendMessage(
                [IntPtr]$TargetHandle,
                0x1002,
                [IntPtr]0,
                $pointer
            )
            if ($result -eq [IntPtr]::Zero) {
                throw "日期控件拒绝 DTM_SETSYSTEMTIME。"
            }
        }
        finally {
            [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pointer)
        }
    }
    "close" {
        # 异步 WM_CLOSE 走旧程序正常退出流程，若出现确认框仍可继续观察而不会阻塞脚本。
        [void][MoneyHomeControlActionNative]::PostMessage(
            [IntPtr]$TargetHandle,
            0x0010,
            [IntPtr]::Zero,
            [IntPtr]::Zero
        )
    }
}

if ($WaitMilliseconds -gt 0) {
    Start-Sleep -Milliseconds $WaitMilliseconds
}

[pscustomobject]@{
    process_id = $MoneyHomeProcessId
    target_handle = $TargetHandle
    action = $Action
    completed = $true
} | ConvertTo-Json -Depth 3
